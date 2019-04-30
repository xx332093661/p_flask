# -*- coding: utf-8 -*-

import os
# import psycopg2
import logging
from logging.handlers import TimedRotatingFileHandler

basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very hard to guess'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FANXIANGCE_MAIL_SUBJECT_PREFIX = u'[翻相册]'
    FANXIANGCE_MAIL_SENDER = 'mimi_19@sina.com'
    FANXIANGCE_ADMIN = '332093661@qq.com' # os.environ.get('FANXIANG_ADMIN')
    UPLOADED_PHOTOS_DEST = os.getcwd() + '/app/static/img/'
    FANXIANGCE_COMMENTS_PER_PAGE = 15
    FANXIANGCE_ALBUMS_PER_PAGE = 12
    FANXIANGCE_PHOTOS_PER_PAGE = 20
    FANXIANGCE_ALBUM_LIKES_PER_PAGE = 12
    FANXIANGCE_PHOTO_LIKES_PER_PAGE = 20
    FANXIANGCE_FOLLOWERS_PER_PAGE = 10
    BOOTSTRAP_SERVE_LOCAL = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.sina.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'mimi_19@sina.com' #os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = 'december' #os.environ.get('MAIL_PASSWORD')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \
    #     'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    SQLALCHEMY_DATABASE_URI = 'mysql://root:admin@localhost:3306/test-xiangce'

#
#
# class TestingConfig(Config):
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
#         'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:admin@localhost:3306/test-xiangce'

    @staticmethod
    def init_app(app):
        Config.init_app(app)

        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        _logger = logging.getLogger()

        LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '.', 'app.log'))

        # 添加TimedRotatingFileHandler
        # 定义一个1秒换一次log文件的handler
        # 保留3个旧log文件
        # filehandler = logging.handlers.TimedRotatingFileHandler(LOG_PATH, when='S', interval=1, backupCount=3)
        # 设置后缀名称，跟strftime的格式一样
        # filehandler.suffix = "%Y-%m-%d_%H-%M-%S.log"

        filehandler = logging.handlers.TimedRotatingFileHandler(LOG_PATH, when='D', interval=1, backupCount=10)
        # filehandler.suffix = "%Y-%m-%d.log"
        _logger.addHandler(filehandler)


        # log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.', 'app_%s.log' % time_now.strftime('%Y-%m-%d-%H%M')))
        # logging.basicConfig(level=logging.DEBUG,
        #                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        #                     datefmt='%Y-%m-%d %H:%M:%S',
        #                     filename=log_path,
        #                     filemode='a')

#
#
# class HerokuConfig(Config):
#     DEBUG = True
#     MAIL_SERVER = 'smtp.sina.com'
#     MAIL_PORT = 25
#     MAIL_USE_TLS = True
#     MAIL_USERNAME = 'mimi_19@sina.com'  # os.environ.get('MAIL_USERNAME')
#     MAIL_PASSWORD = 'december'  # os.environ.get('MAIL_PASSWORD')
#     # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


config = {
    # 'development': DevelopmentConfig,
    # 'testing': TestingConfig,
    'production': ProductionConfig,
    # 'heroku': HerokuConfig,
    'default': DevelopmentConfig
}