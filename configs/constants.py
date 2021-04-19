#!/usr/bin/env python
# -*- coding: utf-8 -*-

import platform
import env

# http请求header
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept - Encoding':'gzip, deflate',
           'Accept-Language':'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
           'Connection':'Keep-Alive',
           'Upgrade-Insecure-Requests':'1',
           'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
           }

# 系统环境配置
systype = platform.system()
if systype == "Windows":    # windows系统参数
    # excel路径
    excel_path = "\\excel\\"
elif systype == "Linux":  # linux系统参数
    # excel路径
    excel_path = "/excel/"

if env.environment == 'TEST':
    # 测试环境EDU数据库
    HOST_EDU = "192.168.100.54"
    PORT_EDU = 3306
    USER_EDU = "test"
    PASSWORD_EDU = "Meihao100@bfbd"
    # 测试环境视频服务数据库
    HOST_HKY_LIVE = "192.168.100.54"
    PORT_HKY_LIVE = 3306
    USER_HKY_LIVE = "test"
    PASSWORD_HKY_LIVE = "Meihao100@bfbd"
    # 测试环境MOS数据库
    HOST_MOS = "192.168.100.54"
    PORT_MOS = 3306
    USER_MOS = "test"
    PASSWORD_MOS = "Meihao100@bfbd"
elif env.environment == 'ONLINE':
    # 正式环境EDU数据库
    HOST_EDU = "rr-2zeb64zax3uxitrs91xo.mysql.rds.aliyuncs.com"
    PORT_EDU = 3306
    USER_EDU = "kkb_read"
    PASSWORD_EDU = "ndpf5Js3TqXaNz9VoQ01W6f6eT7tZRNi1"
    # 正式环境视频服务数据库
    HOST_HKY_LIVE = "rr-2zei6qrx6f2l6ic124do.mysql.rds.aliyuncs.com"
    PORT_HKY_LIVE = 3306
    USER_HKY_LIVE = "zhangtai"
    PASSWORD_HKY_LIVE = "wB8cKcQR6PSDfxo6p"
    # 正式环境MOS数据库
    HOST_MOS = "rm-2ze0f3u1v79619rwt5o.mysql.rds.aliyuncs.com"
    PORT_MOS = 3306
    USER_MOS = "azhang"
    PASSWORD_MOS = "1Do4eMquwApCZ7U5e"

# 学习中心passport数据库
MYSQL_PASSPORT = {
    "host": HOST_EDU,
    "port": PORT_EDU,
    "user": USER_EDU,
    "password": PASSWORD_EDU,
    "database": "kkb_cloud_passport",
    "charset": "utf8"
}

# 学习中心edu数据库
MYSQL_EDU = {
    "host": HOST_EDU,
    "port": PORT_EDU,
    "user": USER_EDU,
    "password": PASSWORD_EDU,
    "database": "kkb_cloud_edu",
    "charset": "utf8"
}

# 视频服务数据库
MYSQL_HKY_LIVE = {
    "host": HOST_HKY_LIVE,
    "port": PORT_HKY_LIVE,
    "user": USER_HKY_LIVE,
    "password": PASSWORD_HKY_LIVE,
    "database": "hky-cloud-live-platform",
    "charset": "utf8"
}

# mos_pay数据库
MYSQL_MOS_PAY = {
    "host": HOST_MOS,
    "port": PORT_MOS,
    "user": USER_MOS,
    "password": PASSWORD_MOS,
    "database": "kkb-cloud-pay",
    "charset": "utf8"
}

# mos_order数据库
MYSQL_MOS_ORDER = {
    "host": HOST_MOS,
    "port": PORT_MOS,
    "user": USER_MOS,
    "password": PASSWORD_MOS,
    "database": "kkb-cloud-order",
    "charset": "utf8"
}

# mos_vipcourse数据库
MYSQL_MOS_VIPCOURSE = {
    "host": HOST_MOS,
    "port": PORT_MOS,
    "user": USER_MOS,
    "password": PASSWORD_MOS,
    "database": "kkb-cloud-vipcourse",
    "charset": "utf8"
}




