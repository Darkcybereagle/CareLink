from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.db.models import User
from app.schemas.ai import AIIntakeRequest, AIIntakeResponse

router = APIRouter(prefix="/ai", tags=["AI Assistant"])

EMERGENCY_SIGNALS = (
    "chest pain",
    "difficulty breathing",
    "can't breathe",
    "cannot breathe",
    "severe bleeding",
    "unconscious",
    "not breathing",
    "seizure",
    "convulsion",
    "stroke",
    "face drooping",
    "slurred speech",
    "sudden weakness",
)

URGENT_SIGNALS = (
    "severe pain",
    "high fever",
    "persistent vomiting",
    "fainting",
    "confusion",
    "dehydration",
    "heavy bleeding",
)


@router.post("/intake", response_model=AIIntakeResponse)
def intake(data: AIIntakeRequest, current_user: User = Depends(get_current_user)) -> AIIntakeResponse:
    text = data.symptoms.lower().strip()

    if any(signal in text for signal in EMERGENCY_SIGNALS):
        urgency = "emergency"
        safety_message = (
            "Some information you provided may indicate an emergency. "
            "Please seek urgent emergency medical care now or contact your local emergency service. "
            "Do not rely on this AI response as a diagnosis."
        )
        next_step = "Emergency professional assessment now."
    elif any(signal in text for signal in URGENT_SIGNALS):
        urgency = "urgent"
        safety_message = (
            "Your symptoms may need prompt assessment by a qualified healthcare professional. "
            "CareLink will prioritize professional review."
        )
        next_step = "Arrange prompt professional medical assessment."
    else:
        urgency = "routine"
        safety_message = (
            "No configured emergency signal was detected from this short intake. "
            "This does not rule out a serious condition."
        )
        next_step = "Continue with CareLink's normal care-routing flow and professional review as needed."

    duration_text = data.duration.strip() if data.duration else "duration not provided"
    summary = f"Patient-reported concern: {data.symptoms.strip()}. Duration: {duration_text}."
    clinician_handoff = (
        f"Patient {current_user.full_name} reported: {data.symptoms.strip()}. "
        f"Reported duration: {duration_text}. "
        "This is an intake summary for a qualified clinician, not a diagnosis."
    )

    return AIIntakeResponse(
        urgency=urgency,
        safety_message=safety_message,
        summary=summary,
        next_step=next_step,
        clinician_handoff=clinician_handoff,
    )
