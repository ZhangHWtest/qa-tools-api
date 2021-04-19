"""管理后台"""
from app import admin
from app.models import *
from flask_admin.contrib.sqla import ModelView


class Useradmin(ModelView):
    column_labels = dict(
        username=u'用户名',
        user_email=u'用户邮件',
        status=u'状态',
        is_sper=u'权限',
        works=u'职位',
        password=u'密码'
    )


admin.add_view(Useradmin(User, db.session, name=u'用户', endpoint='adminuser'))
admin.add_view(ModelView(Task, db.session, name='定时任务', endpoint='tingtask'))
admin.add_view(ModelView(TestCase, db.session, name='测试用例', endpoint='case'))
admin.add_view(ModelView(Interface, db.session, name='接口', endpoint='jiekou'))
