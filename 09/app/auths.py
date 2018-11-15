from flask import flash, redirect, url_for
from flask_login import current_user
from .models.models import Student, Teacher, Course
from functools import wraps


class UserAuth:
    """
    权限认证装饰器，对应装饰器应用在route下即可，若权限不够将返回主页
    """
    @staticmethod
    def dean(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            if not current_user.user_type() == 0:
                flash('无权限', 'danger')
                return redirect(url_for('main.index'))
            else:
                return func(*args, **kwargs)
        return decorated

    @staticmethod
    def teacher(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            if not current_user.user_type() == 1:
                flash('无权限', 'danger')
                return redirect(url_for('main.index'))
            else:
                return func(*args, **kwargs)
        return decorated

    @staticmethod
    def student(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            if not current_user.user_type() == 2:
                flash('无权限！', 'danger')
                return redirect(url_for('main.index'))
            else:
                return func(*args, **kwargs)
        return decorated

    @staticmethod
    def teacher_course_access(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            if not Course.query.filter_by(id=kwargs['course_id']).filter(
                    Course.teachers.any(id=current_user.id)).first():
                flash('无权限！', 'danger')
                return redirect(url_for('main.index'))
            else:
                return func(*args, **kwargs)
        return decorated

    @staticmethod
    def student_course_access(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            if not Course.query.filter_by(id=kwargs['course_id']).filter(
                    Course.students.any(id=current_user.id)).first():
                flash('无权限！', 'danger')
                return redirect(url_for('main.index'))
            else:
                return func(*args, **kwargs)
        return decorated