from flask import render_template, redirect, url_for, flash, request, session, Response
from . import main
from .. import db
from ..models.models import Course, ChatMessage, Teacher, Student
from flask_login import current_user, login_required
from flask import request
from flask_sse import sse
import redis
import datetime

@main.before_request
@login_required
def before_request():
    pass


@main.route('/', methods=['GET', 'POST'])
def index():

    #教师特色主页
    if current_user.user_type() == 1:
        return redirect(url_for('teacher.index'))

    # 学生特色主页
    if current_user.user_type() == 2:
        return redirect(url_for('student.index'))

    return redirect(url_for('dean.manage_semester'))


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form['user']
        return redirect(url_for('index'))
    return '<form action="" method="post">user: <input name="user">'


@main.route('/<int:course_id>/post', methods=['GET', 'POST'])
def post(course_id):
    message = request.form['message']
    user = str(current_user.id)
    # now = datetime.datetime.now().replace(microsecond=0).time()
    time = str(datetime.datetime.now()).split('.')[0]

    # 写入数据库
    cm = ChatMessage()
    cm.course_id = course_id
    # 当前用户是老师
    if current_user.user_type() == 1:
        # cm.student_id = 0
        cm.teacher_id = current_user.id
    # 当前用户是学生
    else:
        cm.student_id = current_user.id
        # cm.teacher_id = 0
    cm.time = datetime.datetime.now()
    cm.content = message

    db.session.add(cm)
    db.session.commit()

    # sse.publish('chat', u'[%s] %s: %s' % (time, user, message))
    sse.publish({'message': message, 'user_id': current_user.id, 'time': time, 'user_name': current_user.name, 'identity': current_user.user_type()}, type=course_id)

    return Response(status=204)


@main.route('/<int:course_id>/chat', methods=['GET', 'POST'])
def chat(course_id):
    cm_list = ChatMessage.query.filter_by(course_id=course_id).order_by(ChatMessage.id.desc()).all()[:10][::-1]
    return render_template('chat.html', course_id=course_id, cm_list=cm_list, nav='chat')

