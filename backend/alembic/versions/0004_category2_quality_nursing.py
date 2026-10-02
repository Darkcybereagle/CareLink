"""category 2 provider quality and nursing operations

Revision ID: 0004
Revises: 0003
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision="0004"
down_revision="0003"
branch_labels=None
depends_on=None

def upgrade():
    bind=op.get_bind()
    op.execute("ALTER TYPE home_visit_status ADD VALUE IF NOT EXISTS 'IN_PROGRESS'")
    visit_check=postgresql.ENUM("NOT_STARTED","CHECKED_IN","CHECKED_OUT",name="visit_check_status",create_type=False)
    complaint=postgresql.ENUM("OPEN","REVIEWING","RESOLVED","DISMISSED",name="complaint_status",create_type=False)
    visit_check.create(bind,checkfirst=True); complaint.create(bind,checkfirst=True)

    for name,typ in [
        ("gender",sa.String(30)),("date_of_birth",sa.Date()),("professional_title",sa.String(120)),
        ("qualifications",sa.Text()),("languages",sa.String(255)),("years_experience",sa.Integer()),
        ("service_radius_km",sa.Integer()),("consultation_modes",sa.String(120))
    ]: op.add_column("provider_profiles",sa.Column(name,typ,nullable=True))
    op.add_column("provider_profiles",sa.Column("offers_home_visits",sa.Boolean(),nullable=False,server_default=sa.false()))

    op.add_column("home_visit_requests",sa.Column("check_status",visit_check,nullable=False,server_default="NOT_STARTED"))
    op.add_column("home_visit_requests",sa.Column("checked_in_at",sa.DateTime(timezone=True)))
    op.add_column("home_visit_requests",sa.Column("checked_out_at",sa.DateTime(timezone=True)))
    op.add_column("home_visit_requests",sa.Column("care_notes",sa.Text()))
    op.add_column("home_visit_requests",sa.Column("observations",sa.Text()))
    op.add_column("home_visit_requests",sa.Column("escalation_note",sa.Text()))

    op.create_unique_constraint("uq_message_thread_participants","message_threads",["patient_id","provider_id"])

    op.create_table("provider_reviews",
        sa.Column("id",sa.Integer(),primary_key=True),
        sa.Column("patient_id",sa.Integer(),sa.ForeignKey("users.id",ondelete="CASCADE"),nullable=False),
        sa.Column("provider_id",sa.Integer(),sa.ForeignKey("users.id",ondelete="CASCADE"),nullable=False),
        sa.Column("appointment_id",sa.Integer(),sa.ForeignKey("appointments.id",ondelete="CASCADE"),nullable=False),
        sa.Column("rating",sa.Integer(),nullable=False),sa.Column("communication",sa.Integer()),sa.Column("punctuality",sa.Integer()),
        sa.Column("professionalism",sa.Integer()),sa.Column("respect",sa.Integer()),sa.Column("clarity",sa.Integer()),
        sa.Column("comment",sa.Text()),sa.Column("created_at",sa.DateTime(timezone=True),nullable=False),
        sa.UniqueConstraint("patient_id","appointment_id",name="uq_review_patient_appointment"))
    for c in ("patient_id","provider_id","appointment_id"): op.create_index(f"ix_provider_reviews_{c}","provider_reviews",[c])

    op.create_table("provider_complaints",
        sa.Column("id",sa.Integer(),primary_key=True),
        sa.Column("patient_id",sa.Integer(),sa.ForeignKey("users.id",ondelete="CASCADE"),nullable=False),
        sa.Column("provider_id",sa.Integer(),sa.ForeignKey("users.id",ondelete="CASCADE"),nullable=False),
        sa.Column("appointment_id",sa.Integer(),sa.ForeignKey("appointments.id",ondelete="SET NULL")),
        sa.Column("category",sa.String(80),nullable=False),sa.Column("description",sa.Text(),nullable=False),
        sa.Column("status",complaint,nullable=False,server_default="OPEN"),sa.Column("created_at",sa.DateTime(timezone=True),nullable=False))
    for c in ("patient_id","provider_id","appointment_id"): op.create_index(f"ix_provider_complaints_{c}","provider_complaints",[c])

    op.create_table("nurse_care_records",
        sa.Column("id",sa.Integer(),primary_key=True),
        sa.Column("home_visit_id",sa.Integer(),sa.ForeignKey("home_visit_requests.id",ondelete="CASCADE"),nullable=False,unique=True),
        sa.Column("nurse_id",sa.Integer(),sa.ForeignKey("users.id",ondelete="CASCADE"),nullable=False),
        sa.Column("patient_id",sa.Integer(),sa.ForeignKey("users.id",ondelete="CASCADE"),nullable=False),
        sa.Column("vitals",sa.Text()),sa.Column("observations",sa.Text()),sa.Column("interventions",sa.Text()),
        sa.Column("escalation_required",sa.Boolean(),nullable=False,server_default=sa.false()),sa.Column("escalation_note",sa.Text()),
        sa.Column("created_at",sa.DateTime(timezone=True),nullable=False),sa.Column("updated_at",sa.DateTime(timezone=True),nullable=False))
    for c in ("home_visit_id","nurse_id","patient_id"): op.create_index(f"ix_nurse_care_records_{c}","nurse_care_records",[c],unique=(c=="home_visit_id"))

def downgrade():
    for table in ("nurse_care_records","provider_complaints","provider_reviews"): op.drop_table(table)
    op.drop_constraint("uq_message_thread_participants","message_threads",type_="unique")
    for c in ("escalation_note","observations","care_notes","checked_out_at","checked_in_at","check_status"): op.drop_column("home_visit_requests",c)
    for c in ("offers_home_visits","consultation_modes","service_radius_km","years_experience","languages","qualifications","professional_title","date_of_birth","gender"): op.drop_column("provider_profiles",c)
    bind=op.get_bind()
    postgresql.ENUM(name="complaint_status").drop(bind,checkfirst=True)
    postgresql.ENUM(name="visit_check_status").drop(bind,checkfirst=True)
