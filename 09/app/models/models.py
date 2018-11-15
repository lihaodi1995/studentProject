from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session


SCRelationship = db.Table('sc_relationship', db.Model.metadata,
                          db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
                          db.Column('course_id', db.Integer, db.ForeignKey('courses.id'))
                          )

TCRelationship = db.Table('tc_relationship', db.Model.metadata,
                          db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id')),
                          db.Column('course_id', db.Integer, db.ForeignKey('courses.id'))
                          )


class DeanInfo(UserMixin, db.Model):
    __tablename__ = 'deanInfo'
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def check_id(self):
        return self.id

    @staticmethod
    def user_type():
        return 0

    @staticmethod
    def init_dean():
        """野兽先辈管理员说"""
        dean = DeanInfo.query.first()
        if dean is None:
            dean = DeanInfo(id=810)
            dean.password = '114514'
            db.session.add(dean)
            db.session.commit()

    def __repr__(self):
        return '<DeanInfo %r>' % self.id


class Semester(db.Model):
    __tablename__ = 'semesters'
    id = db.Column(db.Integer, primary_key=True)
    base_info = db.Column(db.Text)
    begin_time = db.Column(db.Date)
    end_time = db.Column(db.Date)

    def __repr__(self):
        return '<Semester %r>' % self.id


class Student(UserMixin, db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.VARCHAR(length=50, convert_unicode=True))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def init_student():
        student = Student.query.first()
        if student is None:
            student = Student(id=666)
            student.password = '666'
            db.session.add(student)
            db.session.commit()

    @staticmethod
    def user_type():
        return 2

    def __repr__(self):
        return '<Student %r>' % self.id


class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    owner_grade = db.Column(db.Float, default=0)
    team_name = db.Column(db.VARCHAR(length=50, convert_unicode=True))
    status = db.Column(db.Integer, default=0)  # 0: building 1: pending 2: accepted 3: rejected 4: dismiss
    reject_reason = db.Column(db.Text)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    members = db.relationship('TeamMember', backref='team')
    owner = db.relationship('Student', uselist=False)
    submissions = db.relationship('Submission', backref='team')

    @property
    def number_of_members(self):
        return len([a for a in self.members if a.status == 1]) + 1

    def __repr__(self):
        return '<Team %r>' % self.id

    @property
    def order(self):
        return Team.query.filter_by(course_id=self.course_id).all().index(self)

    @staticmethod
    def team_list(course_id):
        teams = Team.query.filter_by(course_id=course_id).all()
        order = 1
        for team in teams:
            team.order = order  #为返回的 team 增加 order (顺序) 属性
            order += 1
        return teams


class TeamMember(db.Model):
    __tablename__ = 'team_members'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    status = db.Column(db.Integer, default=0)  # 0: pending 1: accepted 2: rejected
    grade = db.Column(db.Float, default=0)
    student = db.relationship('Student', uselist=False)

    def __repr__(self):
        return '<TeamMember %r>' % self.id


class Homework(db.Model):
    __tablename__ = 'homework'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    name = db.Column(db.VARCHAR(length=50, convert_unicode=True))
    base_requirement = db.Column(db.Text)
    begin_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    weight = db.Column(db.Integer)
    max_submit_attempts = db.Column(db.Integer)
    submissions = db.relationship('Submission', backref='homework')

    def __repr__(self):
        return '<Homework %r>' % self.id

    @property
    def order(self):
        return Homework.query.filter_by(course_id=self.course_id).all().index(self)

    @staticmethod
    def homework_list(course_id):
        homeworks = Homework.query.filter_by(course_id=course_id).all()
        order = 1
        for homework in homeworks:
            homework.order = order  #为返回的 homework 增加 order (顺序) 属性
            order += 1
        return homeworks


class Submission(db.Model):                       # 学生提交作业信息
    __tablename__ = 'submissions'
    id = db.Column(db.Integer, primary_key=True)
    homework_id = db.Column(db.Integer, db.ForeignKey('homework.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    submitter_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    text_content = db.Column(db.Text)
    score = db.Column(db.Integer)
    comments = db.Column(db.Text)
    submit_attempts = db.Column(db.Integer)
    submit_status = db.Column(db.Integer)  # 0: 提交未批改  1: 已批改

    def __repr__(self):
        return '<Submission %r>' % self.id


class Attachment(db.Model):                       # 学生提交作业附件信息
    __tablename__ = 'attachments'
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'))
    guid = db.Column(db.Text)
    file_name = db.Column(db.String(128))
    upload_time = db.Column(db.DateTime)
    status = db.Column(db.Boolean)
    submission = db.relationship('Submission', backref='attachment', uselist=False)

    def __repr__(self):
        return '<Attachment %r>' % self.id


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.id'))
    course_info = db.Column(db.Text)
    place = db.Column(db.String(50))
    outline = db.Column(db.Text)
    credit = db.Column(db.Integer)
    teamsize_max = db.Column(db.Integer)
    teamsize_min = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    upload_time = db.Column(db.String(128))
    students = db.relationship('Student', secondary=SCRelationship, backref='courses')
    teachers = db.relationship('Teacher', secondary=TCRelationship, backref='courses')
    no_miss = db.Column(db.Integer)
    miss_1 = db.Column(db.Integer)
    miss_2 = db.Column(db.Integer)
    miss_3 = db.Column(db.Integer)
    miss_4 = db.Column(db.Integer)
    miss_5 = db.Column(db.Integer)

    def __repr__(self):
        return '<Course %r>' % self.id


class CourseTime(db.Model):
    __tablename__ = 'course_time'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    start_week = db.Column(db.Integer)
    start_section = db.Column(db.Integer)
    finish_section = db.Column(db.Integer)

    def __repr__(self):
        return '<CourseTime %r>' % self.id


class Teacher(UserMixin, db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    teacher_info = db.Column(db.Text)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def init_teacher():
        teacher = Teacher.query.first()
        if teacher is None:
            teacher = Teacher(id=777)
            teacher.password = '777'
            db.session.add(teacher)
            db.session.commit()

    @staticmethod
    def user_type():
        return 1

    def __repr__(self):
        return '<Teacher %r>' % self.id


@login_manager.user_loader
def load_user(user_id):
    if 'user_type' not in session:
        return None
    elif session['user_type'] == 'dean':
        temp = DeanInfo.query.get(int(user_id))
    elif session['user_type'] == 'teacher':
        temp = Teacher.query.get(int(user_id))
    elif session['user_type'] == 'student':
        temp = Student.query.get(int(user_id))
    return temp


class ChatMessage(db.Model):
    __tablename__ = 'chat_message'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))  # 0 表示 invalid， 即不是学生发言，>0 表示发言者，即为学生发言
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))  # 同理，老师发言
    time = db.Column(db.DateTime)
    content = db.Column(db.String(256))  # 暂定256字
    markdown = db.Column(db.Boolean)
    student = db.relationship('Student', uselist=False)
    teacher = db.relationship('Teacher', uselist=False)

    def __repr__(self):
        return '<ChatMessage %r>' % self.id


class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    time_begin = db.Column(db.DateTime)  # 老师发布签到时间
    time_end = db.Column(db.DateTime)  # 在此时间内可以签到
    info = db.Column(db.Text)  # 写点啥

    def __repr__(self):
        return '<Attendance %r>' % self.id

    @property
    def order(self):
        return Attendance.query.filter_by(course_id=self.course_id).all().index(self)

    @staticmethod
    def attendance_list(course_id):
        attendances = Attendance.query.filter_by(course_id=course_id).all()
        order = 1
        for attendance in attendances:
            attendance.order = order  #为返回的 homework 增加 order (顺序) 属性
            order += 1
        return attendances


class AttendanceStats(db.Model):
    __tablename__ = 'attendance_stats'
    id = db.Column(db.Integer, primary_key=True)
    attendance_id = db.Column(db.Integer, db.ForeignKey('attendance.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    time = db.Column(db.DateTime)  # 学生签到时间点

    def __repr__(self):
        return '<AttendanceStats %r>' % self.id


# 加分项
class Plus(db.Model):
    __tablename__ = 'plus'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    name = db.Column(db.String(256))
    weight = db.Column(db.Integer)
    teams = db.relationship('TeamPlus', backref='plus')


class TeamPlus(db.Model):
    __tablename__ = 'team_plus'
    id = db.Column(db.Integer, primary_key=True)
    plus_id = db.Column(db.Integer, db.ForeignKey('plus.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    score = db.Column(db.Integer)
    team = db.relationship('Team', backref='teamplus', uselist=False)


