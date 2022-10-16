"""add task.jira_id

Revision ID: 1d3663162ed5
Revises: fbc32cc2631b
Create Date: 2022-10-16 17:09:55.663602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1d3663162ed5"
down_revision = "fbc32cc2631b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("task", sa.Column("jira_id", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("task", "jira_id")
    # ### end Alembic commands ###