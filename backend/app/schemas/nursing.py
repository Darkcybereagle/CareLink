from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
class NurseCareRecordUpsert(BaseModel):
    vitals:str|None=Field(default=None,max_length=3000)
    observations:str|None=Field(default=None,max_length=5000)
    interventions:str|None=Field(default=None,max_length=5000)
    escalation_required:bool=False
    escalation_note:str|None=Field(default=None,max_length=5000)
class NurseCareRecordResponse(NurseCareRecordUpsert):
    model_config=ConfigDict(from_attributes=True)
    id:int; home_visit_id:int; nurse_id:int; patient_id:int; created_at:datetime; updated_at:datetime
class VisitActionResponse(BaseModel):
    id:int; status:str; check_status:str; checked_in_at:datetime|None; checked_out_at:datetime|None
