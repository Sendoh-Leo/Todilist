#coding:utf-8
#date:2020/3/1015:49
#author:CQ_Liu
import unittest
#flask中的current_app可以自动搜索项目里是否创建出flask实例(即app=create_app)
from flask import  current_app
from app import create_app


#所有测试用例需以test开头，
class BasicsTestCase(unittest.TestCase):
    """
    setUp() 和 tearDown() 方法分别在各测试前后运行,并且名字以 test_ 开头的函数都作为测试执行
    """

    def setUp(self):
        """
        在测试前创建一个测试环境。
        1). 使用测试配置创建程序
        2). 激活上下文, 确保能在测试中使用 current_app
        3). 创建一个全新的数据库,以备不时之需。
        """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        # Pops the app context
        self.app_context.pop()

    def test_app_exists(self):
        """
        测试当前app是否存在?
        """
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """
        测试当前app是否为测试环境?
        """
        self.assertTrue(current_app.config['TESTING'])