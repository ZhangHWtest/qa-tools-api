"""data2_text_type

Revision ID: ffe2123d32ee
Revises: 63a6e0d64feb
Create Date: 2020-10-30 16:42:56.310020

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ffe2123d32ee'
down_revision = '63a6e0d64feb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('caseresults', schema=None) as batch_op:
        batch_op.alter_column('diff_res',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.Text(),
               existing_nullable=True)
        batch_op.alter_column('header',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.Text(),
               existing_nullable=True)
        batch_op.alter_column('params',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.Text(),
               existing_nullable=True)
        batch_op.alter_column('path',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=255),
               existing_nullable=True)
        batch_op.alter_column('res_assert',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=255),
               existing_nullable=True)

    with op.batch_alter_table('environments', schema=None) as batch_op:
        batch_op.alter_column('db_host',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=255),
               existing_nullable=True)
        batch_op.alter_column('url',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=255),
               existing_nullable=True)

    with op.batch_alter_table('interfaces', schema=None) as batch_op:
        batch_op.alter_column('header',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.Text(),
               existing_nullable=True)
        batch_op.alter_column('params',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=255),
               existing_nullable=True)
        batch_op.alter_column('path',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=255),
               existing_nullable=True)
        batch_op.alter_column('response',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.Text(),
               existing_nullable=True)

    with op.batch_alter_table('mocks', schema=None) as batch_op:
        batch_op.alter_column('header',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.Text(),
               existing_nullable=True)
        batch_op.alter_column('params',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.Text(),
               existing_nullable=True)
        batch_op.alter_column('path',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=255),
               existing_nullable=True)

    with op.batch_alter_table('parameters', schema=None) as batch_op:
        batch_op.alter_column('default',
               existing_type=mysql.VARCHAR(length=64),
               type_=sa.String(length=255),
               existing_nullable=True)
        batch_op.alter_column('param_desc',
               existing_type=mysql.VARCHAR(length=64),
               type_=sa.Text(),
               existing_nullable=True)

    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.alter_column('report_copy',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=255),
               existing_nullable=True)
        batch_op.alter_column('report_to',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=255),
               existing_nullable=True)
        batch_op.alter_column('run_time',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=255),
               existing_nullable=True)
        batch_op.alter_column('task_make_email',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=255),
               existing_nullable=True)

    with op.batch_alter_table('testcases', schema=None) as batch_op:
        batch_op.alter_column('field_value',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=255),
               existing_nullable=True)
        batch_op.alter_column('header',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.Text(),
               existing_nullable=True)
        batch_op.alter_column('params',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.Text(),
               existing_nullable=True)
        batch_op.alter_column('path',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=255),
               existing_nullable=True)
        batch_op.alter_column('res_assert',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=255),
               existing_nullable=True)
        batch_op.alter_column('sql',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.Text(),
               existing_nullable=True)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=255),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)

    with op.batch_alter_table('testcases', schema=None) as batch_op:
        batch_op.alter_column('sql',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
        batch_op.alter_column('res_assert',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
        batch_op.alter_column('path',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
        batch_op.alter_column('params',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
        batch_op.alter_column('header',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
        batch_op.alter_column('field_value',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)

    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.alter_column('task_make_email',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
        batch_op.alter_column('run_time',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
        batch_op.alter_column('report_to',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
        batch_op.alter_column('report_copy',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)

    with op.batch_alter_table('parameters', schema=None) as batch_op:
        batch_op.alter_column('param_desc',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(length=64),
               existing_nullable=True)
        batch_op.alter_column('default',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=64),
               existing_nullable=True)

    with op.batch_alter_table('mocks', schema=None) as batch_op:
        batch_op.alter_column('path',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
        batch_op.alter_column('params',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
        batch_op.alter_column('header',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)

    with op.batch_alter_table('interfaces', schema=None) as batch_op:
        batch_op.alter_column('response',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
        batch_op.alter_column('path',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
        batch_op.alter_column('params',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
        batch_op.alter_column('header',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)

    with op.batch_alter_table('environments', schema=None) as batch_op:
        batch_op.alter_column('url',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
        batch_op.alter_column('db_host',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)

    with op.batch_alter_table('caseresults', schema=None) as batch_op:
        batch_op.alter_column('res_assert',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
        batch_op.alter_column('path',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
        batch_op.alter_column('params',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
        batch_op.alter_column('header',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
        batch_op.alter_column('diff_res',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)

    # ### end Alembic commands ###
