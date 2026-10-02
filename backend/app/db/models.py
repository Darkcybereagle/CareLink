from datetime import date, datetime, time, timezone
from enum import Enum
from sqlalchemy import Boolean, Date, DateTime, Enum as SQLEnum, Float, ForeignKey, Integer, String, Text, Time, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

class UserRole(str, Enum):
    PATIENT="patient"; DOCTOR="doctor"; NURSE="nurse"; HOSPITAL="hospital"; ADMIN="admin"
class VerificationStatus(str, Enum):
    PENDING="pending"; VERIFIED="verified"; REJECTED="rejected"
class AppointmentStatus(str, Enum):
    REQUESTED="requested"; CONFIRMED="confirmed"; COMPLETED="completed"; CANCELLED="cancelled"
class HomeVisitStatus(str, Enum):
    REQUESTED="requested"; ACCEPTED="accepted"; IN_PROGRESS="in_progress"; COMPLETED="completed"; CANCELLED="cancelled"
class VisitCheckStatus(str, Enum):
    NOT_STARTED="not_started"; CHECKED_IN="checked_in"; CHECKED_OUT="checked_out"
class ComplaintStatus(str, Enum):
    OPEN="open"; REVIEWING="reviewing"; RESOLVED="resolved"; DISMISSED="dismissed"

class User(Base):
    __tablename__="users"
    id: Mapped[int]=mapped_column(primary_key=True)
    full_name: Mapped[str]=mapped_column(String(120),nullable=False)
    email: Mapped[str]=mapped_column(String(255),unique=True,index=True,nullable=False)
    password_hash: Mapped[str]=mapped_column(String(255),nullable=False)
    role: Mapped[UserRole]=mapped_column(SQLEnum(UserRole,name="user_role"),default=UserRole.PATIENT,nullable=False)
    is_active: Mapped[bool]=mapped_column(Boolean,default=True,nullable=False)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc),nullable=False)
    patient_profile: Mapped["PatientProfile | None"]=relationship(back_populates="user",uselist=False,cascade="all, delete-orphan")
    provider_profile: Mapped["ProviderProfile | None"]=relationship(back_populates="user",uselist=False,cascade="all, delete-orphan")

class PatientProfile(Base):
    __tablename__="patient_profiles"
    id: Mapped[int]=mapped_column(primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),unique=True,nullable=False,index=True)
    phone: Mapped[str|None]=mapped_column(String(30))
    date_of_birth: Mapped[date|None]=mapped_column(Date)
    gender: Mapped[str|None]=mapped_column(String(30))
    address: Mapped[str|None]=mapped_column(String(255))
    emergency_contact_name: Mapped[str|None]=mapped_column(String(120))
    emergency_contact_phone: Mapped[str|None]=mapped_column(String(30))
    user: Mapped["User"]=relationship(back_populates="patient_profile")

class ProviderProfile(Base):
    __tablename__="provider_profiles"
    id: Mapped[int]=mapped_column(primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),unique=True,nullable=False,index=True)
    provider_type: Mapped[str]=mapped_column(String(30),nullable=False)
    specialty: Mapped[str|None]=mapped_column(String(120))
    license_number: Mapped[str|None]=mapped_column(String(120))
    phone: Mapped[str|None]=mapped_column(String(30))
    facility_name: Mapped[str|None]=mapped_column(String(160))
    city: Mapped[str|None]=mapped_column(String(80))
    bio: Mapped[str|None]=mapped_column(Text)
    gender: Mapped[str|None]=mapped_column(String(30))
    date_of_birth: Mapped[date|None]=mapped_column(Date)
    professional_title: Mapped[str|None]=mapped_column(String(120))
    photo_url: Mapped[str|None]=mapped_column(String(500))
    qualifications: Mapped[str|None]=mapped_column(Text)
    languages: Mapped[str|None]=mapped_column(String(255))
    years_experience: Mapped[int|None]=mapped_column(Integer)
    service_radius_km: Mapped[int|None]=mapped_column(Integer)
    offers_home_visits: Mapped[bool]=mapped_column(Boolean,default=False,nullable=False)
    consultation_modes: Mapped[str|None]=mapped_column(String(120))
    verification_status: Mapped[VerificationStatus]=mapped_column(SQLEnum(VerificationStatus,name="verification_status"),default=VerificationStatus.PENDING,nullable=False)
    is_available: Mapped[bool]=mapped_column(Boolean,default=True,nullable=False)
    user: Mapped["User"]=relationship(back_populates="provider_profile")

class ProviderAvailability(Base):
    __tablename__="provider_availability"
    id: Mapped[int]=mapped_column(primary_key=True)
    provider_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),nullable=False,index=True)
    day_of_week: Mapped[int]=mapped_column(Integer,nullable=False)
    start_time: Mapped[time]=mapped_column(Time,nullable=False)
    end_time: Mapped[time]=mapped_column(Time,nullable=False)

class Hospital(Base):
    __tablename__="hospitals"
    id: Mapped[int]=mapped_column(primary_key=True); name: Mapped[str]=mapped_column(String(160),nullable=False)
    address: Mapped[str]=mapped_column(String(255),nullable=False); city: Mapped[str]=mapped_column(String(80),nullable=False,index=True)
    phone: Mapped[str|None]=mapped_column(String(30)); services: Mapped[str|None]=mapped_column(Text)
    is_active: Mapped[bool]=mapped_column(Boolean,default=True,nullable=False)

class Appointment(Base):
    __tablename__="appointments"
    id: Mapped[int]=mapped_column(primary_key=True); patient_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),nullable=False,index=True)
    provider_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),nullable=False,index=True)
    scheduled_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),nullable=False); reason: Mapped[str]=mapped_column(Text,nullable=False)
    status: Mapped[AppointmentStatus]=mapped_column(SQLEnum(AppointmentStatus,name="appointment_status"),default=AppointmentStatus.REQUESTED,nullable=False)
    notes: Mapped[str|None]=mapped_column(Text)

class HomeVisitRequest(Base):
    __tablename__="home_visit_requests"
    id: Mapped[int]=mapped_column(primary_key=True); patient_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),nullable=False,index=True)
    provider_id: Mapped[int|None]=mapped_column(ForeignKey("users.id",ondelete="SET NULL"),index=True)
    address: Mapped[str]=mapped_column(String(255),nullable=False); requested_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc),nullable=False)
    reason: Mapped[str]=mapped_column(Text,nullable=False)
    status: Mapped[HomeVisitStatus]=mapped_column(SQLEnum(HomeVisitStatus,name="home_visit_status"),default=HomeVisitStatus.REQUESTED,nullable=False)
    check_status: Mapped[VisitCheckStatus]=mapped_column(SQLEnum(VisitCheckStatus,name="visit_check_status"),default=VisitCheckStatus.NOT_STARTED,nullable=False)
    checked_in_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True)); checked_out_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
    care_notes: Mapped[str|None]=mapped_column(Text); observations: Mapped[str|None]=mapped_column(Text); escalation_note: Mapped[str|None]=mapped_column(Text)

class AIIntake(Base):
    __tablename__="ai_intakes"
    id: Mapped[int]=mapped_column(primary_key=True); patient_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),nullable=False,index=True)
    symptoms: Mapped[str]=mapped_column(Text,nullable=False); duration: Mapped[str|None]=mapped_column(String(120)); urgency: Mapped[str]=mapped_column(String(20),nullable=False)
    summary: Mapped[str]=mapped_column(Text,nullable=False); clinician_handoff: Mapped[str]=mapped_column(Text,nullable=False)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc),nullable=False)

class MessageThread(Base):
    __tablename__="message_threads"; __table_args__=(UniqueConstraint("patient_id","provider_id",name="uq_message_thread_participants"),)
    id: Mapped[int]=mapped_column(primary_key=True); patient_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),nullable=False,index=True)
    provider_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),nullable=False,index=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc),nullable=False)

class Message(Base):
    __tablename__="messages"
    id: Mapped[int]=mapped_column(primary_key=True); thread_id: Mapped[int]=mapped_column(ForeignKey("message_threads.id",ondelete="CASCADE"),nullable=False,index=True)
    sender_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),nullable=False); body: Mapped[str]=mapped_column(Text,nullable=False)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc),nullable=False)

class Notification(Base):
    __tablename__="notifications"
    id: Mapped[int]=mapped_column(primary_key=True); user_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),nullable=False,index=True)
    title: Mapped[str]=mapped_column(String(160),nullable=False); body: Mapped[str]=mapped_column(Text,nullable=False)
    is_read: Mapped[bool]=mapped_column(Boolean,default=False,nullable=False); created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc),nullable=False)

class FollowUp(Base):
    __tablename__="follow_ups"
    id: Mapped[int]=mapped_column(primary_key=True); patient_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),nullable=False,index=True)
    provider_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),nullable=False,index=True)
    scheduled_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),nullable=False); note: Mapped[str]=mapped_column(Text,nullable=False)
    completed: Mapped[bool]=mapped_column(Boolean,default=False,nullable=False)

class ProviderReview(Base):
    __tablename__="provider_reviews"; __table_args__=(UniqueConstraint("patient_id","appointment_id",name="uq_review_patient_appointment"),)
    id: Mapped[int]=mapped_column(primary_key=True); patient_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),nullable=False,index=True)
    provider_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),nullable=False,index=True)
    appointment_id: Mapped[int]=mapped_column(ForeignKey("appointments.id",ondelete="CASCADE"),nullable=False,index=True)
    rating: Mapped[int]=mapped_column(Integer,nullable=False); communication: Mapped[int|None]=mapped_column(Integer); punctuality: Mapped[int|None]=mapped_column(Integer)
    professionalism: Mapped[int|None]=mapped_column(Integer); respect: Mapped[int|None]=mapped_column(Integer); clarity: Mapped[int|None]=mapped_column(Integer)
    comment: Mapped[str|None]=mapped_column(Text); created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc),nullable=False)

class ProviderComplaint(Base):
    __tablename__="provider_complaints"
    id: Mapped[int]=mapped_column(primary_key=True); patient_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),nullable=False,index=True)
    provider_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),nullable=False,index=True)
    appointment_id: Mapped[int|None]=mapped_column(ForeignKey("appointments.id",ondelete="SET NULL"),index=True)
    category: Mapped[str]=mapped_column(String(80),nullable=False); description: Mapped[str]=mapped_column(Text,nullable=False)
    status: Mapped[ComplaintStatus]=mapped_column(SQLEnum(ComplaintStatus,name="complaint_status"),default=ComplaintStatus.OPEN,nullable=False)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc),nullable=False)

class NurseCareRecord(Base):
    __tablename__="nurse_care_records"
    id: Mapped[int]=mapped_column(primary_key=True); home_visit_id: Mapped[int]=mapped_column(ForeignKey("home_visit_requests.id",ondelete="CASCADE"),unique=True,nullable=False,index=True)
    nurse_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),nullable=False,index=True)
    patient_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),nullable=False,index=True)
    vitals: Mapped[str|None]=mapped_column(Text); observations: Mapped[str|None]=mapped_column(Text); interventions: Mapped[str|None]=mapped_column(Text)
    escalation_required: Mapped[bool]=mapped_column(Boolean,default=False,nullable=False); escalation_note: Mapped[str|None]=mapped_column(Text)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc),nullable=False)
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc),onupdate=lambda:datetime.now(timezone.utc),nullable=False)
