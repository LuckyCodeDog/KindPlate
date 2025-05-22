"""add water_usage to MenuItemIngredients

Revision ID: add_water_usage_to_menu_item_ingredients
Revises: 
Create Date: 2024-03-21

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_water_usage_to_menu_item_ingredients'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # 添加 water_usage 列
    op.add_column('MenuItemIngredients',
        sa.Column('water_usage', sa.Numeric(10, 2), nullable=False, server_default='0')
    )

def downgrade():
    # 删除 water_usage 列
    op.drop_column('MenuItemIngredients', 'water_usage') 