#coding:utf-8
#date:2020/3/109:00
#author:CQ_Liu
#创建蓝图
from flask import Blueprint

#'auth'是蓝图的名称
#__name__是蓝图所在的路径
auth = Blueprint('auth',__name__)

#当导入auth这个包的时候是导入__init__.py文件，所以在__init__.py中导入view.py函数
from . import views