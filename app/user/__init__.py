#coding:utf-8
#date:2020/3/209:43
#author:CQ_Liu
from flask import Blueprint

#'auth'是蓝图的名称
#__name__是蓝图所在的路径
user = Blueprint('user',__name__)

#当导入auth这个包的时候是导入__init__.py文件，所以在__init__.py中导入view.py函数
from . import views