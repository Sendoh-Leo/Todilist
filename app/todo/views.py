#coding:utf-8
#date:2020/3/109:01
#author:CQ_Liu
from app.todo import todo
@todo.route('/add/')
def add():
    return 'todo add'
@todo.route('/delete/')
def delete():
    return 'todo delete'