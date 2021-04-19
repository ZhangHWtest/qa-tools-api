# -*- coding: utf-8 -*-

from .views import *
from .views import case

case.add_url_rule('/case/list', view_func=CaseList.as_view('case_list'))
case.add_url_rule('/case/info', view_func=CaseInfo.as_view('case_info'))
case.add_url_rule('/case/add', view_func=AddCase.as_view('add_case'))
case.add_url_rule('/case/edit', view_func=EditCase.as_view('edit_case'))
case.add_url_rule('/case/duplicate', view_func=DuplicateCase.as_view('duplicate_case'))
case.add_url_rule('/case/del', view_func=DelCase.as_view('del_case'))
case.add_url_rule('/case/single', view_func=RunSingleCase.as_view('run_single_case'))
case.add_url_rule('/case/multiple', view_func=RunMultipleCase.as_view('run_multiple_case'))
case.add_url_rule('/case/result_list', view_func=CaseResList.as_view('case_result_list'))
case.add_url_rule('/case/result_info', view_func=CaseResInfo.as_view('case_result_info'))
