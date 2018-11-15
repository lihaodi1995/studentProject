#-*- coding:utf-8 -*-
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.servers.basehttp import FileWrapper
from django.utils.encoding import smart_str
import os
import humanfriendly
import time
from datetime import datetime
import shutil
import tempfile
import glob
import zipfile
import StringIO
import xlwt

from importlib import import_module
from django.conf import settings
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore

from teachapp.models import User, Teacher, Course, Student, Semester, Meta, Teach, Enroll, Team, TeamMember, Homework, TeamHomework, Weight

# Create your views here.

def login(request):
    # return status code:
        # 0 -- success
        # 1 -- error
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        s = None
        try:
            s = SessionStore(session_key = request.POST['session_key']) 
        except:
            s = SessionStore()
            s['username'] = username
            s.create()

        final_response = {}

        user = None
        try:
            user = User.objects.get(username = username)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        if user.password == password:
            final_response['status'] = 0
            final_response['name'] = user.name
        else:
            final_response['status'] = 1

        final_response['session_key'] = s.session_key
        return JsonResponse(final_response)

def get_course_list_teacher(request):
    # return 2 course lists(current & previous), each course contains:
        # name, code, semester, student_count, teacher_name
    # return status code:
        # 0 -- success
        # 1 -- object not found error
        # 2 -- session expired error
    if request.method == 'POST':
        final_response = {}

        session = get_session(request.POST['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        username = session['username']
        
        current_semester = get_current_semester()

        user = None
        teacher = None
        try:
            user = User.objects.get(username = username)
            teacher = Teacher.objects.get(user = user)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        teach_list = Teach.objects.filter(teacher = teacher)

        current_course = []
        previous_course = []
        for teach in teach_list:
            course_dict = {}
            course = Course.objects.get(id = teach.course.id)
            course_dict['name'] = course.name
            course_dict['code'] = course.code
            course_dict['semester'] = Semester.objects.get(id = course.semester.id).name
            #get student count
            student_count = 0
            try:
                student_count = Enroll.objects.filter(course = course).count()
            except ObjectDoesNotExist:
                pass
            course_dict['student_count'] = student_count
            #get teacher name
            course_teacher = Teach.objects.filter(course = course)
            teacher_name_list = []
            for ct in course_teacher:
                teacher_name = Teacher.objects.get(id = ct.teacher.id).user.name
                teacher_name_list.append(teacher_name)
            teacher_name_str = u'，'.join(teacher_name_list)    
            course_dict['teacher_name'] = teacher_name_str

            if course.semester == current_semester:
                current_course.append(course_dict)
            else:
                previous_course.append(course_dict)
        final_response['current'] = current_course
        final_response['previous'] = previous_course
        final_response['status'] = 0
        return JsonResponse(final_response)

def get_course_info_teacher(request):
    # return an json object contains course detailed information:
        # name, code, credit, semester, start_week, end_week, student_count, teacher_name, info, description, outline
    # return status code:
        # 0 -- success
        # 1 -- object not found error
        # 2 -- session expired error
    if request.method == 'POST':
        course_code = request.POST['code']
        
        final_response = {}

        session = get_session(request.POST['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        session['course_code'] = course_code
        session.save()

        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        course_dict = {}
        course_dict['name'] = course.name
        course_dict['code'] = course.code
        course_dict['credit'] = course.credit
        course_dict['semester'] = Semester.objects.get(id = course.semester.id).name
        course_dict['start_week'] = course.start_week
        course_dict['end_week'] = course.end_week
        #get student count
        student_count = 0
        try:
            student_count = Enroll.objects.filter(course = course).count()
        except ObjectDoesNotExist:
            pass
        course_dict['student_count'] = student_count
        #get teacher name
        course_teacher = Teach.objects.filter(course = course)
        teacher_name_list = []
        for ct in course_teacher:
            teacher_name = Teacher.objects.get(id = ct.teacher.id).user.name
            teacher_name_list.append(teacher_name)
        teacher_name_str = ', '.join(teacher_name_list)    
        course_dict['teacher_name'] = teacher_name_str
        course_dict['info'] = course.info
        course_dict['description'] = course.description
        course_dict['team_ddl'] = course.team_ddl
        course_dict['team_ubound'] = course.team_ubound
        course_dict['team_lbound'] = course.team_lbound
        # load outline.html
        outline_path = get_base_dir() + '/' + course.semester.name + '/' + course.name + '/' + 'outline.html'
        if os.path.exists(outline_path):
            lines = []
            with open(outline_path, 'rb') as f:
                lines = f.readlines()
            course_dict['outline'] = ''.join(lines)

        final_response['course_info'] = course_dict
        final_response['status'] = 0
        return JsonResponse(final_response)

def edit_course_info_teacher(request):
    # return status code
        # 0 -- success
        # 1 -- object not found error
        # 2 -- session expired error
    if request.method == 'POST':
        course_info = request.POST.get('info', None)
        course_description = request.POST.get('description', None)
        course_outline = request.POST.get('outline', None)
        course_outline_file = request.FILES.get('outline', None)
        course_team_ddl = request.POST.get('team_ddl', None)
        course_team_ubound = request.POST.get('team_ubound', None)
        course_team_lbound = request.POST.get('team_lbound', None)

        final_response = {}

        session = get_session(request.POST['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']

        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)
        if course_info != None:
            course.info = course_info
        if course_description != None:
            course.description = course_description
        if course_team_ddl != None:
            course.team_ddl = course_team_ddl
        if course_team_ubound != None:
            course.team_ubound = course_team_ubound
        if course_team_lbound != None:
            course.team_lbound = course_team_lbound

        if course_outline != None:
            outline = request.POST['outline']
            outline_path = get_base_dir() + '/' + course.semester.name + '/' + course.name + '/' + 'outline.html'
            with open(outline_path, 'wb') as f:
                f.write(outline)
        elif course_outline_file != None:
            outline_file = request.FILES['outline']
            outline_path = get_base_dir() + '/' + course.semester.name + '/' + course.name + '/' + 'outline.html'
            save_inmemory_file(outline_file, outline_path)
        else:
            pass
        course.save()
        final_response['status'] = 0
        return JsonResponse(final_response)

def view_course_resource_teacher(request):
    # return an json object contains:
        # a file list of files in current path:
            # name, size(file only), modified(modify time)
        # base url
        # status code:
            # 0 -- success
            # 1 -- object not found error
            # 2 -- session expired error
            # 3 -- path not exist error
    if request.method == 'POST':
        resource_relpath = request.POST['relpath']

        final_response = {}

        session = get_session(request.POST['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']

        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        current_base = get_base_dir() + '/' + course.semester.name + '/' + course.name + '/' + 'resources'
        resource_abspath = current_base + resource_relpath
        
        if not os.path.exists(resource_abspath):
            final_response['status'] = 3
            return JsonResponse(final_response)

        file_list_current_dir = []
        file_name_list = os.listdir(resource_abspath)
        for file_name in file_name_list:
            file_dict = {}
            file_abs_path = os.path.join(resource_abspath, file_name)
            file_dict['name'] = file_name
            if os.path.isfile(file_abs_path):
                file_dict['size'] = humanfriendly.format_size(os.stat(file_abs_path).st_size)
            struct_time = time.gmtime(os.path.getmtime(file_abs_path))
            format_time = '%s/%s/%s %s:%s' % (struct_time.tm_year, struct_time.tm_mon, struct_time.tm_mday, struct_time.tm_hour, struct_time.tm_min);
            file_dict['modified'] = format_time
            file_list_current_dir.append(file_dict)
        final_response['contents'] = file_list_current_dir
        final_response['base_url'] = '/root' + '/' + course.semester.name + '/' + course.name + '/' + 'resources'
        final_response['status'] = 0
        return JsonResponse(final_response)

def upload_course_resource_teacher(request):
    # status code:
        # 0 -- success
        # 1 -- object not found error
        # 2 -- session expired error
        # 3 -- path not exist error
    if request.method == 'POST':
        resource_file = request.FILES['resource']
        resource_relpath = request.POST['relpath']

        final_response = {}

        session = get_session(request.POST['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']

        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        current_base = get_base_dir() + '/' + course.semester.name + '/' + course.name + '/' + 'resources'
        resource_abspath = current_base + resource_relpath
        
        if not os.path.exists(resource_abspath):
            final_response['status'] = 2
            return JsonResponse(final_response)
        
        save_inmemory_file(resource_file, resource_abspath + '/' + resource_file.name)

        final_response['status'] = 0
        return JsonResponse(final_response)

def delete_course_resource_teacher(request):
    # status code:
        # 0 -- success
        # 1 -- object not found error
        # 2 -- session expired error
        # 3 -- path not exist error
    if request.method == 'POST':
        file_list = request.POST.getlist('contents[]')
        print file_list
        file_relpath = request.POST['relpath']

        final_response = {}
        
        session = get_session(request.POST['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']
        
        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        for file_name in file_list:
            file_abspath = get_base_dir() + '/' + course.semester.name + '/' + course.name + '/' + 'resources' + file_relpath + '/' + file_name
            print file_abspath
            if os.path.exists(file_abspath):
                if os.path.isfile(file_abspath):
                    os.remove(file_abspath)
                else:
                    shutil.rmtree(file_abspath)
        final_response['status'] = 0
        return JsonResponse(final_response)

def create_directory_teacher(request):
    # status code:
        # 0 -- success
        # 1 -- object not exist error
        # 2 -- session expired error
        # 3 -- directory exsits error
    if request.method == 'POST':
        relpath = request.POST['relpath']
        dirname = request.POST['dirname']
        
        final_response = {}

        session = get_session(request.POST['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']

        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        current_base = get_base_dir() + '/' + course.semester.name + '/' + course.name + '/' + 'resources'
        current_dir = current_base + relpath
        new_dir = current_dir + '/' + dirname
        if os.path.exists(new_dir):
            final_response['status'] = 3
            return JsonResponse(final_response)
        os.mkdir(new_dir)
        final_response['status'] = 1
        return JsonResponse(final_response)

def get_student_list_teacher(request):
    # return a student list contains:
        # name, username
    # status code:
        # 0 -- success
        # 1 -- object not exist error
        # 2 -- session expired error
    if request.method == 'POST':
        final_response = {}
        '''
        session = get_session(request.POST['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']
        '''
        course_code = 'se002'
        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        student_list = []
        try:
            enroll_list = Enroll.objects.filter(course = course)
            for enroll in enroll_list:
                student = Student.objects.get(id = enroll.student.id)
                student_dict = {}
                student_dict['name'] = student.user.name
                student_dict['username'] = student.user.username
                if student.user.phone == None:
                    student_dict['phone'] = ''
                else:
                    student_dict['phone'] = student.user.phone
                if student.user.email == None:
                    student_dict['email'] = ''
                else:
                    student_dict['email'] = student.user.email
                student_dict['score'] = cal_student_total_score(student, course)
                student_list.append(student_dict)
        except ObjectDoesNotExist:
            pass

        final_response['student_list'] = student_list
        final_response['status'] = 0
        return JsonResponse(final_response)

def cal_student_total_score(student, course):
    team_obj_list = Team.objects.filter(course = course)
    team = None
    for team_obj in team_obj_list:
        try:
            team_member = TeamMember.objects.get(team = team_obj, student = student)
            team = team_obj
            break
        except:
            pass
    team_homework_list = TeamHomework.objects.filter(team = team)
    weighted_score = 0
    total_score = 0
    for team_homework in team_homework_list:
        total_score = total_score + team_homework.score
        weight = None
        try:
            weight = Weight.objects.get(student = student, teamhomework = team_homework)
        except:
            return 0
        weighted_score = weighted_score + weight.weight * team_homework.score
    return (float)(weighted_score) / total_score * 100

def get_team_list_teacher(request):
    # return 3 team list:
        # verified team list:
        # unverified team list:
            # name, code, members
        # student list:
            # name, username
    # status code:
        # 0 -- success
        # 1 -- object not exist error
        # 2 -- session expired error
    if request.method == 'POST':
        final_response = {}

        session = get_session(request.POST['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']

        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        verified_team = []
        unverified_team = []
        try:
            team_list = Team.objects.filter(course = course)
            for team in team_list:
                team_dict = {}
                team_dict['name'] = team.name
                if team.code != None:
                    team_dict['code'] = team.code
                team_dict['members'] = team.members
                if team.verified == True:
                    verified_team.append(team_dict)
                else:
                    unverified_team.append(team_dict)
        except ObjectDoesNotExist:
            pass

        student_list = Student.objects.all()
        team_list = Team.objects.filter(course = course)
        student_info_list = []
        for student in student_list:
            flag = False
            for team in team_list:
                try:
                    team_member = TeamMember.objects.get(student = student, team = team, verified = True)
                    flag = True
                    break
                except ObjectDoesNotExist:
                    pass
            if not flag:
                student_dict = {}
                student_dict['name'] = student.user.name
                student_dict['username'] = student.user.username
                student_info_list.append(student_dict)
        final_response['verified'] = verified_team
        final_response['unverified'] = unverified_team
        final_response['student'] = student_info_list
        final_response['ddl'] = (course.team_ddl <= datetime.today())
        final_response['status'] = 0
        return JsonResponse(final_response)

def get_team_member_teacher(request):
    # return a team member list contains:
        # name, username
    # status code:
        # 0 -- success
        # 1 -- object not exist error
        # 2 -- session expired error
    if request.method == 'POST':
        team_name = request.POST['name']

        final_response = {}

        session = get_session(request.POST['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']

        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        team = None
        try:
            team = Team.objects.get(course = course, name = team_name)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        team_member_list = TeamMember.objects.filter(team = team)
        student_list = []
        for team_member in team_member_list:
            student = Student.objects.get(id = team_member.student.id)
            student_dict = {}
            student_dict['name'] = student.user.name
            student_dict['username'] = student.user.username
            student_dict['role'] = team_member.role
            student_list.append(student_dict)
        final_response['team_member'] = student_list
        final_response['status']  =0
        return JsonResponse(final_response)

def edit_team_member_teacher(request):
    # status code:
        # 0 -- success
        # 1 -- object not exist error
        # 2 -- session expired error
    if request.method == 'POST':
        username = request.POST['username']
        from_team_name = request.POST.get('from', None)
        to_team_name = request.POST['to']

        final_response = {}

        session = get_session(request.POST['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']

        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        try:
            user = User.objects.get(username = username)
            student = Student.objects.get(user = user)
            to_team = Team.objects.get(name = to_team_name)
            if from_team_name != None:
                from_team = Team.objects.get(name = from_team_name)
                team_member = TeamMember.objects.get(student = student, team = from_team)
                team_member.team = to_team
                team_member.save()
                from_team.members = from_team.members - 1
                from_team.save()
                to_team.members = to_team.members + 1
                to_team.save()
            else:
                team_member = TeamMember()
                team_member.role = 'dev'
                team_member.verified = True
                team_member.student = student
                team_member.team = to_team
                team_member.save()
                to_team.members = to_team.members + 1
                to_team.save()
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        final_response['status'] = 0
        return JsonResponse(final_response)

def agree_team_application_teacher(request):
    # status code:
        # 0 -- success
        # 1 -- object not found error
        # 2 -- session expired error
    if request.method == 'POST':
        team_name = request.POST['name']
        
        final_response = {}
        '''
        session = get_session(request.POST['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']
        '''
        course_code = 'se002' 
        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        team = Team.objects.get(course = course, name = team_name)
        verified_team_num = Team.objects.filter(course = course, verified = True).count()
        team.verified = True
        team.code = verified_team_num + 1
        team.save()

        final_response['status'] = 0
        return JsonResponse(final_response)

def reject_team_application_teacher(request):
    # status code:
        # 0 -- success
        # 1 -- obeject not found error
        # 2 -- session expired error
    if request.method == 'POST':
        team_name = request.POST['name']
        
        final_response = {}
        
        session = get_session(request.POST['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']
        
        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        team = Team.objects.get(course = course, name = team_name)
        TeamMember.objects.filter(team = team).delete()
        team.delete()

        final_response['status'] = 0
        return JsonResponse(final_response)
    
def get_homework_list_teacher(request):
    # return a homework list contains:
        # name, score, start_time, end_time, times
    # status code:
        # 0 -- success
        # 1 -- object not found error
        # 2 -- session expired error
    if request.method == 'POST':
        final_response = {}

        session = get_session(request.POST['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']

        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        homework_list = []
        try:
            homework_obj_list = Homework.objects.filter(course = course)
            for homework in homework_obj_list:
                homework_dict = {}
                homework_dict['name'] = homework.name
                homework_dict['score'] = homework.score
                homework_dict['start_time'] = homework.start_time
                homework_dict['end_time'] = homework.end_time
                homework_dict['times'] = homework.times
                homework_list.append(homework_dict)
        except ObjectDoesNotExist:
            pass

        final_response['homework_list'] = homework_list
        final_response['status'] = 0
        return JsonResponse(final_response)

def get_homework_info_teacher(request):
    # return a homework object contains:
        # name, content, score, start_time, end_time, times
    # status code:
        # 0 -- success
        # 1 -- object not found error
        # 2 -- session expired error
    if request.method == 'POST':
        homework_name = request.POST['name']

        final_response = {}

        session = get_session(request.POST['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']
        session['homework_name'] = homework_name
        session.save()

        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        homework = Homework.objects.get(course = course, name = homework_name)
        homework_dict = {}
        homework_dict['name'] = homework.name
        homework_dict['content'] = homework.content
        homework_dict['score'] = homework.score
        homework_dict['start_time'] = homework.start_time
        homework_dict['end_time'] = homework.end_time
        homework_dict['times'] = homework.times

        final_response['homework_info'] = homework_dict
        final_response['status'] = 0
        return JsonResponse(final_response)
    
def edit_homework_basic_info_teacher(request):
    # status codd:
        # 0 -- success
        # 1 -- object not found error
        # 2 -- session expired error
    if request.method == 'POST':
        homework_name = request.POST['name_origin']
        name = request.POST['name']
        score = request.POST['score']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        times = request.POST['times']

        final_response = {}
        
        session = get_session(request.POST['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']
        
        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        homework = Homework.objects.get(course = course, name = homework_name)
        homework.name = name
        homework.score = score
        homework.start_time = start_time
        homework.end_time = end_time
        homework.times = times

        base = get_base_dir() + '/' + course.semester.name + '/' + course.name + '/' + 'homeworks' + '/'
        homework_base = base + homework_name
        homework_new_base = base + name
        os.rename(homework_base, homework_new_base)
        
        homework.save()

        final_response['status'] = 0
        return JsonResponse(final_response)

def edit_homework_content_teacher(request):
    # status code:
        # 0 -- success
        # 1 -- object not found error
        # 2 -- session expired error
    if request.method == 'POST':
        content = request.POST.get('content', None)
        
        final_response = {}
        
        session = get_session(request.POST['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']
        homework_name = session['homework_name']
        
        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        homework = Homework.objects.get(course = course, name = homework_name)
        homework.content = content
        homework.save()

        final_response['status'] = 0
        return JsonResponse(final_response)

def view_homework_attachment_teacher(request):
    # a homework attachment list contains:
        # name, size(file only), modified(modify time)
    # base url
    # status code:
        # 0 -- success
        # 1 -- object not found error
        # 2 -- session expired error
        # 3 -- path not exist error
    if request.method == 'POST':
        final_response = {}
        
        session = get_session(request.POST['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']
        homework_name = session['homework_name']
        
        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        homework_base = get_base_dir() + '/' + course.semester.name + '/' + course.name + '/' + 'homeworks' + '/' + homework_name
        if not os.path.exists(homework_base):
            final_response['status'] = 3
            return JsonResponse(final_response)

        homework_attachment_list = []
        file_name_list = os.listdir(homework_base)
        for file_name in file_name_list:
            file_dict = {}
            file_abs_path = os.path.join(homework_base, file_name)
            file_dict['name'] = file_name
            if os.path.isfile(file_abs_path):
                file_dict['size'] = humanfriendly.format_size(os.stat(file_abs_path).st_size)
            struct_time = time.gmtime(os.path.getmtime(file_abs_path))
            format_time = '%s/%s/%s %s:%s' % (struct_time.tm_year, struct_time.tm_mon, struct_time.tm_mday, struct_time.tm_hour, struct_time.tm_min);
            file_dict['modified'] = format_time
            homework_attachment_list.append(file_dict)
        final_response['contents'] = homework_attachment_list
        final_response['base_url'] = '/root' + '/' + course.semester.name + '/' + course.name + '/' + 'homeworks' + '/' + homework_name
        final_response['status'] = 0
        return JsonResponse(final_response)

def upload_homework_attachment_teacher(request):
    # status code:
        # 0 -- success
        # 1 -- object not found error
        # 2 -- session expired error
        # 3 -- path not exist error
    if request.method == 'POST':
        attachment = request.FILES['attachment']
        
        final_response = {}
        
        session = get_session(request.POST['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']
        homework_name = session['homework_name']
        
        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        homework_base = get_base_dir() + '/' + course.semester.name + '/' + course.name + '/' + 'homeworks' + '/' + homework_name
        if not os.path.exists(homework_base):
            final_response['status'] = 3
            return JsonResponse(final_response)

        attachment_path = homework_base + '/' + attachment.name
        save_inmemory_file(attachment, attachment_path)

        final_response['status'] = 0
        return JsonResponse(final_response)

def delete_homework_attachment_teacher(request):
    # status code:
        # 0 -- success
        # 1 -- object not found error
        # 2 -- pass not exist error
    if request.method == 'POST':
        homework_attachment_list = request.POST.getlist('contents[]')
        
        final_response = {}
        
        session = get_session(request.POST['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']
        homework_name = session['homework_name']
        
        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        for homework_attachment in homework_attachment_list:
            homework_attachment_path = get_base_dir() + '/' + course.semester.name + '/' + course.name + '/' + 'homeworks' + '/' + homework_name + '/' + homework_attachment
            if os.path.exists(homework_attachment_path):
                os.remove(homework_attachment_path)
            else:
                final_response['status'] = 2
                return JsonResponse(final_response)
        final_response['status'] = 0
        return JsonResponse(final_response)

def add_homework_teacher(request):
    # status code:
        # 0 -- success
        # 1 -- object not found error
        # 2 -- session expired error
        # 3 -- path exist error
        # 4 -- duplicated name error
    if request.method == 'POST':
        name = request.POST['name']
        score = request.POST['score']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        times = request.POST['times']
        
        final_response = {}
        
        session = get_session(request.POST['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']

        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        try:
            test_homework = Homework.objects.get(course = course, name = name)
            final_response['status'] = 4
            return JsonResponse(final_response)
        except:
            homework_base = get_base_dir() + '/' + course.semester.name + '/' + course.name + '/' + 'homeworks' + '/' + name
            if os.path.exists(homework_base):
                final_response['status'] = 3
                return JsonReponse(final_response)
            else:
                os.mkdir(homework_base)
                homework = Homework()
                homework.course = course
                homework.name = name
                homework.score = score
                homework.start_time = start_time
                homework.end_time = end_time
                homework.times = times
                homework.save()
                final_response['status'] = 0
                return JsonResponse(final_response)

def delete_homework_teacher(request):
    # status code:
        # 0 -- success
        # 1 -- object not found error
        # 2 -- path not exist error
    if request.method == 'POST':
        homework_name = request.POST['name']

        final_response = {}
        
        session = get_session(request.POST['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']
        
        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)
        
        try:
            homework = Homework.objects.get(course = course, name = homework_name)
            homework_base = get_base_dir() + '/' + course.semester.name + '/' + course.name + '/' + 'homeworks' + '/' + homework_name
            if os.path.exists(homework_base):
                shutil.rmtree(homework_base)
            else:
                final_response['status'] = 2
                return JsonResponse(final_response)
            homework.delete()
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)
        final_response['status'] = 0
        return JsonResponse(final_response)

def get_team_homework_list_teacher(request):
    # return a team homework list contains:
        # name, code, score
    # status code:
        # 0 -- success
        # 1 -- object not found error
        # 2 -- path not exist error
    if request.method == 'POST':
        final_response = {}

        session = get_session(request.POST['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']
        homework_name = request.POST['name'] if request.POST.get('name', None) else session['homework_name']
        
        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        homework = Homework.objects.get(course = course, name = homework_name)
        team_homework_obj_list = TeamHomework.objects.filter(homework = homework)

        team_homework_list = []
        for team_homework in team_homework_obj_list:
            team_homework_dict = {}
            team_homework_dict['name'] = team_homework.team.name
            team_homework_dict['code'] = team_homework.team.code
            team_homework_dict['score'] = team_homework.score
            team_homework_dict['times'] = team_homework.times
            team_homework_list.append(team_homework_dict)
        final_response['team_homework_list'] = team_homework_list
        final_response['status'] = 0
        return JsonResponse(final_response)

def view_team_homework_info_teacher(request):
    # return a json object contains:
        # contents which is a file list contains:
            # name, size, modified
    # status code:
        # 0 -- success
        # 1 -- object not found error
        # 2 -- path not exist error
    if request.method == 'POST':
        team_code = request.POST['code']
        
        final_response = {}

        session = get_session(request.POST['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']
        homework_name = session['homework_name']
        
        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        homework = Homework.objects.get(course = course, name = homework_name)
        team = Team.objects.get(course = course, code = team_code)
        team_homework = TeamHomework.objects.get(homework = homework, team = team)
        homework_base = get_base_dir() + '/' + course.semester.name + '/' + course.name + '/' + 'homeworks' + '/' + homework_name + '/' + team.name

        homework_file_list = []
        file_name_list = os.listdir(homework_base)
        for file_name in file_name_list:
            file_dict = {}
            file_abs_path = os.path.join(homework_base, file_name)
            file_dict['name'] = file_name
            if os.path.isfile(file_abs_path):
                file_dict['size'] = humanfriendly.format_size(os.stat(file_abs_path).st_size)
            struct_time = time.gmtime(os.path.getmtime(file_abs_path))
            format_time = '%s/%s/%s %s:%s' % (struct_time.tm_year, struct_time.tm_mon, struct_time.tm_mday, struct_time.tm_hour, struct_time.tm_min);
            file_dict['modified'] = format_time
            homework_file_list.append(file_dict)

        final_response['contents'] = homework_file_list
        final_response['homework_content'] = team_homework.content
        final_response['base_url'] = '/root' + '/' + course.semester.name + '/' + course.name + '/' + 'homeworks' + '/' + homework_name + '/' + team.name
        final_response['status'] = 0
        return JsonResponse(final_response)

def score_team_homework_teacher(request):
    # status code:
        # 0 -- success
        # 1 -- object not found error
        # 2 -- session expired error
        # 3 -- score out of range exception
    if request.method == 'POST':
        team_code = request.POST['code']
        score = request.POST['score']
        comment = request.POST['comment']

        final_response = {}

        session = get_session(request.POST['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']
        homework_name = session['homework_name']
        
        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        homework = Homework.objects.get(course = course, name = homework_name)
        team = Team.objects.get(course = course, code = team_code)
        team_homework = TeamHomework.objects.get(homework = homework, team = team)

        if (int)(score) <= homework.score:
            team_homework.score = score
            team_homework.save()
            final_response['status'] = 0
            return JsonResponse(final_response)
        else:
            final_response['status'] = 3
            return JsonResponse(final_response)

def download_team_homework_zip_teacher(request):
    if request.method == 'GET':
        final_response = {}
        
        session = get_session(request.GET['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']
        homework_name = session['homework_name']

        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        homework_base = get_base_dir() + '/' + course.semester.name + '/' + course.name + '/' + 'homeworks' + '/' + homework_name
        list_dirs = os.walk(homework_base)

        zip_subdir = homework_name
        zip_filename = "%s.zip" % zip_subdir
        print zip_filename
        
        s = StringIO.StringIO()

        zf = zipfile.ZipFile(s, "w")

        for root, dirs, files in list_dirs:
            for f in files:
                fpath = os.path.join(root, f)
                zip_path = os.path.relpath(fpath, homework_base)
                zf.write(fpath, zip_path)
        zf.close()

        response = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(zip_filename)
        return response

def upload_modified_homework_teacher(request):
    if request.method == 'POST':
        zip_file = request.FILES['homework']

        final_response = {}

        zf = zipfile.ZipFile(zip_file, 'r')
        '''
        session = get_session(request.POST['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']
        homework_name = session['homework_name']
        '''
        course_code = 'se002'
        homework_name = u'首次版本发布计划'
        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        homework_base = get_base_dir() + '/' + course.semester.name + '/' + course.name + '/' + 'homeworks'
        team_homework_base = homework_base + '/' + homework_name
        
        shutil.rmtree(team_homework_base)
        
        zf.extractall(homework_base.encode('gbk'))

        final_response['status'] = 0
        return JsonResponse(final_response)

def export_team_excel_teacher(request):
    if request.method == 'GET':
        final_response = {}
        
        session = get_session(request.GET['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']
        
        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        wb = xlwt.Workbook()
        sheet = wb.add_sheet(course.name + u'-团队报表')
        sheet.write(0, 0, u'团队名称')
        sheet.write(0, 1, u'团队ID')
        sheet.write(0, 2, u'成员姓名')
        sheet.write(0, 3, u'学号')
        sheet.write(0, 4, u'角色')
        file_name = course.name + u'-团队报表.xls'
        
        team_list = []
        try:
            team_list = Team.objects.filter(course = course)
        except:
            pass

        row_index = 1
        for team in team_list:
            if team.verified == True:
                team_member_list = TeamMember.objects.filter(team = team)
                for team_member in team_member_list:
                    if team_member.verified == True:
                        sheet.write(row_index, 0, team.name)
                        sheet.write(row_index, 1, team.code)
                        sheet.write(row_index, 2, team_member.student.user.name)
                        sheet.write(row_index, 3, team_member.student.user.username)
                        sheet.write(row_index, 4, team_member.role)
                        row_index = row_index + 1
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=' + smart_str(file_name)
        wb.save(response)
        return response

def export_homework_excel_teacher(request):
    if request.method == 'GET':
        homework_name = request.GET['name']
        
        session = get_session(request.GET['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']
        
        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)
        
        homework = Homework.objects.get(course = course, name = homework_name)
      
        wb = xlwt.Workbook()
        sheet = wb.add_sheet(u'作业-' + homework.name + u'-报表')
        sheet.write(0, 0, u'团队名称')
        sheet.write(0, 1, u'团队ID')
        sheet.write(0, 2, u'是否提交')
        sheet.write(0, 3, u'得分')
        file_name = u'作业-' + homework.name + u'-报表.xls'

        team_list = []
        try:
            team_list = Team.objects.filter(course = course)
        except:
            pass

        row_index = 1
        for team in team_list:
            if team.verified == True:
                sheet.write(row_index, 0, team.name)
                sheet.write(row_index, 1, team.code)
                team_homework = None
                try:
                    team_homework = TeamHomework.objects.get(team = team, homework = homework)
                except:
                    pass
                if team_homework == None:
                    sheet.write(row_index, 2, u'否')
                    sheet.write(row_index, 3, 0)
                else:
                    if team_homework.times == 0:
                        sheet.write(row_index, 2, u'否')
                    else:
                        sheet.write(row_index, 2, u'是')
                    sheet.write(row_index, 3, team_homework.score)
                row_index = row_index + 1
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=' + smart_str(file_name)
        wb.save(response)
        return response

def export_n_homework_excel_teacher(request):
    if request.method == 'GET':
        
        session = get_session(request.GET['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']

        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        homework_list = []
        try:
            homework_list = Homework.objects.filter(course = course)
        except:
            pass

        team_list = []
        try:
            team_list = Team.objects.filter(course = course)
        except:
            pass

        wb = xlwt.Workbook()
        file_name = u'课程-' + course.name + u'-作业统计报表.xls'
        
        for homework in homework_list:
            sheet = wb.add_sheet(u'作业-' + homework.name)
            sheet.write(0, 0, u'团队名称')
            sheet.write(0, 1, u'团队ID')
            sheet.write(0, 2, u'是否提交')
            sheet.write(0, 3, u'得分')
            row_index = 1
            for team in team_list:
                if team.verified == True:
                    sheet.write(row_index, 0, team.name)
                    sheet.write(row_index, 1, team.code)
                    team_homework = None
                    try:
                        team_homework = TeamHomework.objects.get(team = team, homework = homework)
                    except:
                        pass
                    if team_homework == None:
                        sheet.write(row_index, 2, u'否')
                        sheet.write(row_index, 3, 0)
                    else:
                        if team_homework.times == 0:
                            sheet.write(row_index, 2, u'否')
                        else:
                            sheet.write(row_index, 2, u'是')
                        sheet.write(row_index, 3, team_homework.score)
                    row_index = row_index + 1
                    
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=' + smart_str(file_name)
        wb.save(response)
        return response

def export_score_excel_teacher(request):
    if request.method == 'GET':
        
        session = get_session(request.GET['session_key'])
        if session is None:
            final_response['status'] = 2
            return JsonResponse(final_response)
        course_code = session['course_code']

        course = None
        try:
            course = Course.objects.get(code = course_code)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        enroll_list = []
        try:
            enroll_list = Enroll.objects.filter(course = course)
        except:
            pass

        team_list = []
        try:
            team_list = Team.objects.filter(course = course)
        except:
            pass

        homework_list = []
        try:
            homework_list = Homework.objects.filter(course = course)
        except:
            pass

        wb = xlwt.Workbook()
        sheet = wb.add_sheet(u'学生成绩统计表')
        sheet.write(0, 0, u'学号')
        sheet.write(0, 1, u'姓名')
        sheet.write(0, 2, u'成绩')
        file_name = u'课程-' + course.name + u'-学生成绩统计报表.xls'

        row_index = 1
        for enroll in enroll_list:
            student = enroll.student
            sheet.write(row_index, 0, student.user.username)
            sheet.write(row_index, 1, student.user.name)
            
            student_team = None
            for team in team_list:
                team_member = None
                try:
                    team_member = TeamMember.objects.get(student = student, team = team, verified = True)
                    student_team = team
                    break
                except:
                    pass
            if student_team == None:
                sheet.write(row_index, 2, 0)
            else:
                total_score = 0
                weighted_score = 0
                for homework in homework_list:
                    team_homework = None
                    try:
                        team_homework = TeamHomework.objects.get(team = student_team, homework = homework)
                    except:
                        pass
                    if team_homework != None:
                        weight = None
                        try:
                            weight = Weight.objects.get(teamhomework = team_homework, student = student, done = 1)
                        except:
                            pass
                        if weight != None:
                            total_score = total_score + team_homework.score
                            weighted_score = weighted_score + weight.weight * team_homework.score
                score = 0
                if total_score != 0:
                    score = (float)(weighted_score) / total_score * 100
                sheet.write(row_index, 2, score)
            row_index = row_index + 1

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=' + smart_str(file_name)
        wb.save(response)
        return response
        
def get_session(session_key):
    s = None
    try:
        s = SessionStore(session_key = session_key)
    except:
        pass
    return s

def get_current_semester():
    current_semester = Meta.objects.get(key = 'current_semester').value
    semester = Semester.objects.get(name = current_semester)
    return semester

def get_base_dir():
    return Meta.objects.get(key = 'root').value

def save_inmemory_file(temp_file, path):
    with open(path, 'wb') as f:
        for chunk in temp_file.chunks():
            f.write(chunk)
