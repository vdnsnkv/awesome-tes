"""init

Revision ID: d1c7970fbb13
Revises: 
Create Date: 2022-10-08 20:25:27.410323

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "d1c7970fbb13"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "public_id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text(
                "md5(random()::text || clock_timestamp()::text)::uuid"
            ),
            nullable=False,
        ),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("bcrypt_hash", sa.LargeBinary(), nullable=False),
        sa.Column("role", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("meta", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade():
    op.drop_table("user")
