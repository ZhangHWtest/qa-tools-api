# -*- coding: utf-8 -*-

from .views import *
from .views import home

home.add_url_rule('/index', view_func=Index.as_view('index'))
home.add_url_rule('/register', view_func=Register.as_view('register'))
home.add_url_rule('/login', view_func=Login.as_view('login'))
home.add_url_rule('/logout', view_func=Logout.as_view('logout'))
home.add_url_rule('/start_cs', view_func=StartCaseStatistics.as_view('start_case_statistics'))
home.add_url_rule('/stop_cs', view_func=StopCaseStatistics.as_view('stop_case_statistics'))
home.add_url_rule('/test_cs', view_func=TestCaseStatistics.as_view('test_case_statistics'))
