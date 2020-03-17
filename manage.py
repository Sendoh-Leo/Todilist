#coding:utf-8
#date:2020/3/109:13
#author:CQ_Liu
from app import  create_app,db
from flask_script import  Manager,Shell
from flask_migrate import Migrate, MigrateCommand

from app.models import Role, User

app=create_app()
manager = Manager(app)
#将数据库迁移插件与数据库db和app关联
migrate = Migrate(app, db)
    # manager.command 修饰器让自定义命令变得简单。修饰函数名就是命令名,函数的文档字符串会显示在帮助消息中。

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    #unittest.TestLoader()--->把测试用例绑定到测试集合
    tests = unittest.TestLoader().discover('test')    #发现所有测试用例绑定成测试集合
    unittest.TextTestRunner(verbosity=2).run(tests)
"""
verbosity:测试结果信息的负责度--->0,1,2
0:静默模式，只获得总的测试用例和测试结果
1:默认模式，成功的用例前有'.',失败的用例前'F'
2.详细模式，显示每个测试用例的具体信息
"""

def make_shell_context():
    return dict(app=app,db = db,Role = Role,User = User)


# 初始化 Flask-Script、Flask-Migrate 和为 Python shell 定义的上下文。
#当执行交互式环境manage.py shell 时，自动传入函数make_shell_context（）中的返回值字典，字典的每个键对应操作命令 ，值对应的是操作对象
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
if __name__ == '__main__':
    manager.run()