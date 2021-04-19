#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

# jenkins_url = 'http://localhost:8080'		# jenkins的地址
# jenkins_user = 'test'		# jenkins的用户名
# jenkins_password = '123456'		# jenkins的密码
SYSTEM_REQUEST_TOKE = 'flask_token_system'		# 系统内部依赖接口请求的时候需要加个token来区分
TRY_NUM_CASE = 5		# 重试的次数
INTERFACE_TIME_OUT = 5		# 超时时间 秒
TEST_FAIL_TRY_NUM = 3
# 在这里配置接受通知的钉钉群自定义机器人webhook，
access_token = '0fa5b764669ac07c1ccb1eb878249fdb4d701002a13b0a8c03b5d13f5e0ef11b'
ddq_url = 'https://oapi.dingtalk.com/robot/send?access_token=%s' % access_token
IMPORT_LIMIT_NUM = 50		# 配置可以导入限制
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 1
REDIS_PASSWORD = 'za111111'
MAX_CONNEC_REDIS = 10
# SAVE_DURATION = 24*60*60		# 配置redis存储的时长
cache_config = {
  'CACHE_TYPE': 'redis',
  'CACHE_REDIS_HOST': REDIS_HOST,
  'CACHE_REDIS_PORT': REDIS_PORT,
  'CACHE_REDIS_DB': REDIS_DB,
  'CACHE_REDIS_PASSWORD': REDIS_PASSWORD,
}
# email_type = "online.com"
jobstores = {
    'redis': RedisJobStore(db=0, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD),
}
executors = {
    'default': ThreadPoolExecutor(10),
    'processpool': ProcessPoolExecutor(3),
}


class Dev(object):		# 研发环境配置
    SECRET_KEY = 'zatest'
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "dev.sqlite")
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.163.com'		# 你的邮箱的smtp服务
    MAIL_PORT = 25		# 端口号
    MAIL_USE_TLS = True		# 是否检验
    MAIL_USERNAME = ""		# 你的邮箱
    MAIL_PASSWORD = ""		# 你邮箱的授权码
    CSRF_ENABLED = True
    UPLOAD_FOLDER = '/upload'
    DEBUG = True
    @staticmethod
    def init_app(app):
        pass


class Test(object):		# 测试环境的配置
    SECRET_KEY = 'zatest'
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "test.sqlite")
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.163.com'		# 你的邮箱的smtp服务
    MAIL_PORT = 25		# 端口号
    MAIL_USE_TLS = True		# 是否检验
    MAIL_USERNAME = ""		# 你的邮箱
    MAIL_PASSWORD = ""		# 你邮箱的授权码
    CSRF_ENABLED = True
    UPLOAD_FOLDER = '/upload'
    DEBUG = True
    @staticmethod
    def init_app(app):
        pass


class Produce(object):		# 线上环境的配置
    SECRET_KEY = 'Platform_Online'
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://test:Meihao100@bfbd@192.168.100.54:3306/qa-test"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 100
    MAIL_SERVER = 'smtp.163.com'		# 你的邮箱的smtp服务
    MAIL_PORT = 25		# 端口号
    MAIL_USE_TLS = True		# 是否检验
    MAIL_USERNAME = ""		# 你的邮箱
    MAIL_PASSWORD = ""		# 你邮箱的授权码
    CSRF_ENABLED = True
    UPLOAD_FOLDER = '/upload'
    DEBUG = False
    @staticmethod
    def init_app(app):
        pass


def lod():
    return Dev


class Config(object):
    JOBS = []
    SCHEDULER_API_ENABLED = True
