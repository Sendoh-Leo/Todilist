#coding:utf-8
#date:2020/3/109:00
#author:CQ_Liu

from  flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo,ValidationError
from app.models import User

class RegisterationForm(FlaskForm):
    email = StringField('电子邮箱',validators=[DataRequired(),Length(1,100),Email()])

    username = StringField('用户名',validators=[DataRequired(), Length(1, 64), Regexp('^\w*$', message='用户名只能由字母数字或者下划线组成')])

    password = PasswordField('密码',validators=[DataRequired()])

    repassword = PasswordField('确认密码',validators=[DataRequired(),EqualTo('password',message='密码不一致')])

    submit = SubmitField('注册')

    # 两个自定义的验证函数, 以validate_ 开头且跟着字段名的方法,这个方法和常规的验证函数一起调 用。
    #filed是email表单对象，filed.data是Email表单里的信息
    def valideate_email(self,field):
        #from app.models import User
        #从数据库对象中寻找User.query.filter_by（过滤）email属性
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('电子邮箱已经注册')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经占用')

class LoginForm(FlaskForm):
    """用户登录表单"""
    email = StringField('电子邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')

