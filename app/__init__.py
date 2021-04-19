#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_cors import CORS
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_cache import Cache
from config import lod, cache_config, jobstores, executors
from apscheduler.schedulers.background import BackgroundScheduler

api = Api(
    version='1.0',
    title='自动化测试平台',
    description='api自动化测试平台',
    doc='/api',
    license_url="/api"
)
app = Flask(__name__)
CORS(app, resources=r'/*', supports_credentials=True)
api.init_app(app)
app.config.from_object(lod())
cache = Cache(app=app, config=cache_config, with_jinja2_ext=False)
loginManager = LoginManager(app)
loginManager.session_protection = "strong"
loginManager.login_view = 'home.login'
loginManager.login_message = u'接口自动化测试平台必须登录，请登录您的平台账号！'
db = SQLAlchemy(app)
sched = BackgroundScheduler(jobstores=jobstores, executors=executors)
admin = Admin(app, name=u'FXTest系统管理后台')

from app import models
