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

from app.auth.send_email import send_mail

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
            #return redirect(url_for('auth.index'))   此处定位到auth.index不会进行comfirmed判断，即用户confirmed状态为True或者False都可以登录跳转到auth.index
            return redirect(url_for('todo.index'))    #此处定位到todo.index，定位时回用钩子函数进行判定，如果confirmed=False，则进行验证等操作
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
        token = user.generate_confirmation_token()
        #接收人to=[]  用列表保存
        send_mail(to=[user.email,], subject='请激活你的任务管理平台帐号', filename='auth/confirm', user=user, token=token)
        flash('平台验证消息已经发送到你的邮箱， 请确认后登录.', category='success')
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

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    """
    判断用户账户是否验证，验证转到主页
    没有验证，执行验证函数，用户状态confirmed转为True
    :param token:
    :return:
    """
    if current_user.confirmed:
        return redirect(url_for('todo.index'))
    if current_user.confirm(token):
        flash('验证邮箱通过', category='success')
    else:
        flash('验证连接失效', category='error')
    return redirect(url_for('todo.index'))

@auth.before_app_request
def before_request():
    """
    钩子函数，当用户登录但没确认邮箱登录账户，进入unconfirmed页面

    and request.endpoint[:5] != 'auth.'  ----->只要定位的不是auth，就要进行跳转验证，，即对应views中的login，在登陆时跳转到auth.index不需要验证confirmed，跳转到todo.index则需要
    :return:
    """
    if current_user.is_authenticated \
        and not current_user.confirmed \
        and request.endpoint[:5] != 'auth.' \
        and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    # 如果当前用户是匿名用户或者已经验证的用户， 则访问主页, 否则进入未验证界面;
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('todo.index'))
    token = current_user.generate_confirmation_token()
    return render_template('auth/unconfirmed.html')

@auth.route('/reconfirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    try:
        send_mail([current_user.email], '请激活你的任务管理平台帐号','auth/confirm', user=current_user, token=token)
    except Exception as e:
        print(e)
        flash(str(e), category='error')
        return redirect(url_for('auth.register'))
    else:
        flash('新的平台验证消息已经发送到你的邮箱， 请确认后登录.', category='success')
        return redirect(url_for('todo.index'))