"""record_type

Revision ID: 9f508f95f76f
Revises: 8197163581a2
Create Date: 2025-05-19 03:25:57.294205

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9f508f95f76f"
down_revision: Union[str, None] = "8197163581a2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "record_type",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.add_column(
        "category", sa.Column("record_type_id", sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        None, "category", "record_type", ["record_type_id"], ["id"]
    )
    op.alter_column('record', 'price', new_column_name='amount', existing_type=sa.Float(), nullable=False)

    op.add_column(
        "record", sa.Column("record_type_id", sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        None, "record", "record_type", ["record_type_id"], ["id"]
    )
    op.add_column(
        "tag", sa.Column("record_type_id", sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        None, "tag", "record_type", ["record_type_id"], ["id"]
    )
    op.bulk_insert(
        sa.table('record_type', sa.Column('name')),
        [{'name': 'expense'}, {'name': 'income'}]
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "tag", type_="foreignkey")
    op.drop_column("tag", "record_type_id")
    op.add_column(
        "record",
        sa.Column(
            "price",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_constraint(None, "record", type_="foreignkey")
    op.drop_column("record", "record_type_id")
    op.drop_column("record", "amount")
    op.drop_constraint(None, "category", type_="foreignkey")
    op.drop_column("category", "record_type_id")
    op.drop_table("record_type")
    # ### end Alembic commands ###
