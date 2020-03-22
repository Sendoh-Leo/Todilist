#coding:utf-8
#date:2020/3/209:43
#author:CQ_Liu
from flask import abort, flash, redirect, url_for

from flask import render_template
from flask_login import login_required, current_user

from app import db
from app.models import User
from app.user import user
from app.user.forms import EditProfileForm


@user.route('/changepwd/<id>')
def change_password(id):
    return 'change password'

@user.route('/user/<id>')
@login_required
def users(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    else:
        todos = user.todos
        all_count = len(todos)
        undo_count = done_count=0
        for todo in todos:
            if todo.status:
                done_count+=1
            else:
                undo_count+=1
    return render_template('user/user.html', user=user,
                           all_count=all_count,
                           done_count=done_count,
                           undo_count=undo_count)

@user.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('用户配置信息更新成功!', category='success')
        return redirect(url_for('user.users', id=current_user.id))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me

    return render_template('user/edit_profile.html', form=form)
