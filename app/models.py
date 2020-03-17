#coding:utf-8
#date:2020/3/109:00
#author:CQ_Liu

"""
设计数据库模型
    1.用户信息：User
    2.用户角色信息：Role
    3.用户角色和用户是1对多...(1：n)..一对多关系外键卸载多的一端.一个角色对应多个用户
"""
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

from flask_login import UserMixin

#类继承一个model对象，Flask中一个Model子类就是一个数据库表，表名默认  '类名'.lower()
class User(UserMixin,db.Model):
    """ Flask-Login 提供了一个 UserMixin 类,包含常用方法的默认实现,且能满足大多数需求。
            1). is_authenticated      用户是否已经登录?
            2). is_active             是否允许用户登录?False代表用户禁用
            3). is_anonymous          是否匿名用户?
            4). get_id()              返回用户的唯一标识符
    """



    __tablename__ = 'users'   #自定义表名
    #定义用户id: Column列数据，Integer整形，primary_key唯一标识，autoincrement自增
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    #定义用户名，列数据，字符串不超过100，唯一，不能为空
    username=db.Column(db.String(100),unique=True,nullable=False)
    #哈希密码,字段尽量大，不能为空
    password_hash = db.Column(db.String(200),nullable=False)
    #邮箱
    email = db.Column(db.String(50))

    #外键关联：表示一对多关系
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))

    """
    设置密码
    """
    @property    #不允许获取密码
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter   #设置密码
    def password(self,password):
         # generate_password_hash(password, method= pbkdf2:sha1 , salt_length=8) :密码加密的散列值。
         self.password_hash = generate_password_hash(password)

    def verify_password(self,password):    #验证密码
        # check_password_hash(hash, password) :密码散列值和用户输入的密码是否匹配.
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User % r>' % self.username

class Role(db.Model):
    __tablename__ = 'roles'  # 自定义表名
    # 定义用户id: Column列数据，Integer整形，primary_key唯一标识，autoincrement自增
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 定义用户名，列数据，字符串不超过100，唯一，不能为空


    username = db.Column(db.String(100), unique=True, nullable=False)
    #name = db.Column(db.String(100), unique=True, nullable=False)


    
    #1.Role添加属性users，可以访问拥有角色的所有用户，
    #2.User添加属性role，可以访问某一个用户的角色是什么
    users = db.relationship('User',backref = 'role')

    def __repr__(self):
        return '<Role % r>' % self.username

# 加载用户的回调函数;如果能找到用户,返回用户对象;否则返回 None 。
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))