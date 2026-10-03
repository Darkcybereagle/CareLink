from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from app.db.models import Appointment, AppointmentStatus, HomeVisitRequest, HomeVisitStatus, ProviderProfile, User, VerificationStatus
from conftest import TestingSessionLocal, auth_header

def make_verified_provider(client,role="nurse",email="quality-nurse@carelink.example.com"):
    headers=auth_header(client,role,email)
    user=client.get("/api/v1/users/me",headers=headers).json()
    response=client.post("/api/v1/providers/me/profile",headers=headers,json={
        "provider_type":role,"specialty":"Community health","license_number":"TEST-LIC-200",
        "city":"Abuja","gender":"female","professional_title":"Registered Nurse",
        "qualifications":"RN","languages":"English, Hausa","years_experience":5,
        "service_radius_km":20,"offers_home_visits":role=="nurse","consultation_modes":"home visit, chat"
    })
    assert response.status_code==201,response.text
    with TestingSessionLocal() as db:
        profile=db.scalar(select(ProviderProfile).where(ProviderProfile.user_id==user["id"]))
        profile.verification_status=VerificationStatus.VERIFIED;db.commit()
    return headers,user

def test_verified_review_and_quality(client):
    patient=auth_header(client,"patient","quality-patient@carelink.example.com")
    provider,user=make_verified_provider(client)
    scheduled=(datetime.now(timezone.utc)+timedelta(hours=2)).isoformat()
    ap=client.post("/api/v1/care/appointments",headers=patient,json={"provider_id":user["id"],"scheduled_at":scheduled,"reason":"Care review test"})
    assert ap.status_code==201,ap.text
    ap_id=ap.json()["id"]
    with TestingSessionLocal() as db:
        row=db.get(Appointment,ap_id);row.status=AppointmentStatus.COMPLETED;db.commit()
    review=client.post("/api/v1/quality/reviews",headers=patient,json={"appointment_id":ap_id,"rating":5,"communication":5,"punctuality":4,"professionalism":5,"respect":5,"clarity":5,"comment":"Clear and respectful."})
    assert review.status_code==201,review.text
    duplicate=client.post("/api/v1/quality/reviews",headers=patient,json={"appointment_id":ap_id,"rating":4})
    assert duplicate.status_code==409
    q=client.get(f"/api/v1/quality/providers/{user['id']}",headers=patient)
    assert q.status_code==200
    assert q.json()["average_rating"]==5.0
    assert q.json()["cases_completed"]==1

def test_nurse_checkin_record_checkout(client):
    patient=auth_header(client,"patient","visit-patient@carelink.example.com")
    nurse,user=make_verified_provider(client,"nurse","visit-nurse@carelink.example.com")
    visit=client.post("/api/v1/care/home-visits",headers=patient,json={"provider_id":user["id"],"address":"Central Area, Abuja","reason":"Home nursing follow-up"})
    assert visit.status_code==201,visit.text
    visit_id=visit.json()["id"]
    accepted=client.patch(f"/api/v1/providers/home-visits/{visit_id}/status",headers=nurse,json={"status":"accepted"})
    assert accepted.status_code==200
    checkin=client.post(f"/api/v1/nurses/home-visits/{visit_id}/check-in",headers=nurse)
    assert checkin.status_code==200,checkin.text
    record=client.put(f"/api/v1/nurses/home-visits/{visit_id}/care-record",headers=nurse,json={"vitals":"BP recorded","observations":"Patient alert","interventions":"Routine nursing care","escalation_required":False})
    assert record.status_code==200,record.text
    checkout=client.post(f"/api/v1/nurses/home-visits/{visit_id}/check-out",headers=nurse)
    assert checkout.status_code==200,checkout.text
    assert checkout.json()["status"]=="completed"
