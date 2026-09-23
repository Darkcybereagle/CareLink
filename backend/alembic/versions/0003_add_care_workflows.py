"""add patient and provider care workflows

Revision ID: 0003
Revises: 0002
"""
from alembic import op
import sqlalchemy as sa

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    user_role = sa.Enum("patient", "doctor", "nurse", "hospital", "admin", name="user_role")
    verification_status = sa.Enum("pending", "verified", "rejected", name="verification_status")
    appointment_status = sa.Enum("requested", "confirmed", "completed", "cancelled", name="appointment_status")
    home_visit_status = sa.Enum("requested", "accepted", "completed", "cancelled", name="home_visit_status")

    bind = op.get_bind()
    user_role.create(bind, checkfirst=True)
    verification_status.create(bind, checkfirst=True)
    appointment_status.create(bind, checkfirst=True)
    home_visit_status.create(bind, checkfirst=True)

    op.create_table(
        "provider_profiles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False),
        sa.Column("provider_type", sa.String(30), nullable=False),
        sa.Column("specialty", sa.String(120)),
        sa.Column("license_number", sa.String(120)),
        sa.Column("phone", sa.String(30)),
        sa.Column("facility_name", sa.String(160)),
        sa.Column("city", sa.String(80)),
        sa.Column("bio", sa.Text()),
        sa.Column("verification_status", verification_status, nullable=False, server_default="pending"),
        sa.Column("is_available", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_index("ix_provider_profiles_user_id", "provider_profiles", ["user_id"], unique=True)

    op.create_table(
        "provider_availability",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("provider_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("day_of_week", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.Time(), nullable=False),
        sa.Column("end_time", sa.Time(), nullable=False),
    )
    op.create_index("ix_provider_availability_provider_id", "provider_availability", ["provider_id"])

    op.create_table(
        "hospitals",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(160), nullable=False),
        sa.Column("address", sa.String(255), nullable=False),
        sa.Column("city", sa.String(80), nullable=False),
        sa.Column("phone", sa.String(30)),
        sa.Column("services", sa.Text()),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_index("ix_hospitals_city", "hospitals", ["city"])

    op.create_table(
        "appointments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("patient_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("provider_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("status", appointment_status, nullable=False, server_default="requested"),
        sa.Column("notes", sa.Text()),
    )
    op.create_index("ix_appointments_patient_id", "appointments", ["patient_id"])
    op.create_index("ix_appointments_provider_id", "appointments", ["provider_id"])

    op.create_table(
        "home_visit_requests",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("patient_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("provider_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("address", sa.String(255), nullable=False),
        sa.Column("requested_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("status", home_visit_status, nullable=False, server_default="requested"),
    )
    op.create_index("ix_home_visit_requests_patient_id", "home_visit_requests", ["patient_id"])
    op.create_index("ix_home_visit_requests_provider_id", "home_visit_requests", ["provider_id"])

    op.create_table(
        "ai_intakes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("patient_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("symptoms", sa.Text(), nullable=False),
        sa.Column("duration", sa.String(120)),
        sa.Column("urgency", sa.String(20), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("clinician_handoff", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_ai_intakes_patient_id", "ai_intakes", ["patient_id"])

    op.create_table(
        "message_threads",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("patient_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("provider_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "messages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("thread_id", sa.Integer(), sa.ForeignKey("message_threads.id", ondelete="CASCADE"), nullable=False),
        sa.Column("sender_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_messages_thread_id", "messages", ["thread_id"])

    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(160), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("is_read", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_notifications_user_id", "notifications", ["user_id"])

    op.create_table(
        "follow_ups",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("patient_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("provider_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("note", sa.Text(), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.create_index("ix_follow_ups_patient_id", "follow_ups", ["patient_id"])
    op.create_index("ix_follow_ups_provider_id", "follow_ups", ["provider_id"])


def downgrade() -> None:
    for table in [
        "follow_ups", "notifications", "messages", "message_threads",
        "ai_intakes", "home_visit_requests", "appointments", "hospitals",
        "provider_availability", "provider_profiles"
    ]:
        op.drop_table(table)

    bind = op.get_bind()
    sa.Enum(name="home_visit_status").drop(bind, checkfirst=True)
    sa.Enum(name="appointment_status").drop(bind, checkfirst=True)
    sa.Enum(name="verification_status").drop(bind, checkfirst=True)
