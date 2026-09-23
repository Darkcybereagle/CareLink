from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.db.models import (
    AIIntake, Appointment, AppointmentStatus, FollowUp, HomeVisitRequest,
    HomeVisitStatus, Message, MessageThread, Notification, ProviderAvailability,
    ProviderProfile, User, UserRole,
)
from app.schemas.care import (
    AppointmentResponse, FollowUpResponse, HomeVisitResponse, MessageCreate,
    MessageResponse, NotificationResponse,
)
from app.schemas.providers import (
    AvailabilityCreate, AvailabilityResponse, PatientSummary, ProviderProfileCreate,
    ProviderProfileResponse,
)

router = APIRouter(prefix="/providers", tags=["Providers"])
CurrentUser = Annotated[User, Depends(get_current_user)]
DB = Annotated[Session, Depends(get_db)]


def provider_only(user: User) -> None:
    if user.role not in (UserRole.DOCTOR, UserRole.NURSE):
        raise HTTPException(status_code=403, detail="Provider access required")


@router.get("/me", response_model=ProviderProfileResponse)
def get_profile(current_user: CurrentUser, db: DB):
    provider_only(current_user)
    profile = db.scalar(select(ProviderProfile).where(ProviderProfile.user_id == current_user.id))
    if not profile:
        raise HTTPException(status_code=404, detail="Provider profile not created")
    return profile


@router.post("/me/profile", response_model=ProviderProfileResponse, status_code=201)
def create_profile(data: ProviderProfileCreate, current_user: CurrentUser, db: DB):
    provider_only(current_user)
    existing = db.scalar(select(ProviderProfile).where(ProviderProfile.user_id == current_user.id))
    if existing:
        raise HTTPException(status_code=409, detail="Provider profile already exists")
    if data.provider_type != current_user.role.value:
        raise HTTPException(status_code=400, detail="Provider type must match the account role")
    profile = ProviderProfile(user_id=current_user.id, **data.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.patch("/me/profile", response_model=ProviderProfileResponse)
def update_profile(data: ProviderProfileCreate, current_user: CurrentUser, db: DB):
    provider_only(current_user)
    profile = db.scalar(select(ProviderProfile).where(ProviderProfile.user_id == current_user.id))
    if not profile:
        raise HTTPException(status_code=404, detail="Provider profile not created")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)
    db.commit()
    db.refresh(profile)
    return profile


@router.post("/me/availability", response_model=AvailabilityResponse, status_code=201)
def add_availability(data: AvailabilityCreate, current_user: CurrentUser, db: DB):
    provider_only(current_user)
    row = ProviderAvailability(provider_id=current_user.id, **data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.get("/me/availability", response_model=list[AvailabilityResponse])
def availability(current_user: CurrentUser, db: DB):
    provider_only(current_user)
    return list(db.scalars(select(ProviderAvailability).where(ProviderAvailability.provider_id == current_user.id)).all())


@router.get("/appointments", response_model=list[AppointmentResponse])
def appointments(current_user: CurrentUser, db: DB):
    provider_only(current_user)
    return list(db.scalars(select(Appointment).where(Appointment.provider_id == current_user.id).order_by(Appointment.scheduled_at.desc())).all())


@router.patch("/appointments/{appointment_id}/status", response_model=AppointmentResponse)
def update_appointment(appointment_id: int, data: dict, current_user: CurrentUser, db: DB):
    provider_only(current_user)
    appointment = db.scalar(select(Appointment).where(Appointment.id == appointment_id, Appointment.provider_id == current_user.id))
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if data.get("status") not in {s.value for s in AppointmentStatus}:
        raise HTTPException(status_code=400, detail="Invalid appointment status")
    appointment.status = AppointmentStatus(data["status"])
    db.add(Notification(user_id=appointment.patient_id, title="Appointment updated", body=f"Appointment status: {appointment.status.value}."))
    db.commit()
    db.refresh(appointment)
    return appointment


@router.get("/home-visits", response_model=list[HomeVisitResponse])
def home_visits(current_user: CurrentUser, db: DB):
    provider_only(current_user)
    return list(db.scalars(select(HomeVisitRequest).where(HomeVisitRequest.provider_id == current_user.id).order_by(HomeVisitRequest.requested_at.desc())).all())


@router.patch("/home-visits/{visit_id}/status", response_model=HomeVisitResponse)
def update_home_visit(visit_id: int, data: dict, current_user: CurrentUser, db: DB):
    provider_only(current_user)
    visit = db.scalar(select(HomeVisitRequest).where(HomeVisitRequest.id == visit_id, HomeVisitRequest.provider_id == current_user.id))
    if not visit:
        raise HTTPException(status_code=404, detail="Home visit not found")
    if data.get("status") not in {"accepted", "completed", "cancelled"}:
        raise HTTPException(status_code=400, detail="Invalid home visit status")
    visit.status = HomeVisitStatus(data["status"])
    db.add(Notification(user_id=visit.patient_id, title="Home-care request updated", body=f"Home-care status: {visit.status.value}."))
    db.commit()
    db.refresh(visit)
    return visit


@router.get("/ai-summaries", response_model=list[PatientSummary])
def ai_summaries(current_user: CurrentUser, db: DB):
    provider_only(current_user)
    rows = db.execute(
        select(AIIntake, User)
        .join(User, AIIntake.patient_id == User.id)
        .order_by(AIIntake.created_at.desc())
    ).all()
    return [
        PatientSummary(
            intake_id=intake.id,
            patient_id=patient.id,
            patient_name=patient.full_name,
            symptoms=intake.symptoms,
            duration=intake.duration,
            urgency=intake.urgency,
            summary=intake.summary,
            clinician_handoff=intake.clinician_handoff,
            created_at=intake.created_at,
        )
        for intake, patient in rows
    ]


@router.get("/threads/{thread_id}/messages", response_model=list[MessageResponse])
def provider_messages(thread_id: int, current_user: CurrentUser, db: DB):
    provider_only(current_user)
    thread = db.scalar(select(MessageThread).where(MessageThread.id == thread_id, MessageThread.provider_id == current_user.id))
    if not thread:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return list(db.scalars(select(Message).where(Message.thread_id == thread_id).order_by(Message.created_at)).all())


@router.post("/threads/{thread_id}/messages", response_model=MessageResponse, status_code=201)
def provider_send_message(thread_id: int, data: MessageCreate, current_user: CurrentUser, db: DB):
    provider_only(current_user)
    thread = db.scalar(select(MessageThread).where(MessageThread.id == thread_id, MessageThread.provider_id == current_user.id))
    if not thread:
        raise HTTPException(status_code=404, detail="Conversation not found")
    message = Message(thread_id=thread_id, sender_id=current_user.id, body=data.body.strip())
    db.add(message)
    db.add(Notification(user_id=thread.patient_id, title="New CareLink message", body=f"{current_user.full_name} sent you a message."))
    db.commit()
    db.refresh(message)
    return message


@router.get("/notifications", response_model=list[NotificationResponse])
def provider_notifications(current_user: CurrentUser, db: DB):
    provider_only(current_user)
    return list(db.scalars(select(Notification).where(Notification.user_id == current_user.id).order_by(Notification.created_at.desc())).all())



@router.get("/threads", response_model=list[ProviderMessageThread])
def provider_threads(current_user: CurrentUser, db: DB):
    provider_only(current_user)
    return list(db.scalars(select(MessageThread).where(MessageThread.provider_id == current_user.id).order_by(MessageThread.created_at.desc())).all())


@router.get("/follow-ups", response_model=list[FollowUpResponse])
def provider_follow_ups(current_user: CurrentUser, db: DB):
    provider_only(current_user)
    return list(db.scalars(select(FollowUp).where(FollowUp.provider_id == current_user.id).order_by(FollowUp.scheduled_at.desc())).all())


@router.patch("/follow-ups/{follow_up_id}/complete", response_model=FollowUpResponse)
def complete_follow_up(follow_up_id: int, current_user: CurrentUser, db: DB):
    provider_only(current_user)
    row = db.scalar(select(FollowUp).where(FollowUp.id == follow_up_id, FollowUp.provider_id == current_user.id))
    if not row:
        raise HTTPException(status_code=404, detail="Follow-up not found")
    row.completed = True
    db.add(Notification(user_id=row.patient_id, title="Follow-up completed", body="Your provider marked the follow-up complete."))
    db.commit()
    db.refresh(row)
    return row
