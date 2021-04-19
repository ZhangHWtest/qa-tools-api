# -*- coding: utf-8 -*-

from .views import *
from .views import environment

environment.add_url_rule('/environment/list', view_func=EnvironmentList.as_view('environment_list'))
environment.add_url_rule('/environment/info', view_func=EnvironmentInfo.as_view('environment_info'))
environment.add_url_rule('/environment/add', view_func=AddEnvironment.as_view('add_environment'))
environment.add_url_rule('/environment/edit', view_func=EditEnvironment.as_view('edit_environment'))
environment.add_url_rule('/environment/del', view_func=DelEnvironment.as_view('del_environment'))
