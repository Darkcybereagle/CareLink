from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.db.database import get_db
from app.db.models import Appointment, AppointmentStatus, HomeVisitRequest, HomeVisitStatus, ProviderComplaint, ProviderReview, User, UserRole
from app.schemas.quality import ComplaintCreate, ComplaintResponse, ProviderQualityResponse, ReviewCreate, ReviewResponse

router=APIRouter(prefix="/quality",tags=["Provider Quality"])
CurrentUser=Annotated[User,Depends(get_current_user)]; DB=Annotated[Session,Depends(get_db)]

def patient_only(user):
    if user.role!=UserRole.PATIENT: raise HTTPException(403,"Patient access required")

@router.post("/reviews",response_model=ReviewResponse,status_code=201)
def review(data:ReviewCreate,current_user:CurrentUser,db:DB):
    patient_only(current_user)
    appointment=db.scalar(select(Appointment).where(Appointment.id==data.appointment_id,Appointment.patient_id==current_user.id))
    if not appointment or appointment.status!=AppointmentStatus.COMPLETED: raise HTTPException(400,"Only completed CareLink appointments can be reviewed")
    if db.scalar(select(ProviderReview).where(ProviderReview.patient_id==current_user.id,ProviderReview.appointment_id==appointment.id)):
        raise HTTPException(409,"This appointment has already been reviewed")
    row=ProviderReview(patient_id=current_user.id,provider_id=appointment.provider_id,**data.model_dump())
    db.add(row); db.commit(); db.refresh(row); return row

@router.get("/providers/{provider_id}/reviews",response_model=list[ReviewResponse])
def reviews(provider_id:int,current_user:CurrentUser,db:DB):
    return list(db.scalars(select(ProviderReview).where(ProviderReview.provider_id==provider_id).order_by(ProviderReview.created_at.desc())).all())

@router.post("/complaints",response_model=ComplaintResponse,status_code=201)
def complaint(data:ComplaintCreate,current_user:CurrentUser,db:DB):
    patient_only(current_user)
    if data.appointment_id:
        appointment=db.scalar(select(Appointment).where(Appointment.id==data.appointment_id,Appointment.patient_id==current_user.id,Appointment.provider_id==data.provider_id))
        if not appointment: raise HTTPException(400,"Appointment does not belong to this patient/provider")
    row=ProviderComplaint(patient_id=current_user.id,**data.model_dump())
    db.add(row); db.commit(); db.refresh(row); return row

@router.get("/providers/{provider_id}",response_model=ProviderQualityResponse)
def quality(provider_id:int,current_user:CurrentUser,db:DB):
    completed_a=db.scalar(select(func.count()).select_from(Appointment).where(Appointment.provider_id==provider_id,Appointment.status==AppointmentStatus.COMPLETED)) or 0
    completed_h=db.scalar(select(func.count()).select_from(HomeVisitRequest).where(HomeVisitRequest.provider_id==provider_id,HomeVisitRequest.status==HomeVisitStatus.COMPLETED)) or 0
    avg=db.scalar(select(func.avg(ProviderReview.rating)).where(ProviderReview.provider_id==provider_id))
    reviews=db.scalar(select(func.count()).select_from(ProviderReview).where(ProviderReview.provider_id==provider_id)) or 0
    complaints=db.scalar(select(func.count()).select_from(ProviderComplaint).where(ProviderComplaint.provider_id==provider_id)) or 0
    open_c=db.scalar(select(func.count()).select_from(ProviderComplaint).where(ProviderComplaint.provider_id==provider_id,ProviderComplaint.status.in_(["OPEN","REVIEWING"]))) or 0
    cancelled=db.scalar(select(func.count()).select_from(Appointment).where(Appointment.provider_id==provider_id,Appointment.status==AppointmentStatus.CANCELLED)) or 0
    no_shows=db.scalar(select(func.count()).select_from(ProviderComplaint).where(ProviderComplaint.provider_id==provider_id,ProviderComplaint.category=="provider_no_show")) or 0
    return ProviderQualityResponse(provider_id=provider_id,cases_completed=completed_a+completed_h,appointments_completed=completed_a,home_visits_completed=completed_h,average_rating=round(float(avg),2) if avg is not None else None,review_count=reviews,complaint_count=complaints,open_complaints=open_c,cancellation_count=cancelled,no_show_reports=no_shows)
