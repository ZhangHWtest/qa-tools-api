# -*- coding: utf-8 -*-
# @File    : db_migrate.py
"""数据库同步使用"""

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import db, app

manage = Manager(app)
migrate = Migrate(app, db=db, render_as_batch=True)
manage.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manage.run()

# a.使用init自命令创建迁移仓库.$ python db_migrate.py db init
# 该命令会创建 migrations 文件夹, 所有迁移脚本都存在其中.

# b.创建数据路迁移脚本.
# $ python db_migrate.py db migrate -m "COMMONT"
# 自动创建迁移.
# 自动创建的迁移会根据模型定义和数据库当前的状态之间的差异生成
# upgrade() 和 downgrade() 函数的内容.
# ** 自动创建的迁移不一定总是正确的, 有可能漏掉一些细节, 自动生成迁移脚本后一定要进行检查.

# c.更新数据库
# $ python db_migrate.py db upgrade
# 将迁移应用到数据库中.
