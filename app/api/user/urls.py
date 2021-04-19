# -*- coding: utf-8 -*-

from .views import *
from .views import user

user.add_url_rule('/user/list', view_func=UserList.as_view('user_list'))
user.add_url_rule('/user/add', view_func=AddUser.as_view('add_user'))
user.add_url_rule('/user/change_password', view_func=ChangePassword.as_view('change_password'))
user.add_url_rule('/user/reset_password', view_func=ResetPassword.as_view('reset_password'))
user.add_url_rule('/user/on_off_user', view_func=OnOffUser.as_view('on_off_user'))
user.add_url_rule('/user/set_role', view_func=SetRole.as_view('set_role'))
