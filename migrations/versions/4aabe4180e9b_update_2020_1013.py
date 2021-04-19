"""update 2020-1013

Revision ID: 4aabe4180e9b
Revises: 3042be41091b
Create Date: 2020-10-13 17:36:43.488222

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4aabe4180e9b'
down_revision = '3042be41091b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('manufacturers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True, comment='厂商名称'),
    sa.Column('status', sa.Integer(), nullable=True, comment='厂商状态，0删除，1正常'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('manufacturers', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_manufacturers_status'), ['status'], unique=False)

    op.create_table('equipments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('eq_code', sa.String(length=64), nullable=True, comment='设备编码'),
    sa.Column('eq_name', sa.String(length=64), nullable=True, comment='设备名称'),
    sa.Column('eq_desc', sa.String(length=64), nullable=True, comment='设备描述'),
    sa.Column('eq_type', sa.Integer(), nullable=True, comment='设备类型，0其它，1手机，2pad'),
    sa.Column('eq_sys', sa.Integer(), nullable=True, comment='设备系统，0其它，1ios，2android'),
    sa.Column('eq_sys_ver', sa.String(length=16), nullable=True, comment='设备系统版本'),
    sa.Column('eq_owner', sa.String(length=16), nullable=True, comment='设备管理者'),
    sa.Column('borrower', sa.String(length=16), nullable=True, comment='借用者姓名'),
    sa.Column('have_sim', sa.Integer(), nullable=True, comment='是否有sim卡，0没有，1有'),
    sa.Column('eq_status', sa.Integer(), nullable=True, comment='设备状态，0停用，1可外借，2已外借'),
    sa.Column('status', sa.Integer(), nullable=True, comment='设备是否删除，0删除，1正常'),
    sa.Column('mf_id', sa.Integer(), nullable=True, comment='设备厂商'),
    sa.ForeignKeyConstraint(['mf_id'], ['manufacturers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('equipments', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_equipments_eq_code'), ['eq_code'], unique=False)
        batch_op.create_index(batch_op.f('ix_equipments_eq_status'), ['eq_status'], unique=False)
        batch_op.create_index(batch_op.f('ix_equipments_status'), ['status'], unique=False)

    op.create_table('equipment_log',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('eq_code', sa.String(length=64), nullable=True, comment='设备编码'),
    sa.Column('eq_name', sa.String(length=64), nullable=True, comment='设备名称'),
    sa.Column('eq_desc', sa.String(length=64), nullable=True, comment='设备描述'),
    sa.Column('eq_type', sa.Integer(), nullable=True, comment='设备类型，0其它，1手机，2pad'),
    sa.Column('eq_sys', sa.Integer(), nullable=True, comment='设备系统，0其它，1ios，2android'),
    sa.Column('eq_sys_ver', sa.String(length=16), nullable=True, comment='设备系统版本'),
    sa.Column('eq_owner', sa.String(length=16), nullable=True, comment='设备管理者'),
    sa.Column('borrower', sa.String(length=16), nullable=True, comment='借用者姓名'),
    sa.Column('have_sim', sa.Integer(), nullable=True, comment='是否有sim卡，0没有，1有'),
    sa.Column('status', sa.Integer(), nullable=True, comment='设备状态，0停用，1启用，2编辑，3归还，4外借，5删除'),
    sa.Column('mf_id', sa.Integer(), nullable=True, comment='设备厂商'),
    sa.Column('eq_id', sa.Integer(), nullable=True, comment='设备ID'),
    sa.Column('c_uid', sa.Integer(), nullable=True, comment='log创建者'),
    sa.ForeignKeyConstraint(['c_uid'], ['users.id'], ),
    sa.ForeignKeyConstraint(['eq_id'], ['equipments.id'], ),
    sa.ForeignKeyConstraint(['mf_id'], ['manufacturers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('equipment_log')
    with op.batch_alter_table('equipments', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_equipments_status'))
        batch_op.drop_index(batch_op.f('ix_equipments_eq_status'))
        batch_op.drop_index(batch_op.f('ix_equipments_eq_code'))

    op.drop_table('equipments')
    with op.batch_alter_table('manufacturers', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_manufacturers_status'))

    op.drop_table('manufacturers')
    # ### end Alembic commands ###