from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from .forms import LoginForm, ChangePasswordForm
from . import auth
from ..models.models import DeanInfo, Student, Teacher
from flask_login import current_user
from .. import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.identity.data == '0':
            user = DeanInfo.query.filter_by(id=form.username.data).first()
            if user is not None and user.verify_password(form.password.data):
                login_user(user, form.remember_me.data)
                session['user_type'] = 'dean'
                return redirect(request.args.get('next') or url_for('main.index'))
        elif form.identity.data == '1':
            user = Teacher.query.filter_by(id=form.username.data).first()
            if user is not None and user.verify_password(form.password.data):
                login_user(user, form.remember_me.data)
                session['user_type'] = 'teacher'
                return redirect(request.args.get('next') or url_for('main.index'))
        else:
            user = Student.query.filter_by(id=form.username.data).first()
            if user is not None and user.verify_password(form.password.data):
                login_user(user, form.remember_me.data)
                session['user_type'] = 'student'
                return redirect(request.args.get('next') or url_for('main.index'))
        flash('用户名或账户错误')

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            flash('密码修改成功', 'success')
            logout_user()
            return redirect(url_for('auth.login'))
        else:
            print(2333)
            flash('旧密码错误', 'danger')
    return render_template('auth/change_password.html', form=form)
