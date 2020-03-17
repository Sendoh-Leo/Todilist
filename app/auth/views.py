#coding:utf-8
#date:2020/3/109:01
#author:CQ_Liu

#蓝图对象上注册路由，指定静态文件夹，注册模板过滤器
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required

from app import db
from app.auth import auth
#此处导入auth为实例化的蓝图，来自__init__.py文件中，用蓝图管理views中的函数
from app.auth.forms import RegisterationForm, LoginForm
from app.models import User, Role


@auth.route('/')
def index():

    return render_template('auth/index.html')

@auth.route('/login',methods = (['GET','POST']))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #判断用户是否存在并且密码是否正确
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('用户%s登录成功' %(user.username),category='success')
            return redirect(url_for('auth.index'))
        else:
            flash('用户%s登录失败，错误的用户名或密码.' %(form.email.data),category='error')
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html', form=form)

@auth.route('/register',methods = (['GET','POST']))
def register():
    """
    /register
        -GET   获取html页面
        -POST   获取提交到页面的信息
        1）判断是否为post方法提交数据，提交的数据是否通过表单验证
        2）若通过验证，存储到数据库中,注册成功跳转到登录页面
        获取表单数据的两种方法
            1）.form.data  得到一个字典，按字典的键值方式获取
            2）直接由属性获取   form.email.data   form.username.data
    :return:
    """
    form = RegisterationForm()
    if form.validate_on_submit():
        #实例化数据库对象
        user = User()
        #username为数据库字段
        user.username = form.username.data
        user.password = form.password.data
        user.email = form.email.data
        user.role = Role.query.filter_by(username = '普通会员').first()
        db.session.add(user)
        flash('用户%s注册成功' %(user.username),category='success')
        #注册成功跳转至登录页面
        #return redirect('/longin')
        #方法二，通过视图函数寻找对应的路由地址
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html',form=form)

@auth.route('/logout',methods = (['GET','POST']))
@login_required
def logout():
    logout_user()
    flash('用户注销成功.',category='success')

    #return 'longout'
    return redirect(url_for('auth.index'))
