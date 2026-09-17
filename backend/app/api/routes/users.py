from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.db.models import PatientProfile, User, UserRole
from app.schemas.users import (
    PatientProfileCreate,
    PatientProfileResponse,
    PatientProfileUpdate,
    UserResponse,
)

router = APIRouter(prefix="/users", tags=["Users"])

CurrentUser = Annotated[User, Depends(get_current_user)]
DatabaseSession = Annotated[Session, Depends(get_db)]


@router.get("/me", response_model=UserResponse)
def get_my_account(current_user: CurrentUser) -> UserResponse:
    return current_user


@router.get("/me/patient-profile", response_model=PatientProfileResponse)
def get_patient_profile(current_user: CurrentUser) -> PatientProfileResponse:
    if current_user.role != UserRole.PATIENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Patient profile required")
    profile = current_user.patient_profile
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient profile not created")
    return profile


@router.post("/me/patient-profile", response_model=PatientProfileResponse, status_code=status.HTTP_201_CREATED)
def create_patient_profile(data: PatientProfileCreate, current_user: CurrentUser, db: DatabaseSession) -> PatientProfileResponse:
    if current_user.role != UserRole.PATIENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Patient profile required")
    if current_user.patient_profile is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Patient profile already exists")
    profile = PatientProfile(user_id=current_user.id, **data.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.patch("/me/patient-profile", response_model=PatientProfileResponse)
def update_patient_profile(data: PatientProfileUpdate, current_user: CurrentUser, db: DatabaseSession) -> PatientProfileResponse:
    if current_user.role != UserRole.PATIENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Patient profile required")
    profile = current_user.patient_profile
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient profile not created")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)
    db.commit()
    db.refresh(profile)
    return profile
