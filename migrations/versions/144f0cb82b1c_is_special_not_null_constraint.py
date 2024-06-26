"""is_special not null constraint

Revision ID: 144f0cb82b1c
Revises: 8a6c21847fa6
Create Date: 2023-10-05 22:44:42.069741

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "144f0cb82b1c"
down_revision = "8a6c21847fa6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("boat", schema=None) as batch_op:
        batch_op.alter_column("is_special", existing_type=sa.BOOLEAN(), nullable=False)

    with op.batch_alter_table("infantry", schema=None) as batch_op:
        batch_op.alter_column("is_special", existing_type=sa.BOOLEAN(), nullable=False)

    with op.batch_alter_table("plane", schema=None) as batch_op:
        batch_op.alter_column("is_special", existing_type=sa.BOOLEAN(), nullable=False)

    with op.batch_alter_table("structure", schema=None) as batch_op:
        batch_op.alter_column("is_special", existing_type=sa.BOOLEAN(), nullable=False)

    with op.batch_alter_table("tank", schema=None) as batch_op:
        batch_op.alter_column("is_special", existing_type=sa.BOOLEAN(), nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("tank", schema=None) as batch_op:
        batch_op.alter_column("is_special", existing_type=sa.BOOLEAN(), nullable=True)

    with op.batch_alter_table("structure", schema=None) as batch_op:
        batch_op.alter_column("is_special", existing_type=sa.BOOLEAN(), nullable=True)

    with op.batch_alter_table("plane", schema=None) as batch_op:
        batch_op.alter_column("is_special", existing_type=sa.BOOLEAN(), nullable=True)

    with op.batch_alter_table("infantry", schema=None) as batch_op:
        batch_op.alter_column("is_special", existing_type=sa.BOOLEAN(), nullable=True)

    with op.batch_alter_table("boat", schema=None) as batch_op:
        batch_op.alter_column("is_special", existing_type=sa.BOOLEAN(), nullable=True)

    # ### end Alembic commands ###
