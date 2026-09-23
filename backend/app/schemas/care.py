from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProviderCard(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    provider_type: str
    specialty: str | None
    facility_name: str | None
    city: str | None
    verification_status: str
    is_available: bool


class HospitalCard(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    address: str
    city: str
    phone: str | None
    services: str | None


class AppointmentCreate(BaseModel):
    provider_id: int
    scheduled_at: datetime
    reason: str = Field(min_length=3, max_length=2000)


class AppointmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    patient_id: int
    provider_id: int
    scheduled_at: datetime
    reason: str
    status: str
    notes: str | None


class HomeVisitCreate(BaseModel):
    provider_id: int | None = None
    address: str = Field(min_length=5, max_length=255)
    reason: str = Field(min_length=3, max_length=2000)


class HomeVisitResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    patient_id: int
    provider_id: int | None
    address: str
    requested_at: datetime
    reason: str
    status: str


class ThreadCreate(BaseModel):
    provider_id: int


class MessageCreate(BaseModel):
    body: str = Field(min_length=1, max_length=4000)


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    thread_id: int
    sender_id: int
    body: str
    created_at: datetime


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    body: str
    is_read: bool
    created_at: datetime


class FollowUpCreate(BaseModel):
    provider_id: int
    scheduled_at: datetime
    note: str = Field(min_length=3, max_length=2000)


class FollowUpResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    patient_id: int
    provider_id: int
    scheduled_at: datetime
    note: str
    completed: bool
