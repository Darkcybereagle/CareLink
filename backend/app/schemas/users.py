from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: str
    role: str
    is_active: bool


class PatientProfileCreate(BaseModel):
    phone: str | None = Field(default=None, max_length=30)
    date_of_birth: date | None = None
    gender: str | None = Field(default=None, max_length=30)
    address: str | None = Field(default=None, max_length=255)
    emergency_contact_name: str | None = Field(default=None, max_length=120)
    emergency_contact_phone: str | None = Field(default=None, max_length=30)


class PatientProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    phone: str | None
    date_of_birth: date | None
    gender: str | None
    address: str | None
    emergency_contact_name: str | None
    emergency_contact_phone: str | None


class PatientProfileUpdate(PatientProfileCreate):
    pass
