"""upgrade relationship between Forecasts and States

Revision ID: f27c4b581256
Revises: 8625dcfc68af
Create Date: 2024-12-07 20:22:22.393145

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f27c4b581256'
down_revision: Union[str, None] = '8625dcfc68af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
