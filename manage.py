# -*- coding: utf-8 -*-
# @file: manage.py
"""主运行文件，使用gevent异步请求"""
# from gevent.pywsgi import WSGIServer
# from gevent import monkey
# monkey.patch_all()
from app import app
from app import sched
from app.api.tools import tools
from app.api.home import home
from app.api.user import user
from app.api.project import project
from app.api.model import model
from app.api.interface import interface
from app.api.case import case
from app.api.task import task
from app.api.environment import environment
from app.api.mock import mock
from app.api.equipment import equipment
from app.api.report import  report
app.register_blueprint(tools)
app.register_blueprint(home)
app.register_blueprint(user)
app.register_blueprint(project)
app.register_blueprint(model)
app.register_blueprint(interface)
app.register_blueprint(case)
app.register_blueprint(task)
app.register_blueprint(environment)
app.register_blueprint(mock)
app.register_blueprint(equipment)
app.register_blueprint(report)
sched.start()

# def app_start():
# 	sched.start()
# 	http_server = WSGIServer(('0.0.0.0', 5555), app)
# 	http_server.serve_forever()


if __name__ == '__main__':
	# app_start()
	app.run()
