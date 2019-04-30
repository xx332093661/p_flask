# -*- coding: utf-8 -*-

import os
import logging
# import psycopg2

basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very hard to guess'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # UPLOADED_DOCUMENTS_DEST = os.getcwd() + '/app/files/'
    UPLOADED_DOCUMENTS_DEST = os.path.abspath(os.path.dirname(__file__)) + '/app/files/'
    # FANXIANGCE_COMMENTS_PER_PAGE = 15
    FANXIANGCE_ALBUMS_PER_PAGE = 12
    # FANXIANGCE_PHOTOS_PER_PAGE = 20
    # FANXIANGCE_ALBUM_LIKES_PER_PAGE = 12
    # FANXIANGCE_PHOTO_LIKES_PER_PAGE = 20
    # FANXIANGCE_FOLLOWERS_PER_PAGE = 10
    # BOOTSTRAP_SERVE_LOCAL = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:admin@localhost:3306/taobao4'

#
#
# class TestingConfig(Config):
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
#         'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    DEBUG = False
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:admin@localhost:3306/taobao4'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:admin1!@#$@101.37.254.86:3306/taobao4'

    @staticmethod
    def init_app(app):
        Config.init_app(app)

        log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.', 'app.log'))
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=log_path,
                            filemode='a')




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