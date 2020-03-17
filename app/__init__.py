#coding:utf-8
#date:2020/3/108:59
#author:CQ_Liu
"""
程序工厂函数, 延迟创建程序实例
"""
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import config

bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()


login_manager = LoginManager()
# session_protection 属性提供不同的安全等级防止用户会话遭篡改。
login_manager.session_protection = 'strong'
# login_view 属性设置登录页面的端点,跳出到登录页面
login_manager.login_view = 'auth.login'


def create_app(config_name='development'):
    """
    默认创建开发环境的app对象
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)

    # 用户认证新加扩展
    login_manager.init_app(app)


    # 附加路由和自定义的错误页面
    # .........后续还需完善， 补充视图和错误页面

    #注册蓝图，让app与蓝图关联
    from app.auth import auth
    # url_prefix： 指定访问该蓝图中定义的视图函数时需要添加的前缀， 没有指定则不加;
    #auth为蓝图对象
    app.register_blueprint(auth, url_prefix='/auth')

    from app.todo import todo
    app.register_blueprint(todo,url_prefix='/todo')  # 注册蓝本
    return app

