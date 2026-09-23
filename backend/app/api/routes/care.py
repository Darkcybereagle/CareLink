from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.db.models import (
    Appointment, AppointmentStatus, FollowUp, HomeVisitRequest, Hospital, Message,
    MessageThread, Notification, ProviderProfile, User, UserRole, VerificationStatus,
)
from app.schemas.care import (
    AppointmentCreate, AppointmentResponse, FollowUpCreate, FollowUpResponse,
    HomeVisitCreate, HomeVisitResponse, HospitalCard, MessageCreate, MessageResponse,
    NotificationResponse, ProviderCard, ThreadCreate,
)

router = APIRouter(prefix="/care", tags=["Patient Care"])
CurrentUser = Annotated[User, Depends(get_current_user)]
DB = Annotated[Session, Depends(get_db)]


def patient_only(user: User) -> None:
    if user.role != UserRole.PATIENT:
        raise HTTPException(status_code=403, detail="Patient access required")


@router.get("/providers", response_model=list[ProviderCard])
def discover_providers(current_user: CurrentUser, db: DB, city: str | None = None, specialty: str | None = None):
    patient_only(current_user)
    query = select(ProviderProfile, User).join(User, ProviderProfile.user_id == User.id).where(
        User.is_active.is_(True), ProviderProfile.is_available.is_(True)
    )
    if city:
        query = query.where(ProviderProfile.city.ilike(f"%{city.strip()}%"))
    if specialty:
        query = query.where(ProviderProfile.specialty.ilike(f"%{specialty.strip()}%"))
    rows = db.execute(query).all()
    return [
        ProviderCard(
            id=user.id,
            full_name=user.full_name,
            provider_type=profile.provider_type,
            specialty=profile.specialty,
            facility_name=profile.facility_name,
            city=profile.city,
            verification_status=profile.verification_status.value,
            is_available=profile.is_available,
        )
        for profile, user in rows
    ]


@router.get("/hospitals", response_model=list[HospitalCard])
def discover_hospitals(current_user: CurrentUser, db: DB, city: str | None = None):
    patient_only(current_user)
    query = select(Hospital).where(Hospital.is_active.is_(True))
    if city:
        query = query.where(Hospital.city.ilike(f"%{city.strip()}%"))
    return list(db.scalars(query).all())


@router.post("/appointments", response_model=AppointmentResponse, status_code=201)
def request_appointment(data: AppointmentCreate, current_user: CurrentUser, db: DB):
    patient_only(current_user)
    provider = db.scalar(select(User).where(User.id == data.provider_id, User.role.in_([UserRole.DOCTOR, UserRole.NURSE]), User.is_active.is_(True)))
    profile = db.scalar(select(ProviderProfile).where(ProviderProfile.user_id == data.provider_id))
    if not provider or not profile or profile.verification_status != VerificationStatus.VERIFIED:
        raise HTTPException(status_code=400, detail="Provider is not verified for booking")
    appointment = Appointment(patient_id=current_user.id, **data.model_dump())
    db.add(appointment)
    db.add(Notification(user_id=provider.id, title="New appointment request", body=f"{current_user.full_name} requested an appointment."))
    db.commit()
    db.refresh(appointment)
    return appointment


@router.get("/appointments", response_model=list[AppointmentResponse])
def patient_appointments(current_user: CurrentUser, db: DB):
    patient_only(current_user)
    return list(db.scalars(select(Appointment).where(Appointment.patient_id == current_user.id).order_by(Appointment.scheduled_at.desc())).all())


@router.post("/home-visits", response_model=HomeVisitResponse, status_code=201)
def request_home_visit(data: HomeVisitCreate, current_user: CurrentUser, db: DB):
    patient_only(current_user)
    if data.provider_id:
        provider = db.scalar(select(User).where(User.id == data.provider_id, User.role.in_([UserRole.DOCTOR, UserRole.NURSE]), User.is_active.is_(True)))
        profile = db.scalar(select(ProviderProfile).where(ProviderProfile.user_id == data.provider_id))
        if not provider or not profile or profile.verification_status != VerificationStatus.VERIFIED:
            raise HTTPException(status_code=400, detail="Provider is not verified for home visits")
    visit = HomeVisitRequest(patient_id=current_user.id, **data.model_dump())
    db.add(visit)
    if data.provider_id:
        db.add(Notification(user_id=data.provider_id, title="New home-care request", body=f"{current_user.full_name} requested home care."))
    db.commit()
    db.refresh(visit)
    return visit


@router.get("/home-visits", response_model=list[HomeVisitResponse])
def patient_home_visits(current_user: CurrentUser, db: DB):
    patient_only(current_user)
    return list(db.scalars(select(HomeVisitRequest).where(HomeVisitRequest.patient_id == current_user.id).order_by(HomeVisitRequest.requested_at.desc())).all())


@router.post("/threads", response_model=dict, status_code=201)
def create_thread(data: ThreadCreate, current_user: CurrentUser, db: DB):
    patient_only(current_user)
    provider = db.scalar(select(User).where(User.id == data.provider_id, User.role.in_([UserRole.DOCTOR, UserRole.NURSE]), User.is_active.is_(True)))
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    thread = db.scalar(select(MessageThread).where(MessageThread.patient_id == current_user.id, MessageThread.provider_id == data.provider_id))
    if not thread:
        thread = MessageThread(patient_id=current_user.id, provider_id=data.provider_id)
        db.add(thread)
        db.commit()
        db.refresh(thread)
    return {"id": thread.id, "patient_id": thread.patient_id, "provider_id": thread.provider_id, "created_at": thread.created_at}


@router.get("/threads/{thread_id}/messages", response_model=list[MessageResponse])
def get_messages(thread_id: int, current_user: CurrentUser, db: DB):
    thread = db.get(MessageThread, thread_id)
    if not thread or current_user.id not in (thread.patient_id, thread.provider_id):
        raise HTTPException(status_code=404, detail="Conversation not found")
    return list(db.scalars(select(Message).where(Message.thread_id == thread_id).order_by(Message.created_at)).all())


@router.post("/threads/{thread_id}/messages", response_model=MessageResponse, status_code=201)
def send_message(thread_id: int, data: MessageCreate, current_user: CurrentUser, db: DB):
    thread = db.get(MessageThread, thread_id)
    if not thread or current_user.id not in (thread.patient_id, thread.provider_id):
        raise HTTPException(status_code=404, detail="Conversation not found")
    message = Message(thread_id=thread_id, sender_id=current_user.id, body=data.body.strip())
    recipient = thread.provider_id if current_user.id == thread.patient_id else thread.patient_id
    db.add(message)
    db.add(Notification(user_id=recipient, title="New CareLink message", body=f"{current_user.full_name} sent you a message."))
    db.commit()
    db.refresh(message)
    return message


@router.get("/notifications", response_model=list[NotificationResponse])
def notifications(current_user: CurrentUser, db: DB):
    return list(db.scalars(select(Notification).where(Notification.user_id == current_user.id).order_by(Notification.created_at.desc())).all())


@router.patch("/notifications/{notification_id}/read", response_model=NotificationResponse)
def mark_notification_read(notification_id: int, current_user: CurrentUser, db: DB):
    notification = db.scalar(select(Notification).where(Notification.id == notification_id, Notification.user_id == current_user.id))
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    notification.is_read = True
    db.commit()
    db.refresh(notification)
    return notification


@router.post("/follow-ups", response_model=FollowUpResponse, status_code=201)
def create_follow_up(data: FollowUpCreate, current_user: CurrentUser, db: DB):
    patient_only(current_user)
    provider = db.scalar(select(User).where(User.id == data.provider_id, User.role.in_([UserRole.DOCTOR, UserRole.NURSE])))
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    follow_up = FollowUp(patient_id=current_user.id, **data.model_dump())
    db.add(follow_up)
    db.add(Notification(user_id=data.provider_id, title="Follow-up requested", body=f"{current_user.full_name} requested a follow-up."))
    db.commit()
    db.refresh(follow_up)
    return follow_up


@router.get("/follow-ups", response_model=list[FollowUpResponse])
def patient_follow_ups(current_user: CurrentUser, db: DB):
    patient_only(current_user)
    return list(db.scalars(select(FollowUp).where(FollowUp.patient_id == current_user.id).order_by(FollowUp.scheduled_at.desc())).all())
