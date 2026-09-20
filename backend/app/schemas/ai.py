from typing import Literal

from pydantic import BaseModel, Field


class AIIntakeRequest(BaseModel):
    symptoms: str = Field(min_length=3, max_length=3000)
    duration: str | None = Field(default=None, max_length=120)


class AIIntakeResponse(BaseModel):
    urgency: Literal["emergency", "urgent", "routine"]
    safety_message: str
    summary: str
    next_step: str
    clinician_handoff: str
