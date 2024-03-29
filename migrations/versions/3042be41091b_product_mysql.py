"""product mysql

Revision ID: 3042be41091b
Revises: 
Create Date: 2020-06-11 13:08:37.402913

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3042be41091b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('default', sa.Boolean(), nullable=True),
    sa.Column('permissions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=32), nullable=True),
    sa.Column('password', sa.String(length=256), nullable=True),
    sa.Column('user_email', sa.String(length=64), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('mocks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mock_name', sa.String(length=64), nullable=True),
    sa.Column('mock_desc', sa.String(length=64), nullable=True),
    sa.Column('method', sa.String(length=16), nullable=True),
    sa.Column('path', sa.String(length=256), nullable=True),
    sa.Column('params', sa.String(length=256), nullable=True),
    sa.Column('header', sa.String(length=256), nullable=True),
    sa.Column('response', sa.String(length=256), nullable=True),
    sa.Column('res_type', sa.String(length=16), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('run_status', sa.Integer(), nullable=True),
    sa.Column('check_params', sa.Integer(), nullable=True),
    sa.Column('check_header', sa.Integer(), nullable=True),
    sa.Column('c_uid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['c_uid'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('projects',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('project_name', sa.String(length=64), nullable=True),
    sa.Column('project_desc', sa.String(length=64), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('c_uid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['c_uid'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('environments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('env_name', sa.String(length=64), nullable=True),
    sa.Column('desc', sa.String(length=64), nullable=True),
    sa.Column('url', sa.String(length=256), nullable=True),
    sa.Column('use_db', sa.Boolean(), nullable=True),
    sa.Column('db_host', sa.String(length=256), nullable=True),
    sa.Column('db_port', sa.String(length=16), nullable=True),
    sa.Column('db_user', sa.String(length=64), nullable=True),
    sa.Column('db_pass', sa.String(length=64), nullable=True),
    sa.Column('database', sa.String(length=64), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('c_uid', sa.Integer(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['c_uid'], ['users.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('models',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('model_name', sa.String(length=64), nullable=True),
    sa.Column('model_desc', sa.String(length=64), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('c_uid', sa.Integer(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['c_uid'], ['users.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('interfaces',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('Interface_name', sa.String(length=64), nullable=True),
    sa.Column('Interface_desc', sa.String(length=64), nullable=True),
    sa.Column('interface_type', sa.String(length=16), nullable=True),
    sa.Column('method', sa.String(length=16), nullable=True),
    sa.Column('path', sa.String(length=256), nullable=True),
    sa.Column('header', sa.String(length=256), nullable=True),
    sa.Column('params', sa.String(length=256), nullable=True),
    sa.Column('response', sa.String(length=256), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('c_uid', sa.Integer(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('model_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['c_uid'], ['users.id'], ),
    sa.ForeignKeyConstraint(['model_id'], ['models.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_name', sa.String(length=64), nullable=True),
    sa.Column('task_type', sa.Integer(), nullable=True),
    sa.Column('run_time', sa.String(length=256), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('report_to', sa.String(length=256), nullable=True),
    sa.Column('report_copy', sa.String(length=256), nullable=True),
    sa.Column('task_make_email', sa.String(length=256), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('run_status', sa.Integer(), nullable=True),
    sa.Column('c_uid', sa.Integer(), nullable=True),
    sa.Column('s_uid', sa.Integer(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('env_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['c_uid'], ['users.id'], ),
    sa.ForeignKeyConstraint(['env_id'], ['environments.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('parameters',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('param_name', sa.String(length=64), nullable=True),
    sa.Column('param_desc', sa.String(length=64), nullable=True),
    sa.Column('param_type', sa.String(length=16), nullable=True),
    sa.Column('necessary', sa.Boolean(), nullable=True),
    sa.Column('default', sa.String(length=64), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('c_uid', sa.Integer(), nullable=True),
    sa.Column('interface_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['c_uid'], ['users.id'], ),
    sa.ForeignKeyConstraint(['interface_id'], ['interfaces.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('testcases',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('case_name', sa.String(length=64), nullable=True),
    sa.Column('case_desc', sa.String(length=64), nullable=True),
    sa.Column('case_type', sa.String(length=16), nullable=True),
    sa.Column('method', sa.String(length=16), nullable=True),
    sa.Column('path', sa.String(length=256), nullable=True),
    sa.Column('params', sa.String(length=256), nullable=True),
    sa.Column('header', sa.String(length=256), nullable=True),
    sa.Column('res_assert', sa.String(length=256), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('rely_params', sa.String(length=64), nullable=True),
    sa.Column('is_debug', sa.Boolean(), nullable=True),
    sa.Column('is_pass', sa.Boolean(), nullable=True),
    sa.Column('save_result', sa.Boolean(), nullable=True),
    sa.Column('use_db', sa.Boolean(), nullable=True),
    sa.Column('sql', sa.String(length=256), nullable=True),
    sa.Column('field_value', sa.String(length=256), nullable=True),
    sa.Column('c_uid', sa.Integer(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('model_id', sa.Integer(), nullable=True),
    sa.Column('interface_id', sa.Integer(), nullable=True),
    sa.Column('env_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['c_uid'], ['users.id'], ),
    sa.ForeignKeyConstraint(['env_id'], ['environments.id'], ),
    sa.ForeignKeyConstraint(['interface_id'], ['interfaces.id'], ),
    sa.ForeignKeyConstraint(['model_id'], ['models.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('testresults',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('case_num', sa.Integer(), nullable=True),
    sa.Column('pass_num', sa.Integer(), nullable=True),
    sa.Column('fail_num', sa.Integer(), nullable=True),
    sa.Column('exception_num', sa.Integer(), nullable=True),
    sa.Column('not_expect_num', sa.Integer(), nullable=True),
    sa.Column('unknown_num', sa.Integer(), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('test_report', sa.String(length=64), nullable=True),
    sa.Column('test_log', sa.String(length=64), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('c_uid', sa.Integer(), nullable=True),
    sa.Column('projects_id', sa.Integer(), nullable=True),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['c_uid'], ['users.id'], ),
    sa.ForeignKeyConstraint(['projects_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('caseresults',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('case_type', sa.String(length=16), nullable=True),
    sa.Column('method', sa.String(length=16), nullable=True),
    sa.Column('path', sa.String(length=256), nullable=True),
    sa.Column('params', sa.String(length=256), nullable=True),
    sa.Column('header', sa.String(length=256), nullable=True),
    sa.Column('res_assert', sa.String(length=256), nullable=True),
    sa.Column('result', sa.Boolean(), nullable=True),
    sa.Column('case_result', sa.Integer(), nullable=True),
    sa.Column('response', sa.String(length=256), nullable=True),
    sa.Column('diff_res', sa.String(length=256), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('case_id', sa.Integer(), nullable=True),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.Column('environment', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['case_id'], ['testcases.id'], ),
    sa.ForeignKeyConstraint(['environment'], ['environments.id'], ),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('registrations',
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.Column('case_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['case_id'], ['testcases.id'], ),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], )
    )
    op.create_table('relycases',
    sa.Column('case_id', sa.Integer(), nullable=True),
    sa.Column('rely_case_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['case_id'], ['testcases.id'], ),
    sa.ForeignKeyConstraint(['rely_case_id'], ['testcases.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('relycases')
    op.drop_table('registrations')
    op.drop_table('caseresults')
    op.drop_table('testresults')
    op.drop_table('testcases')
    op.drop_table('parameters')
    op.drop_table('tasks')
    op.drop_table('interfaces')
    op.drop_table('models')
    op.drop_table('environments')
    op.drop_table('projects')
    op.drop_table('mocks')
    op.drop_table('users')
    op.drop_table('roles')
    # ### end Alembic commands ###
