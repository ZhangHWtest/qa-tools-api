# -*- coding: utf-8 -*-

from .views import *
from .views import task

task.add_url_rule('/task/list', view_func=TaskList.as_view('task_list'))
task.add_url_rule('/task/info', view_func=TaskInfo.as_view('task_info'))
task.add_url_rule('/task/add', view_func=AddTask.as_view('add_task'))
task.add_url_rule('/task/edit', view_func=EditTask.as_view('edit_task'))
task.add_url_rule('/task/del', view_func=DelTask.as_view('del_task'))
task.add_url_rule('/task/update_case', view_func=UpdateTaskCase.as_view('update_task_case'))
task.add_url_rule('/task/start', view_func=StartTask.as_view('start_task'))
task.add_url_rule('/task/stop', view_func=StopTask.as_view('stop_task'))
task.add_url_rule('/task/result_list', view_func=TaskResList.as_view('task_result_list'))
task.add_url_rule('/task/result_info', view_func=TaskResInfo.as_view('task_result_info'))
