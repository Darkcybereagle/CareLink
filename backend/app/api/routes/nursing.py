from datetime import datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.db.database import get_db
from app.db.models import HomeVisitRequest, HomeVisitStatus, NurseCareRecord, Notification, User, UserRole, VisitCheckStatus
from app.schemas.nursing import NurseCareRecordResponse, NurseCareRecordUpsert, VisitActionResponse

router=APIRouter(prefix="/nurses",tags=["Nursing"])
CurrentUser=Annotated[User,Depends(get_current_user)]; DB=Annotated[Session,Depends(get_db)]
def nurse_only(user):
    if user.role!=UserRole.NURSE: raise HTTPException(403,"Nurse access required")
def assigned(db,user_id,visit_id):
    visit=db.scalar(select(HomeVisitRequest).where(HomeVisitRequest.id==visit_id,HomeVisitRequest.provider_id==user_id))
    if not visit: raise HTTPException(404,"Assigned home visit not found")
    return visit

@router.post("/home-visits/{visit_id}/check-in",response_model=VisitActionResponse)
def check_in(visit_id:int,current_user:CurrentUser,db:DB):
    nurse_only(current_user); visit=assigned(db,current_user.id,visit_id)
    if visit.status not in (HomeVisitStatus.ACCEPTED,HomeVisitStatus.IN_PROGRESS): raise HTTPException(409,"Visit is not ready for check-in")
    visit.status=HomeVisitStatus.IN_PROGRESS; visit.check_status=VisitCheckStatus.CHECKED_IN; visit.checked_in_at=datetime.now(timezone.utc)
    db.add(Notification(user_id=visit.patient_id,title="Nurse checked in",body=f"{current_user.full_name} has started your CareLink home visit."))
    db.commit(); db.refresh(visit); return visit

@router.put("/home-visits/{visit_id}/care-record",response_model=NurseCareRecordResponse)
def care_record(visit_id:int,data:NurseCareRecordUpsert,current_user:CurrentUser,db:DB):
    nurse_only(current_user); visit=assigned(db,current_user.id,visit_id)
    if visit.check_status!=VisitCheckStatus.CHECKED_IN: raise HTTPException(409,"Check in before recording care")
    row=db.scalar(select(NurseCareRecord).where(NurseCareRecord.home_visit_id==visit.id))
    if not row: row=NurseCareRecord(home_visit_id=visit.id,nurse_id=current_user.id,patient_id=visit.patient_id)
    for k,v in data.model_dump().items(): setattr(row,k,v)
    if data.escalation_required and not data.escalation_note: raise HTTPException(400,"Escalation note is required")
    db.add(row)
    if data.escalation_required: db.add(Notification(user_id=visit.patient_id,title="Care escalation recorded",body="Your nurse recorded that further professional assessment is required."))
    db.commit(); db.refresh(row); return row

@router.get("/home-visits/{visit_id}/care-record",response_model=NurseCareRecordResponse)
def get_record(visit_id:int,current_user:CurrentUser,db:DB):
    nurse_only(current_user); visit=assigned(db,current_user.id,visit_id)
    row=db.scalar(select(NurseCareRecord).where(NurseCareRecord.home_visit_id==visit.id))
    if not row: raise HTTPException(404,"Care record not found")
    return row

@router.post("/home-visits/{visit_id}/check-out",response_model=VisitActionResponse)
def check_out(visit_id:int,current_user:CurrentUser,db:DB):
    nurse_only(current_user); visit=assigned(db,current_user.id,visit_id)
    if visit.check_status!=VisitCheckStatus.CHECKED_IN: raise HTTPException(409,"Visit is not checked in")
    if not db.scalar(select(NurseCareRecord).where(NurseCareRecord.home_visit_id==visit.id)): raise HTTPException(409,"Complete the care record before check-out")
    visit.check_status=VisitCheckStatus.CHECKED_OUT; visit.checked_out_at=datetime.now(timezone.utc); visit.status=HomeVisitStatus.COMPLETED
    db.add(Notification(user_id=visit.patient_id,title="Home visit completed",body=f"{current_user.full_name} completed your CareLink home visit."))
    db.commit(); db.refresh(visit); return visit
