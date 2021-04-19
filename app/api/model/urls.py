# -*- coding: utf-8 -*-

from .views import *
from .views import model

model.add_url_rule('/model/list', view_func=ModelList.as_view('model_list'))
model.add_url_rule('/model/info', view_func=ModelInfo.as_view('model_info'))
model.add_url_rule('/model/add', view_func=AddModel.as_view('add_model'))
model.add_url_rule('/model/edit', view_func=EditModel.as_view('edit_model'))
model.add_url_rule('/model/del', view_func=DelModel.as_view('del_model'))
