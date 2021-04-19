# -*- coding: utf-8 -*-

from .views import *
from .views import interface

interface.add_url_rule('/interface/list', view_func=InterfaceList.as_view('interface_list'))
interface.add_url_rule('/interface/info', view_func=InterfaceInfo.as_view('interface_info'))
interface.add_url_rule('/interface/add', view_func=AddInterface.as_view('add_interface'))
interface.add_url_rule('/interface/edit', view_func=EditInterface.as_view('edit_interface'))
interface.add_url_rule('/interface/move', view_func=MoveInterface.as_view('move_interface'))
interface.add_url_rule('/interface/del', view_func=DelInterface.as_view('del_interface'))
interface.add_url_rule('/interface/param/edit', view_func=EditParam.as_view('edit_param'))
interface.add_url_rule('/interface/header/edit', view_func=EditHeader.as_view('edit_header'))
interface.add_url_rule('/interface/response/edit', view_func=EditResponse.as_view('edit_response'))
interface.add_url_rule('/interface/response/import', view_func=ImportJsonData.as_view('import_json_data'))
