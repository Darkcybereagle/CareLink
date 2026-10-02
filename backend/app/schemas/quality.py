from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class ReviewCreate(BaseModel):
    appointment_id:int
    rating:int=Field(ge=1,le=5)
    communication:int|None=Field(default=None,ge=1,le=5)
    punctuality:int|None=Field(default=None,ge=1,le=5)
    professionalism:int|None=Field(default=None,ge=1,le=5)
    respect:int|None=Field(default=None,ge=1,le=5)
    clarity:int|None=Field(default=None,ge=1,le=5)
    comment:str|None=Field(default=None,max_length=3000)
class ReviewResponse(ReviewCreate):
    model_config=ConfigDict(from_attributes=True)
    id:int; patient_id:int; provider_id:int; created_at:datetime
class ComplaintCreate(BaseModel):
    provider_id:int; appointment_id:int|None=None; category:str=Field(min_length=3,max_length=80); description:str=Field(min_length=5,max_length=4000)
class ComplaintResponse(ComplaintCreate):
    model_config=ConfigDict(from_attributes=True)
    id:int; patient_id:int; status:str; created_at:datetime
class ProviderQualityResponse(BaseModel):
    provider_id:int; cases_completed:int; appointments_completed:int; home_visits_completed:int
    average_rating:float|None; review_count:int; complaint_count:int; open_complaints:int
    cancellation_count:int; no_show_reports:int; average_response_minutes:float|None=None
