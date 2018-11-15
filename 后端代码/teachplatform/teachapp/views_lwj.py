# -*- coding: utf-8 -*- 
from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import os
import xlrd
from teachapp.models import User, Admin, Teacher, Student, Meta, Course, Teach, TeamMember, Semester, Enroll, Relationship, Message
import json
from datetime import datetime
from django.contrib.sessions.models import Session
from importlib import import_module
from django.conf import settings
from django.db.models.query import QuerySet
from django.db.models import Q
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore

def setSemester(request):                                   
    if request.method == 'POST':
        request_type = request.POST['type'] 
        semester_name = request.POST['name']
        semester_start = request.POST['start_date']
        semester_end = request.POST['end_date']
        semester_weeks = request.POST['weeks']

        json_response = {}
        
        if request_type == 'new':
            try:
                semester = Semester.objects.get(name = semester_name)
                json_response['success'] = False
                json_response['error_msg'] = 'semester exist'
                return JsonResponse(json_response)
            except ObjectDoesNotExist:
                Semester.objects.create(name = semester_name, start_time = semester_start, end_time = semester_end, weeks = semester_weeks)
                basedir = os.path.dirname(__name__)
                dirname = os.path.join(basedir, semester_name)
                os.mkdir(dirname)
                json_response['success'] = True
                return JsonResponse(json_response)
        elif request_type == 'maintain':
            try:
                semester = Semester.objects.get(name = semester_name)
                semester.start_time = semester_start
                semester.end_time = semester_end
                semester.weeks = semester_weeks
                semester.save()
                json_response['success'] = True
                return JsonResponse(json_response)
            except ObjectDoesNotExist:
                json_response['success'] = False
                json_response['error_msg'] = 'semester not exist!'
                return JsonResponse(json_response)

def setCurrentSemester(request):
    if request.method == 'POST':
        semester_name = request.POST['name']

        json_response = {}

        try:
            meta = Meta.objects.get(key = 'current_semester')
            try:
                meta.value = semester_name
                meta.save()
                json_response['success'] = True
                return JsonResponse(json_response)
            except:
                json_response['success'] = False
                json_response['error_msg'] = 'modify current semester failed!'
                return JsonResponse(json_response)
        except ObjectDoesNotExist:
            try:
                Meta.objects.create(key = 'current_semester', value = semester_name)
                json_response['success'] = True
                return JsonResponse(json_response)
            except:
                json_response['success'] = False
                json_response['error_msg'] = 'create current semester failed!'
                return JsonResponse(json_response)

def getAllSemester(request):
    if request.method == 'GET':
        json_response = {}
        json_response['current_semester'] = []
        json_response['semester_list'] = []

        try:                                                     #get current semester
            current_semester_name = Meta.objects.get(key = 'current_semester').value
            current_semester = Semester.objects.get(name = current_semester_name)
            json_response['current_semester'].append(True)
            json_response['current_semester'].append(current_semester.name)
            json_response['current_semester'].append(current_semester.start_time)
            json_response['current_semester'].append(current_semester.end_time)
            json_response['current_semester'].append(current_semester.weeks)
        except:
            json_response['current_semester'].append(False)
            json_response['current_semester'].append('')

        try:                                                      #get semester list
            semester_list = Semester.objects.all()
            for semester_item in semester_list:
                semester = {}
                semester['name'] = semester_item.name
                semester['start_time'] = semester_item.start_time
                semester['end_time'] = semester_item.end_time
                semester['weeks'] = semester_item.weeks
                json_response['semester_list'].append(semester)
        except:
            pass
        
        return JsonResponse(json_response)

def getSemester(request):
    if request.method == 'POST':
        semester_name = request.POST['name']
        json_response = {}

        try:
            semester = Semester.objects.get(name = semester_name)
            json_response['name'] = semester.name
            json_response['start_time'] = semester.start_time
            json_response['end_time'] = semester.end_time
            json_response['weeks']= semester.weeks
            json_response['success'] = True
            return JsonResponse(json_response)
        except ObjectDoesNotExist:
            json_response['success'] = False
            json_response['error_msg'] = 'semester not exist'
            return JsonResponse(json_response)

def deleteSemester(request):
    if request.method == 'POST':
        semester_name = request.POST['name']
        json_response = {}

        try:
            semester = Semester.objects.get(name = semester_name)
            semester.delete()
            json_response['sueecss'] = True
        except ObjectDoesNotExist:
            json_response['success'] = False
            json_response['error_msg'] = 'delete failed!'

        try:
            current_semester_name = Meta.objects.get(key = 'current_semester').value
            if current_semester_name == semester_name:
                Meta.objects.get(key = 'current_semester').delete()
        except ObjectDoesNotExist:
            pass

        return JsonResponse(json_response)

def setCourse(request):
    if request.method == 'POST':
        request_type = request.POST['type']
        course_name = request.POST['name']
        course_code = request.POST['code']
        course_credit = request.POST['credit']
        course_start_week = request.POST['start_week']
        course_end_week = request.POST['end_week']
        course_info = request.POST['info']

        json_response = {}

        current_semester_name = Meta.objects.get(key = 'current_semester').value
        course_semester = Semester.objects.get(name = current_semester_name)
        if request_type == 'new':                                           #set new course
            try:
                course = Course.objects.get(code = course_code)
                json_response['success'] = False
                json_response['error_msg'] = 'course exist!'
                return JsonResponse(json_response)
            except ObjectDoesNotExist:
                Course.objects.create(name = course_name, code = course_code, credit = course_credit, semester = course_semester, start_week = course_start_week, end_week = course_end_week, info = course_info)
                basedir = os.path.dirname(__name__)
                semesterdir = os.path.join(basedir, current_semester_name)
                coursedir = os.path.join(semesterdir, course_code)
                os.mkdir(coursedir)
                json_response['success'] = True
                return JsonResponse(json_response) 
        if request_type == 'maintain':                                       #maintain course
            try:
                course = Course.objects.get(code = course_code)
                course.name = course_name
                course.code = course_code
                course.credit = course_credit
                course.start_week = course_start_week
                course.end_week = course_end_week
                course.info = course_info
                course.save()
                json_response['success'] = True
                return JsonResponse(json_response)
            except ObjectDoesNotExist:
                json_response['success'] = False
                json_response['error_msg'] = 'course not exist!'
                return JsonResponse(json_response)


def getCurrentSemesterWeeks(request):
    if request.method == 'GET':
        json_response = {}

        try:
            current_semester_name = Meta.objects.get(key = 'current_semester').value
            json_response['weeks'] = int(Semester.objects.get(name = current_semester_name).weeks)
            json_response['success'] = True
            return JsonResponse(json_response)
        except:
            json_response['success'] = False
            json_response['error_msg'] = 'semester not exist!'
            return JsonResponse(json_response)

def getAllCourse(request):
    if request.method == 'GET':
        json_response = {}
        json_response['course_list'] = []
        try:
            current_semester_name = Meta.objects.get(key = 'current_semester').value
            current_semester = Semester.objects.get(name = current_semester_name)
        except:
            json_response['success'] = False
            json_response['error_msg'] = 'semester not exist!'
            return JsonResponse(json_response)
        
        course_list = Course.objects.filter(semester = current_semester)
        for course_item in course_list:
            course = {}
            course['name'] = course_item.name
            course['code'] = course_item.code
            course['credit'] = course_item.credit
            course['start_week'] = course_item.start_week
            course['end_week'] = course_item.end_week
            c = Course.objects.get(code = course_item.code)
            teach = Teach.objects.filter(course = c)
            course['teacher_name'] = []
            for teach_item in teach:
                course['teacher_name'].append(teach_item.teacher.user.name)
            course['student_number'] = len(Enroll.objects.filter(course = c))
            json_response['course_list'].append(course)
        return JsonResponse(json_response)

def getCourse(request):
    if request.method == 'POST':
        course_code = request.POST['code']

        json_response = {}
        try:
            current_semester_name = Meta.objects.get(key = 'current_semester').value
            current_semester = Semester.objects.get(name = current_semester_name)
        except:
            json_response['success'] = False
            json_response['error_msg'] = 'semester not exist!'
            return JsonResponse(json_response)

        try:
            course = Course.objects.get(semester = current_semester, code = course_code)
            json_response['name'] = course.name
            json_response['code'] = course.code
            json_response['credit'] = course.credit
            json_response['start_week'] = course.start_week
            json_response['end_week'] = course.end_week
            json_response['info'] = course.info
            return JsonResponse(json_response)
        except :
            json_response['success'] = False
            json_response['error_msg'] = 'course not exist!'
            return JsonResponse(json_response)

def deleteCourse(request):
    if request.method == 'POST':
        course_code = request.POST['code']
        json_response = {}

        try:
            current_semester_name = Meta.objects.get(key = 'current_semester').value
            current_semester = Semester.objects.get(name = current_semester_name)
        except:
            json_response['success'] = False
            json_response['error_msg'] = 'semester not exist!'
            return JsonResponse(json_response)

        try:
            Course.objects.get(semester = current_semester, code = course_code).delete()
            json_response['success'] = True
            return JsonResponse(json_response)
        except ObjectDoesNotExist:
            json_response['success'] = False
            json_response['error_msg'] = 'delete failed!'
            return JsonResponse(json_response)

def importUserOfCourse(request):
    if request.method == 'POST':
        print request.POST
        request_member = request.POST['member']
        code = request.POST['code']
        fl = request.FILES.get('file')
        json_response = {}
        try:
            filename = write(fl)
        except:
            json_response['success'] = False
            json_response['error_msg'] = 'upload failed!'
            return JsonResponse(json_response)
        bk = xlrd.open_workbook(filename)
        try:
            sh = bk.sheet_by_name('Sheet1')
        except:
            json_response['success'] = False
            json_response['error_msg'] = 'sheet name error!'
            return JsonResponse(json_response)
        nrows = sh.nrows

        try:
            course = Course.objects.get(code = code)
        except:
            json_response['success'] = False
            json_response['error_msg'] = 'course not exist!'
            return JsonResponse(json_response)
        for i in range(1, nrows):
            try:
                username = sh.cell_value(i, 0)
            except:
                pass
            try:
                user = User.objects.get(username = username)
                if request_member == 'teacher':
                    try:
                        teacher = Teacher.objects.get(user = user)
                        if len(Teach.objects.filter(teacher = teacher, course = course)) == 0:
                            Teach.objects.create(teacher = teacher, course = course)
                    except:
                        pass
                elif request_member == 'student':
                    try:
                        student = Student.objects.get(user = user)
                        if len(Enroll.objects.filter(student = student, course = course)) == 0:
                            Enroll.objects.create(student = student, course = course)
                    except:
                        pass
            except:
                pass
        
        json_response['success'] = True
        return JsonResponse(json_response)

def getUserOfCourse(request):
    if request.method == 'POST':
        code = request.POST['code']
        json_response = {}
        json_response['teacher_list'] = []
        json_response['student_list'] = []

        try:
            course = Course.objects.get(code = code)
        except:
            json_response['success'] = False
            json_response['error_msg'] = 'course not exist!'
            return JsonResponse(json_response)
        teach = Teach.objects.filter(course = course)
        for teach_item in teach:
            teacher = {}
            teacher['name'] = teach_item.teacher.user.name
            teacher['username'] = teach_item.teacher.user.username
            json_response['teacher_list'].append(teacher)
        enroll = Enroll.objects.filter(course = course)
        for enroll_item in enroll:
            student = {}
            student['name'] = enroll_item.student.user.name
            student['username'] = enroll_item.student.user.username
            json_response['student_list'].append(student)
        
        return JsonResponse(json_response)
        
def deleteUserOfCourse(request):
    if request.method == 'POST':
        member = request.POST['member']
        username = request.POST['username']
        code = request.POST['code']
        json_response = {}

        try:
            course = Course.objects.get(code = code)
        except:
            json_response['success'] = False
            json_response['error_msg'] = 'course not exist!'
            return JsonResponse(json_response)
        if member == 'teacher':
            try:
                teacher = Teacher.objects.get(user = User.objects.get(username = username))
            except:
                json_response['success'] = False
                json_response['error_msg'] = 'teacher not exist!'
                return JsonResponse(json_response)
            try:
                Teach.objects.get(teacher = teacher, course = course).delete()
            except:
                json_response['success'] = False
                json_response['error_msg'] = 'delete teacher failed!'
                return JsonResponse(json_response)
        
        if member == 'student':
            try:
                student = Student.objects.get(user = User.objects.get(username = username))
            except:
                json_response['success'] = False
                json_response['error_msg'] = 'student not exist!'
                return JsonResponse(json_response)
            try:
                Enroll.objects.get(student = student, course = course).delete()
            except:
                json_response['success'] = False
                json_response['error_msg'] = 'delete student failed!'
                return JsonResponse(json_response)
        
        json_response['success'] = True
        return JsonResponse(json_response)


def setUser(request):
    if request.method == 'POST':
        request_type = request.POST['type']
        request_member = request.POST['member']
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']

        json_response = {}

        if request_type == 'new': 
            if len(User.objects.filter(username = username)) > 0:
                json_response['success'] = False
                json_response['error_msg'] = 'username exist!'
                return JsonResponse(json_response)
            if len(User.objects.filter(email = email)) > 0:
                json_response['success'] = False
                json_response['error_msg'] = 'email exist!'
                return JsonResponse(json_response)
            if len(User.objects.filter(phone = phone)) > 0:
                json_response['success'] = False
                json_response['error_msg'] = 'phone exist!'
                return JsonResponse(json_response)

            if password == '':
                password = '000000' 
            try:
                User.objects.create(username = username, password = password, name = name, email = email, phone = phone)
            except:
                json_response['success'] = False
                json_response['error_msg'] = 'create user failed!'
                return JsonResponse(json_response)

            if request_member == 'teacher':
                try:
                    user = User.objects.get(username = username)
                    Teacher.objects.create(user = user)
                    json_response['success'] = True
                    return JsonResponse(json_response)
                except:
                    json_response['success'] = False
                    json_response['error_msg'] = 'create teacher failed!'
                    return JsonResponse(json_response)
            if request_member == 'student':
                try:
                    user = User.objects.get(username = username)
                    Student.objects.create(user = user)
                    json_response['success'] = True
                    return JsonResponse(json_response)
                except:
                    json_response['success'] = False
                    json_response['error_msg'] = 'create student failed!'
                    return JsonResponse(json_response)

        if request_type == 'maintain':
            try:
                user = User.objects.get(username = username)
            except:
                json_response['success'] = False
                json_response['error_msg'] = 'user not exist!'
                return JsonResponse(json_response)

            if user.email != email and len(User.objects.filter(email = email)) > 0:
                json_response['success'] = False
                json_response['error_msg'] = 'email exist!'
                return JsonResponse(json_response)
            if user.phone != phone and len(User.objects.filter(phone = phone)) > 0:
                json_response['success'] = False
                json_response['error_msg'] = 'phone exist!'
                return JsonResponse(json_response)
                
            try:
                user.name = name
                user.email = email
                user.phone = phone
                user.save()
                json_response['success'] = True
                return JsonResponse(json_response)
            except:
                json_response['success'] = False
                json_response['error_msg'] = 'modify user failed!'
                return JsonResponse(json_response)

def getAllUser(request):
    if request.method == 'POST':
        request_member = request.POST['member']
        json_response = {}

        if request_member == 'teacher':
            json_response['teacher_list'] = []
            teacher_list = Teacher.objects.all()
            for teacher_item in teacher_list:
                teacher = {}
                teacher['name'] = teacher_item.user.name
                teacher['username'] = teacher_item.user.username
                teacher['email'] = teacher_item.user.email
                teacher['phone'] = teacher_item.user.phone
                json_response['teacher_list'].append(teacher)
            
            return JsonResponse(json_response)

        if request_member == 'student':
            json_response['student_list'] = []
            student_list = Student.objects.all()
            for student_item in student_list:
                student = {}
                student['name'] = student_item.user.name
                student['username'] = student_item.user.username
                student['email'] = student_item.user.email
                student['phone'] = student_item.user.phone
                json_response['student_list'].append(student)
            
            return JsonResponse(json_response)

def getUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        json_response = {}

        try:
            user = User.objects.get(username = username)
            json_response['name'] = user.name
            json_response['username'] = user.username
            json_response['email'] = user.email
            json_response['phone'] = user.phone
            return JsonResponse(json_response)
        except:
            json_response['success'] = False
            json_response['error_msg'] = 'user not exist!'
            return JsonResponse(json_response)

def deleteUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        request_member = request.POST['member']
        json_response = {}

        try:
            user = User.objects.get(username = username)
        except ObjectDoesNotExist:
            json_response['success'] = False
            json_response['error_msg'] = 'user not exist!'
            return JsonResponse(json_response)

        if request_member == 'teacher':
            try:
                teacher = Teacher.objects.get(user = user)
            except ObjectDoesNotExist:
                json_response['success'] = False
                json_response['error_msg'] = 'teacher not exist!'
                return JsonResponse(json_response)
            try:
                teacher.delete()
                user.delete()
                json_response['success'] = True
                return JsonResponse(json_response)
            except:
                json_response['success'] = False
                json_response['error_msg'] = 'delete teacher failed!'
                return JsonResponse(json_response)
        if request_member == 'student':
            try:
                student = Student.objects.get(user = user)
            except ObjectDoesNotExist:
                json_response['success'] = False
                json_response['error_msg'] = 'student not exist!'
                return JsonResponse(json_response)
            try:
                student.delete()
                user.delete()
                json_response['success'] = True
                return JsonResponse(json_response)
            except:
                json_response['success'] = False
                json_response['error_msg'] = 'delete student failed!'
                return JsonResponse(json_response)

def importUser(request):
    if request.method == 'POST':
        if request.FILES.keys()[0] == 'teacher':
            fl = request.FILES.get('teacher')
        elif request.FILES.keys()[0] == 'student':
            fl = request.FILES.get('student')

        json_response = {}
        json_response['success'] = True

        try:
            filename = write(fl)
        except:
            json_response['success'] = False
            json_response['error_msg'] = 'upload failed!'
            return JsonResponse(json_response)
            
        bk = xlrd.open_workbook(filename)
        try:
            sh = bk.sheet_by_name('Sheet1')
        except:
            json_response['success'] = False
            json_response['error_msg'] = 'sheet name error'
            return JsonResponse(json_response)
        nrows = sh.nrows

        for i in range(1, nrows):
            try:
                username = sh.cell_value(i, 0)
                name = sh.cell_value(i, 1)
                email = sh.cell_value(i, 2)
                phone = sh.cell_value(i, 3)
            except:
                json_response['success'] = False
                json_response['error_msg'] = 'read message error!'
                return JsonResponse(json_response)
            try:
                user = User.objects.get(username= username)
                user.name = name
                if email != user.email and len(User.objects.filter(email = email)) == 0:
                    user.email = email
                if phone != user.phone and len(User.objects.filter(phone = phone)) == 0:
                    user.phone = phone
                user.save()
            except:
                if len(User.objects.filter(email = email)) > 0:
                    email = None
                if len(User.objects.filter(phone = phone)) > 0:
                    phone = None
                User.objects.create(username = username, name = name, email = email, phone = phone)
                user = User.objects.get(username = username)
                if request.FILES.keys()[0] == 'teacher':
                    Teacher.objects.create(user = user)
                elif request.FILES.keys()[0] == 'student':
                    Student.objects.create(user = user)
        
        os.remove(filename)
        return JsonResponse(json_response)

def importCourse(request):
    if request.method == 'POST':
        fl = request.FILES.get('file')

        json_response = {}

        try:
            filename = write(fl)
        except:
            json_response['success'] = False
            json_response['error_msg'] = 'upload failed!'
            return JsonResponse(json_response)

        bk = xlrd.open_workbook(filename)
        try:
            sh = bk.sheet_by_name('Sheet1')
        except:
            json_response['success'] = False
            json_response['error_msg'] = 'sheet name error'
            return JsonResponse(json_response)
        nrows = sh.nrows

        try:
            current_semester_name = Meta.objects.get(key = 'current_semester').value
            current_semester = Semester.objects.get(name = current_semester_name)
        except:
            json_response['success'] = False
            json_response['error_msg'] = 'semester not exist!'
            return JsonResponse(json_response)
        
        for i in range(1, nrows):
            try:
                name = sh.cell_value(i, 0)
                code = sh.cell_value(i, 1)
                credit = int(sh.cell_value(i, 2))
                semester = current_semester
                start_week = int(sh.cell_value(i, 3))
                start_week = min(start_week, current_semester.weeks)
                end_week = int(sh.cell_value(i, 4))
                end_week = min(end_week, current_semester.weeks)
                info = sh.cell_value(i, 5)
            except:
                json_response['success'] = False
                json_response['error_msg'] = 'read message error'
                return JsonResponse(json_response)
            try:
                course = Course.objects.get(code = code)
                course.name = name
                course.credit = credit
                course.start_week = start_week
                course.end_week = end_week
                course.info = info
                course.save()   
            except:
                Course.objects.create(name = name, code = code, credit = credit, semester = semester, start_week = start_week, end_week = end_week, info = info)
                basedir = os.path.dirname(__name__)
                semesterdir = os.path.join(basedir, current_semester_name)
                coursedir = os.path.join(semesterdir, code)
                os.mkdir(coursedir)

        os.remove(filename)
        json_response['success'] = True
        return JsonResponse(json_response)


def write(fl):
    basedir = os.path.dirname(__name__)
    filedir = os.path.join(basedir, 'static')
    filename = os.path.join(filedir, fl.name)

    try:
        file_des = open(filename,'wb')
        for chrunk in fl.chunks():
            file_des.write(chrunk)
        file_des.close()
        return filename
    except:
        raise Exception()

def searchUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        json_response = {}
        json_response['user_list'] = []

        user_list = User.objects.filter(username__contains = username)
        for user_item in user_list:
            user = {}
            user['name'] = user_item.name
            user['username'] = user_item.username
            json_response['user_list'].append(user)

        json_response['success'] = True
        return JsonResponse(json_response)


def addRelationship(request):
    if request.method == 'POST':
        user_a_username = request.POST['user_a_username']
        user_b_username = request.POST['user_b_username']
        json_response = {}
        json_response['success'] = False

        try:
            user_a = User.objects.get(username = user_a_username)
        except:
            json_response['error_msg'] = 'user_a not exist!'
            return JsonResponse(json_response)
        try:
            user_b = User.objects.get(username = user_b_username)
        except:           
            json_response['error_msg'] = 'user_b not exist!'
            return JsonResponse(json_response)

        try:
            Relationship.objects.get(user_a = user_a, user_b = user_b)
            json_response['error_msg'] = '好友已存在!'
        except:
            Relationship.objects.create(user_a = user_a, user_b = user_b)

        json_response['success'] = True
        return JsonResponse(json_response)

def getRelationship(request):
    if request.method == 'POST':
        username = request.POST['username']
        json_response = {}
        json_response['user_list'] = []

        try:
            user = User.objects.get(username = username)
        except:
            json_response['success'] = False
            json_response['error_msg'] = 'user not exist!'
            return JsonResponse(json_response)

        relationship_list = Relationship.objects.filter(user_a = user)
        for relationship_item in relationship_list:
            user = {}
            user['name'] = User.objects.get(username = relationship_item.user_b.username).name
            user['username'] = User.objects.get(username = relationship_item.user_b.username).username
            json_response['user_list'].append(user)

        json_response['success'] = True
        return JsonResponse(json_response)

def deleteRelationship(request):
    if request.method == 'POST':
        user_a_username = request.POST['user_a_username']
        user_b_username = request.POST['user_b_username']
        json_response = {}
        json_response['success'] = False

        try:
            user_a = User.objects.get(username = user_a_username) 
        except:
            json_response['error_msg'] = 'user_a not exist!'
            return JsonResponse(json_response)
        try:
            user_b = User.objects.get(username = user_b_username) 
        except:
            json_response['error_msg'] = 'user_b not exist!'
            return JsonResponse(json_response)
        
        try:
            relationship = Relationship.objects.get(user_a = user_a, user_b = user_b)
        except:
            json_response['error_msg'] = 'relationship not exist!'
            return JsonResponse(json_response)
        try:
            relationship.delete()
        except:
            json_response['error_msg'] = 'delete failed!'
            return JsonResponse(json_response)

        json_response['success'] = True
        return JsonResponse(json_response)

def sendMessage(request):
    if request.method == 'POST':
        user_from_username = request.POST['user_from_username']
        user_to_username = request.POST['user_to_username']
        content = request.POST['content']
        json_response = {}
        json_response['success'] = False

        message_time = datetime.now()

        try:
            user_from = User.objects.get(username = user_from_username)
            user_to = User.objects.get(username = user_to_username)
        except:
            json_response['error_msg'] = 'user not exist!'
            return JsonResponse(json_response)
        
        try:
            Message.objects.create(user_from = user_from, user_to = user_to, content = content, time = message_time)
        except:
            json_response['error_msg'] = 'send failed!'
            return JsonResponse(json_response)

        json_response['success'] = True
        return JsonResponse(json_response)

def getNewMessage(request):
    if request.method == 'POST':
        username = request.POST['username']
        json_response = {}
        json_response['success'] = False
        json_response['user_list'] = []

        try:
            user_to = User.objects.get(username = username)
        except:
            json_response['error_msg'] = 'user not exist!'
            return JsonResponse(json_response)
        
        username_list = []
        message_list = Message.objects.filter(user_to = user_to, judge = False)
        for message_item in message_list:
            if message_item.user_from.username not in username_list:
                username_list.append(message_item.user_from.username)
        
        for username_item in username_list:
            user_from = {}
            user_from['name'] = None
            user_from['username'] = username_item
            user_from['content'] = []
            user_from['time'] = []
            json_response['user_list'].append(user_from)

        message_list = Message.objects.filter(user_to = user_to, judge = False)
        for message_item in message_list:
            for i in range(0, len(json_response['user_list'])):
                if message_item.user_from.username == json_response['user_list'][i]['username']:
                    json_response['user_list'][i]['name'] = message_item.user_from.name
                    json_response['user_list'][i]['content'].append(message_item.content)
                    json_response['user_list'][i]['time'].append(message_item.time.strftime('%Y-%m-%d %H:%M:%S'))

        json_response['success'] = True
        return JsonResponse(json_response)

def getAllMessage(request):
    if request.method == 'POST':
        user_from_username = request.POST['user_from_username']
        user_to_username = request.POST['user_to_username']
        json_response = {}
        json_response['success'] = False
        json_response['message_list'] = []

        try:
            user_from = User.objects.get(username = user_from_username)
            user_to = User.objects.get(username = user_to_username)
        except:
            json_response['error_msg'] = 'user not exist!'
            return JsonResponse(json_response)

        message_list = Message.objects.filter(Q(user_from = user_from, user_to = user_to) | Q(user_from = user_to, user_to = user_from)).order_by('time')
        for message_item in message_list:
            message = {}
            if user_from == message_item.user_from:
                message['left'] = True
            else:
                message['left'] = False
            message['content'] = message_item.content
            message['time'] = message_item.time.strftime('%Y-%m-%d %H:%M:%S')
            json_response['message_list'].append(message)
        
        json_response['success'] = True
        return JsonResponse(json_response)

def read(request):
    if request.method == 'POST':
        user_from_username = request.POST['user_from_username']
        user_to_username = request.POST['user_to_username']
        json_response = {}
        json_response['success'] = False

        try:
            user_from = User.objects.get(username = user_from_username)
            user_to = User.objects.get(username = user_to_username)
        except:
            json_response['error_msg'] = 'uer not exist!'
            return JsonResponse(json_response)

        message_list = Message.objects.filter(user_from = user_from, user_to = user_to, judge = False).update(judge = True)

        json_response['success'] = True
        return JsonResponse(json_response)
