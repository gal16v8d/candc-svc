"""Add target air unit and base defense field

Revision ID: 74147848bb10
Revises: 3caac7606c52
Create Date: 2023-12-03 22:21:50.085430

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '74147848bb10'
down_revision = '3caac7606c52'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('boat', schema=None) as batch_op:
        batch_op.add_column(sa.Column('target_air_unit', sa.Boolean(), nullable=True))

    with op.batch_alter_table('infantry', schema=None) as batch_op:
        batch_op.add_column(sa.Column('target_air_unit', sa.Boolean(), nullable=True))

    with op.batch_alter_table('plane', schema=None) as batch_op:
        batch_op.add_column(sa.Column('target_air_unit', sa.Boolean(), nullable=True))

    with op.batch_alter_table('structure', schema=None) as batch_op:
        batch_op.add_column(sa.Column('target_air_unit', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('base_defense', sa.Boolean(), nullable=True))

    with op.batch_alter_table('structurexfaction', schema=None) as batch_op:
        batch_op.alter_column('faction_id',
               existing_type=sa.BIGINT(),
               nullable=False)

    with op.batch_alter_table('tank', schema=None) as batch_op:
        batch_op.add_column(sa.Column('target_air_unit', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tank', schema=None) as batch_op:
        batch_op.drop_column('target_air_unit')

    with op.batch_alter_table('structurexfaction', schema=None) as batch_op:
        batch_op.alter_column('faction_id',
               existing_type=sa.BIGINT(),
               nullable=True)

    with op.batch_alter_table('structure', schema=None) as batch_op:
        batch_op.drop_column('base_defense')
        batch_op.drop_column('target_air_unit')

    with op.batch_alter_table('plane', schema=None) as batch_op:
        batch_op.drop_column('target_air_unit')

    with op.batch_alter_table('infantry', schema=None) as batch_op:
        batch_op.drop_column('target_air_unit')

    with op.batch_alter_table('boat', schema=None) as batch_op:
        batch_op.drop_column('target_air_unit')

    # ### end Alembic commands ###