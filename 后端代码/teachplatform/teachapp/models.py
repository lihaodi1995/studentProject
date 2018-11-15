#-*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.

class User(models.Model):                                                   #用户模型
    username = models.CharField(max_length = 16, unique = True)                 #用户名(管理员用户名、教师工号、学生学号)
    password = models.CharField(max_length = 128, default = '000000')           #密码
    name = models.CharField(max_length = 8)                                     #真实姓名
    email = models.CharField(max_length = 48, unique = True, null = True)        #邮箱
    phone = models.CharField(max_length = 11, unique = True, null = True)       #手机号
    

class Admin(models.Model):                                              #管理员模型
    user = models.ForeignKey(User)                                          #用户外键

class Teacher(models.Model):                                            #教师模型
    user = models.ForeignKey(User)                                          #用户外键

class Student(models.Model):                                            #学生模型
    user = models.ForeignKey(User)                                          #用户外键

class Semester(models.Model):                                           #学期模型
    name = models.CharField(max_length = 24, unique = True)             #学期名称
    start_time = models.DateField()                                     #开始时间
    end_time = models.DateField()                                       #结束时间
    weeks = models.IntegerField()                                           #周次

class Course(models.Model):                                             #课程模型
    semester = models.ForeignKey(Semester)                                  #学期外键
    name = models.CharField(max_length = 24)                                #课程名称
    code = models.CharField(max_length = 8, unique = True)                  #课程代号
    credit = models.IntegerField()                                          #课程学分
    start_week = models.IntegerField()                                      #课程开始周次
    end_week = models.IntegerField()                                        #课程结束周次
    info = models.TextField(null = True)                                    #课程要求信息(上课地点等)
    description = models.TextField(null = True)                             #课程描述信息(课程大纲等)
    team_ddl = models.DateTimeField(default = datetime.now)                 #团队组建截止时间
    team_ubound = models.IntegerField(default = 10)                         #团队成员上限
    team_lbound = models.IntegerField(default = 1)                          #团队成员下限

class Team(models.Model):                                               #团队模型
    course = models.ForeignKey(Course)                                      #课程外键
    code = models.IntegerField(null = True)                                 #团队编号
    name = models.CharField(max_length = 16)                                #团队名称
    done = models.BooleanField(default = False)                             #团队组建是否完成
    verified = models.BooleanField(default = False)                         #团队验证是否通过
    members = models.IntegerField(default = 1)                              #团队人数

class Homework(models.Model):                                           #作业模型
    course = models.ForeignKey(Course)                                      #课程外键
    name = models.CharField(max_length = 24)                                #作业名称
    content = models.TextField(null = True)                                 #作业描述内容
    score = models.IntegerField()                                           #作业最大分值
    start_time = models.DateTimeField()                                     #作业开始时间
    end_time = models.DateTimeField()                                       #作业结束时间
    times = models.IntegerField()                                           #作业最大提交次数

class Message(models.Model):                                             #消息模型
    user_from = models.ForeignKey(User, related_name = 'user_from')         #发送方用户
    user_to = models.ForeignKey(User, related_name = 'user_to')             #接收方用户
    content = models.TextField(default = '')                                #消息内容
    judge = models.BooleanField(default = False)                            #判断消息是否读取
    time = models.DateTimeField(default = datetime.now)                     #消息发送时间

class Enroll(models.Model):                                             #学生-课程关系表
    student = models.ForeignKey(Student)                                    #学生外键
    course = models.ForeignKey(Course)                                      #课程外键
    
class Teach(models.Model):                                              #教师-课程关系表
    teacher = models.ForeignKey(Teacher)                                    #教师外键
    course = models.ForeignKey(Course)                                      #课程外键

class TeamMember(models.Model):                                         #团队-学生关系表
    student = models.ForeignKey(Student)                                    #学生外键
    team = models.ForeignKey(Team)                                          #团队外键
    role = models.CharField(max_length = 16)                                #学生在团队中的角色
    verified = models.BooleanField(default = False)                         #学生加队申请是否通过

class TeamHomework(models.Model):                                       #团队-作业关系表
    team = models.ForeignKey(Team)                                          #团队外键
    homework = models.ForeignKey(Homework)                                  #作业外键
    content = models.TextField(null = True)                                 #团队在线提交的文本内容
    time = models.DateTimeField()                                           #团队提交作业的时间
    score = models.IntegerField(null = True)                                #团队本次作业的得分
    comment = models.TextField(null = True)                                 #教师对作业的评语
    times = models.IntegerField(default = 1)                                #已提交次数

class Weight(models.Model):                                             #学生作业得分权重
    teamhomework = models.ForeignKey(TeamHomework)                          #团队-作业外键
    student = models.ForeignKey(Student)                                    #学生外键
    weight = models.FloatField(default = 0)                               #权重系数
    done = models.BooleanField(default = False)                             #学生是否完成组内评价

class Meta(models.Model):                                               #记录一些持久化数据
    key = models.CharField(max_length = 32, unique = True)                  #键
    value = models.TextField()                                              #值

class Relationship(models.Model):                                       #好友关系表
    user_a = models.ForeignKey(User, related_name = 'user_a')               #主动方
    user_b = models.ForeignKey(User, related_name = 'user_b')               #被动方
