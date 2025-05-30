"""Added index and aosr_name -> name

Revision ID: 50b73a64c8de
Revises: 445639b4bab2
Create Date: 2025-01-27 13:38:44.626955

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50b73a64c8de'
down_revision: Union[str, None] = '445639b4bab2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('aosr', sa.Column('name', sa.String(), nullable=False))
    op.create_index(op.f('ix_aosr_section_id'), 'aosr', ['section_id'], unique=False)
    op.drop_column('aosr', 'aosr_name')
    op.create_index(op.f('ix_aosrmaterial_aosr_id'), 'aosrmaterial', ['aosr_id'], unique=False)
    op.create_index(op.f('ix_aosrmaterial_material_id'), 'aosrmaterial', ['material_id'], unique=False)
    op.create_index(op.f('ix_sectionmaterial_material_id'), 'sectionmaterial', ['material_id'], unique=False)
    op.create_index(op.f('ix_sectionmaterial_section_id'), 'sectionmaterial', ['section_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_sectionmaterial_section_id'), table_name='sectionmaterial')
    op.drop_index(op.f('ix_sectionmaterial_material_id'), table_name='sectionmaterial')
    op.drop_index(op.f('ix_aosrmaterial_material_id'), table_name='aosrmaterial')
    op.drop_index(op.f('ix_aosrmaterial_aosr_id'), table_name='aosrmaterial')
    op.add_column('aosr', sa.Column('aosr_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_index(op.f('ix_aosr_section_id'), table_name='aosr')
    op.drop_column('aosr', 'name')
    # ### end Alembic commands ###
