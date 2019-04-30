# _*_ coding: utf-8 _*_
import os


# 调试模式是否开启
DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = False
# session必须要设置key
SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# mysql数据库连接信息,这里改为自己的账号
SQLALCHEMY_DATABASE_URI = "mysql://root:admin@localhost:3306/taobao3"

UPLOADED_DOCUMENTS_DEST = os.path.abspath(os.path.join(os.path.dirname(__file__), 'files/'))