#coding:utf-8
#date:2020/3/109:13
#author:CQ_Liu

import os

# 获取当前项目的绝对路径;
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    所有配置环境的基类, 包含通用配置
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'westos secret key'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[西部开源]'
    FLASKY_MAIL_SENDER = '976131979@qq.com'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """
    开发环境的配置i信息
    """
    # 启用了调试支持，服务器会在代码修改后自动重新载入，并在发生错误时提供一个相当有用的调试器
    DEBUG = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '976131979'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or '密码'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'datadev.sqlite')

class TestingConfig(Config):
    """
    测试环境的配置信息
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'datatest.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'data.sqlite')

config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        'default': DevelopmentConfig
         }


