from datetime import date, datetime, time
from pydantic import BaseModel, ConfigDict, Field

class ProviderProfileCreate(BaseModel):
    provider_type:str=Field(min_length=4,max_length=30)
    specialty:str|None=Field(default=None,max_length=120)
    license_number:str|None=Field(default=None,max_length=120)
    phone:str|None=Field(default=None,max_length=30)
    facility_name:str|None=Field(default=None,max_length=160)
    city:str|None=Field(default=None,max_length=80)
    bio:str|None=Field(default=None,max_length=3000)
    gender:str|None=Field(default=None,max_length=30)
    date_of_birth:date|None=None
    professional_title:str|None=Field(default=None,max_length=120)
    qualifications:str|None=Field(default=None,max_length=3000)
    languages:str|None=Field(default=None,max_length=255)
    years_experience:int|None=Field(default=None,ge=0,le=80)
    service_radius_km:int|None=Field(default=None,ge=0,le=1000)
    offers_home_visits:bool=False
    consultation_modes:str|None=Field(default=None,max_length=120)
class ProviderProfileResponse(ProviderProfileCreate):
    model_config=ConfigDict(from_attributes=True)
    id:int; user_id:int; verification_status:str; is_available:bool
class AvailabilityCreate(BaseModel):
    day_of_week:int=Field(ge=0,le=6); start_time:time; end_time:time
class AvailabilityResponse(AvailabilityCreate):
    model_config=ConfigDict(from_attributes=True)
    id:int; provider_id:int
class StatusUpdate(BaseModel): status:str
class ProviderMessageThread(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int; patient_id:int; provider_id:int; created_at:datetime
class PatientSummary(BaseModel):
    intake_id:int; patient_id:int; patient_name:str; symptoms:str; duration:str|None; urgency:str; summary:str; clinician_handoff:str; created_at:datetime
class ProviderFollowUpCreate(BaseModel):
    patient_id:int; scheduled_at:datetime; note:str=Field(min_length=3,max_length=2000)
