"""AosrMaterial: deleted several nullable attrs from columns

Revision ID: 1cbb47a7b9f3
Revises: 4d2d93f51e8b
Create Date: 2025-04-04 10:12:08.396758

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1cbb47a7b9f3'
down_revision: Union[str, None] = '4d2d93f51e8b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('aosrmaterials', 'aosr_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('aosrmaterials', 'section_material_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('aosrmaterials', 'section_material_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('aosrmaterials', 'aosr_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
