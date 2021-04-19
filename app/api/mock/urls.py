# -*- coding: utf-8 -*-

from .views import *
from .views import mock

mock.add_url_rule('/mock/list', view_func=MockList.as_view('mock_list'))
mock.add_url_rule('/mock/info', view_func=MockInfo.as_view('mock_info'))
mock.add_url_rule('/mock/add', view_func=AddMock.as_view('add_mock'))
mock.add_url_rule('/mock/edit', view_func=EditMock.as_view('edit_mock'))
mock.add_url_rule('/mock/del', view_func=DelMock.as_view('del_mock'))
mock.add_url_rule('/mock/status', view_func=MockStatus.as_view('mock_status'))
mock.add_url_rule('/mock/<string:path>', view_func=MockServer.as_view('mock_server'))
