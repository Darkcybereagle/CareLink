"""create users table

Revision ID: 0001_create_users
Revises:
Create Date: 2026-09-11
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM


revision: str = "0001_create_users"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


user_role = ENUM(
    "PATIENT",
    "DOCTOR",
    "NURSE",
    "HOSPITAL",
    "ADMIN",
    name="user_role",
    create_type=False,
)


def upgrade() -> None:
    bind = op.get_bind()

    user_role.create(bind, checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

    op.create_index(
        "ix_users_email",
        "users",
        ["email"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")

    bind = op.get_bind()
    user_role.drop(bind, checkfirst=True)