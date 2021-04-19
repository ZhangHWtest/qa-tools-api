# -*- coding: utf-8 -*-

from .views import *
from .views import project

project.add_url_rule('/project/list', view_func=ProjectList.as_view('project_list'))
project.add_url_rule('/project/info', view_func=ProjectInfo.as_view('project_info'))
project.add_url_rule('/project/add', view_func=AddProject.as_view('add_project'))
project.add_url_rule('/project/edit', view_func=EditProject.as_view('edit_project'))
project.add_url_rule('/project/del', view_func=DelProject.as_view('del_project'))
