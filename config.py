#coding:utf-8
#date:2020/3/109:13
#author:CQ_Liu

import os

# 获取当前项目的绝对路径;
basedir = os.path.abspath(os.path.dirname(__file__))

"""
qq邮箱的配置信息：需写入配置中    （163邮箱的配置信息已写入开发环境中）
   # 添加的发送邮件的配置信息 MAIL_SERVER = 'smtp.qq.com' 
   # 指定端口， 默认25， 但qq邮箱默认为 端口号465或587； MAIL_PORT = 465 
   #由于QQ邮箱不支持非加密的协议，那么使用加密协议, 分为两种加密协议，选择其中之一即可  MAIL_USE_SSL = True 
    MAIL_USERNAME = '976131979@qq.com'
   # 此处的密码并非邮箱登录密码， 而是开启   pop3 MAIL_PASSWORD = "自己的密码123sdjuoeyoxjoubedb"
"""


class Config:
    """
    所有配置环境的基类, 包含通用配置
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'westos secret key'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # FLASKY_MAIL_SUBJECT_PREFIX = '[西部开源]'
    # FLASKY_MAIL_SENDER = '976131979@qq.com'
    PER_PAGE = 5
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """
    开发环境的配置i信息
    """
    # 启用了调试支持，服务器会在代码修改后自动重新载入，并在发生错误时提供一个相当有用的调试器
    DEBUG = True
    # MAIL_SERVER = 'smtp.qq.com'
    # MAIL_PORT = 587
    """ 由于QQ邮箱不支持非加密的协议，那么使用加密协议, 分为两种加密协议，选择其中之一即可 """
    #MAIL_USE_TLS = True

    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USERNAME = '18829288784@163.com'
    # 此处的密码并非邮箱登录密码， 而是开启pop3
    MAIL_PASSWORD = "YTVPJEJJFUCGSWDS"

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


