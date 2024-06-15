import os.path
from pathlib import Path
from .const_bf import db_uri
from .const_bf import MAIL_USERNAME
from .const_bf import MAIL_PASSWORD

from redis import StrictRedis


class Config:
    SECRET_KEY = 'How^the%Steel&236c78afcb9a393ec1&was$Tempered'
    # mysql
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACE_MODIFICATIONS = False
    # SQLALCHEMY_RECORD_QUERIES = True
    # session in redis
    SESSION_TYPE = 'redis'
    SESSION_REDIS = StrictRedis(host='localhost', port=6379, db=4)
    SESSION_COOKIE_SECURE = False  # 为True需要HTTPS协议
    SESSION_USE_SIGNER = True
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = 12 * 60 * 60  # 秒
    # flask send email
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = MAIL_USERNAME  # QQ邮箱
    MAIL_PASSWORD = MAIL_PASSWORD
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
    # path
    BASE_DIR = Path(__file__).resolve().parent.parent
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
    UPLOAD_DIR = os.path.join(STATIC_DIR, 'uploads')
    ICON_DIR = os.path.join(UPLOAD_DIR, 'icon')
    PHOTO_DIR = os.path.join(UPLOAD_DIR, 'photo')
    # debug
    # DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True  # 启用模板编辑器
    # DEBUG_TB_PROFILER_ENABLED = True  # 在所有请求上启用分析器
    # DEBUG_TB_INTERCEPT_REDIRECTS = False  # 是否拦截重定向。


class Development(Config):
    ENV = 'development'
    DEBUG = True


class Production(Config):
    ENV = 'production'
    DEBUG = False


if __name__ == '__main__':
    print(Config.BASE_DIR)
    print(Config.STATIC_DIR)
