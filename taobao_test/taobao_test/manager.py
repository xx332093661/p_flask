# coding: utf-8
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from taobao_test import db
from taobao_test import app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand  # 载入migrate扩展


manager = Manager(app)
migrate = Migrate(app, db)  # 注册migrate到flask

manager.add_command('db', MigrateCommand)  # 在终端环境下添加一个db命令

if __name__ == '__main__':
    manager.run()