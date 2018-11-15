#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
#from teachapp.models import Admin, Teacher, Student, Course, Homework, Team, TeamMember,TeamHomework, Teach, Meta
import json
import mammoth
import os
import xlrd
import time, datetime
# Create your views here.
'''
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        identity = request.POST['identity']

        json_response = {}

        if identity == 'admin':
            try:
                user = Admin.objects.get(username = username)
                if user.password == password:
                    json_response['info'] = 'login success'
                    #request.session['username'] = username
                    #request.session['identity'] = identity
                    response = JsonResponse(json_response)
                    response.set_cookie('username', username)
                    response.set_cookie('identity', identity)
                    return response
                else:
                    json_response['info'] = 'password error'
                    return JsonResponse(json_response)
            except ObjectDoesNotExist:
                json_response['info'] = 'user not exist'
                return JsonResponse(json_response)
        elif identity == 'teacher':
            try:
                user = Teacher.objects.get(username = username)
                if user.password == password:
                    json_response['info'] = 'login success'
                    #request.session['username'] = username
                    #request.session['identity'] = identity
                    response = JsonResponse(json_response)
                    response.set_cookie('username', username)
                    response.set_cookie('identity', identity)
                    return response
                else:
                    json_response['info'] = 'password error'
                    return JsonResponse(json_response)
            except ObjectDoesNotExist:
                json_response['info'] = 'user not exist'
                return JsonResponse(json_response)
        else:
            try:
                user = Student.objects.get(username = username)
                if user.password == password:
                    json_response['info'] = 'login success'
                    #request.session['username'] = username
                    #request.session['identity'] = identity
                    response = JsonResponse(json_response)
                    response.set_cookie('username', username)
                    response.set_cookie('identity', identity)
                    return response
                else:
                    json_response['info'] = 'password error'
                    return JsonResponse(json_response)
            except ObjectDoesNotExist:
                json_response['info'] = 'user not exist'
                return JsonResponse(json_response)

def show_all_course(request):
    if request.method == 'POST':
        #print request.session.keys()
    #username = request.session['username']
    #identity = request.session['identity']

    #username = '14211059'
    #identity = 'student'
        username = request.POST['username']
        identity = request.POST['identity']

        if identity == 'teacher':
            teacher = None
            try:
                teacher = Teacher.objects.get(username = username)
            except ObjectDoesNotExist:
                return HttpResponse('error')

            all_teach = Teach.objects.filter(teacher = teacher)

            current_course = []
            previous_course = []
            for ta in all_teach:
                course_dict = {}

                teach = Teach.objects.filter(course = ta.course)
                teacher_list = []
                
                for t in teach:
                    if t.teacher.name not in teacher_list:
                        teacher_list.append(t.teacher.name)

                course_dict['name'] = ta.course.name
                course_dict['teacher_name'] = teacher_list
                course_dict['code'] = ta.course.code
                course_dict['semester'] = ta.course.semester

                current_semester = Meta.objects.get(key = 'semester_name').value

                if ta.course.semester == current_semester:
                    student_count = TeamMember.objects.filter(course = ta.course).count()
                    course_dict['student_count'] = student_count
                    current_course.append(course_dict)
                else:
                    previous_course.append(course_dict)
                    
            final_response = {}
            final_response['current'] = current_course
            final_response['previous'] = previous_course
            return JsonResponse(final_response)
        else:
            student = None
            try:
                student = Student.objects.get(username = username)
            except ObjectDoesNotExist:
                return HttpResponse('error')
            print '1'
            all_tm = TeamMember.objects.filter(student = student)
            print all_tm
            current_course = []
            
            for tm in all_tm:
                course_dict = {}

                teach = Teach.objects.filter(course = tm.course)
                teacher_list = []
                
                for t in teach:
                    if t.teacher.name not in teacher_list:
                        teacher_list.append(t.teacher.name)

                course_dict['name'] = tm.course.name
                course_dict['teacher_name'] = teacher_list
                course_dict['code'] = tm.course.code
                course_dict['semester'] = tm.course.semester
                
                current_semester = Meta.objects.get(key = 'semester_name').value

                print current_semester
                print tm.course.semester
                if tm.course.semester == current_semester:
                    student_count = TeamMember.objects.filter(course = tm.course).count()
                    course_dict['student_count'] = student_count
                    current_course.append(course_dict)
            print '2'
            final_response = {}
            final_response['current'] = current_course
            print final_response
            return JsonResponse(final_response)

def set_semester(request):
    if request.method == 'POST':
        semester_name = request.POST['name']
        semester_start = request.POST['start_date']
        semester_end = request.POST['end_date']
        semester_weeks = request.POST['weeks']

        json_response = {}

        try:
            meta1 = Meta.objects.get(key = 'semester_name')
            meta2 = Meta.objects.get(key = 'semester_start')
            meta3 = Meta.objects.get(key = 'semester_end')
            meta4 = Meta.objects.get(key = 'semester_weeks')
            meta1.value = semester_name
            meta2.value = semester_start
            meta3.value = semester_end
            meta4.value = semester_weeks
            meta1.save()
            meta2.save()
            meta3.save()
            meta4.save()
        except ObjectDoesNotExist:
            Meta.objects.create(key = 'semester_name', value = semester_name)
            Meta.objects.create(key = 'semester_start', value = semester_start)
            Meta.objects.create(key = 'semester_end', value = semester_end)
            Meta.objects.create(key = 'semester_weeks', value = semester_weeks)

        return JsonResponse(json_response)

def get_information(request):
    if request.method == 'GET':
        json_response = {}

        try:
            meta = Meta.objects.get(key = 'semester_weeks')
            json_response['weeks'] = int(meta.value)
            json_response['teacher_username'] = []
            json_response['teacher_name'] = []
            json_response['student_username'] = []
            json_response['student_name'] = []

            teacher = Teacher.objects.all()
            for teacher_item in teacher:
                json_response['teacher_username'].append(teacher_item.username)
                json_response['teacher_name'].append(teacher_item.name)

            student = Student.objects.all()
            for student_item in student:
                json_response['student_username'].append(student_item.username)
                json_response['student_name'].append(student_item.name)
            json_response['success'] = True

            return JsonResponse(json_response)
        except ObjectDoesNotExist:
            json_response['success'] = False
            json_response['error_msg'] = 'no semester'
            return JsonResponse(json_response)

def set_course_admin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data['name']
        code = data['code']
        credit = data['credit']
        semester = Meta.objects.get(key = 'semester_name').value
        start_week = data['start_week']
        end_week = data['end_week']
        info = data['info']
        #description = data['description']
        teacher_username = data['teacher_username']
        student_username = data['student_username']

        json_response = {}

        if(len(Course.objects.filter(code = code)) > 0):
            json_response['success'] = False
            json_response['error_msg'] = 'course exist'
            return JsonResponse(json_response)
        else:
            Course.objects.create(name = name, code = code, credit = credit, semester = semester, start_week = start_week, end_week = end_week, info = info)
            try:
                course = Course.objects.get(code = code)
                for teacher_item in teacher_username:  
                    teacher_item = Teacher.objects.get(username = teacher_item)   
                    if len(Teach.objects.filter(teacher = teacher_item, course = course)) == 0:
                        Teach.objects.create(teacher = teacher_item, course = course)

                if student_username != None:
                    for student_item in student_username:
                        student_item = Student.objects.get(username = student_item)
                        if len(TeamMember.objects.filter(student = student_item, course = course)) == 0:
                            TeamMember.objects.create(student = student_item, course = course)
            except:
                pass
            json_response['success'] = True      

            return JsonResponse(json_response)

def set_course_by_excel(request):
    if request.method == 'POST':
        fl = request.FILES.get('file')
        baseDir = os.path.dirname(os.path.abspath(__name__))
        filedir = os.path.join(baseDir,'static')
        filename = os.path.join(filedir,fl.name)

        file_des = open(filename,'wb')
        for chrunk in fl.chunks():
            file_des.write(chrunk)
        file_des.close()

        json_response = {}
        bk = xlrd.open_workbook(filename)
        try:
            sh = bk.sheet_by_name('Sheet1')
        except:
            json_response['success'] = False
            json_response['error_msg'] = 'sheet name error'
            return JsonResponse(json_response)
        nrows = sh.nrows

        try:
            name = sh.cell_value(1, 0)
            code = sh.cell_value(1, 1)
            credit = int(sh.cell_value(1, 2))
            semester = Meta.objects.get(key = 'semester_name').value
            start_week = int(sh.cell_value(1, 3))
            end_week = int(sh.cell_value(1, 4))
            info = sh.cell_value(1, 7)
            if len(Course.objects.filter(code = code)) == 0:
                Course.objects.create(name = name, code = code, credit = credit, semester = semester, start_week = start_week, end_week = end_week, info = info)
        except:
            json_response['success'] = False
            json_response['error_msg'] = 'Add course failed, please check your content of excel'
            return JsonResponse(json_response)

        course = Course.objects.get(code = code)
        for i in range(1, nrows - 1):
            teacher_username = sh.cell_value(i, 5)
            try:
                teacher = Teacher.objects.get(username = teacher_username)
                if len(Teach.objects.filter(teacher = teacher, course = course)) == 0:
                    Teach.objects.create(teacher = teacher, course = course)
            except:
                pass
        for i in range(1, nrows - 1):
            student_username = sh.cell_value(i, 6)
            try:
                student = Student.objects.get(username = student_username)
                if len(TeamMember.objects.filter(student = student, course = course)) == 0:
                    TeamMember.objects.create(student = student, course = course)
            except:
                pass
        os.remove(filename)
        json_response['success'] = True
        return JsonResponse(json_response)

def show_course_detail(request):
    if request.method == 'POST':
        semester = Meta.objects.get(key = 'semester_name').value
        course_name = request.POST['course_name']

        course = None
        try:
            course = Course.objects.get(name = course_name, semester = semester)
        except ObjectDoesNotExist:
            HttpResponse('error')

        final_response = {}
        final_response['course_name'] = course.name
        final_response['semester'] = course.semester
        final_response['start_week'] = course.start_week
        final_response['end_week'] = course.end_week
        final_response['code'] = course.code
        final_response['credit'] = course.credit
        final_response['student_num'] = TeamMember.objects.filter(course = course).count()
        final_response['info'] = course.info
        final_response['description'] = course.description
        
        root = Meta.objects.get(key = 'root').value
        outline_path = os.path.dirname(root) + '/' + course.semester + '/' + course.name + '/' + 'outline.html'
        if os.path.exists(outline_path):
            final_response['outline'] = outline_path
        
        return JsonResponse(final_response)

def get_student_list(request):
    if request.method == 'POST':
        semester = Meta.objects.get(key = 'semester_name').value
        course_name = request.POST['course_name']
        
        course_obj = Course.objects.get(name = course_name, semester = semester)
        course_id = course_obj.id
        member_list = TeamMember.objects.filter(course = course_id)
        student_list = []
        for member in member_list:
            student = Student.objects.get(id = member.student.id)
            student_dict = {}
	    student_dict['username'] = student.username
            student_dict['name'] = student.name
            student_dict['phone'] = student.phone
            student_dict['email'] = student.email
            student_list.append(student_dict)
        print student_list
        final_response = {}
        final_response['student_list'] = student_list
	
        return JsonResponse(final_response)

def get_homework_list(request):
    if request.method == 'POST':
        semester = Meta.objects.get(key = 'semester_name').value
        course_name = request.POST['course_name']
        
        course_obj = Course.objects.get(name = course_name, semester = semester)
        course_id = course_obj.id

        homework_list = Homework.objects.filter(course = course_id)
	
        result_list = []
        for hw in homework_list:
            homework = {}
            homework['name'] = hw.name
            homework['start_time'] = hw.start_time
            homework['end_time'] = hw.end_time
            homework['times'] = hw.times
            homework['score'] = hw.score
            result_list.append(homework)
	print result_list
        final_response = {}
        final_response['homework_list'] = result_list
        return JsonResponse(final_response)

def get_team_homework_list(request):
    if request.method == 'POST':
        semester = Meta.objects.get(key = 'semester_name').value
        homework_name = 'team construction'
        course_name = request.POST['course_name']
        course = Course.objects.get(name = course_name, semester = semester)
	homework = Homework.objects.get(name = homework_name, course = course)
        team_homework = TeamHomework.objects.filter(Homework = homework)
        thw_list = []
        for thw in team_homework:
            homework = {}
            team_id = thw.team
            team_member = TeamMember.objects.filter(team = team_id)

            for member in team_member:
                if member.role == 'sm':
                    student = Student.objects.get(id = member.student.id)
		    homework['sender'] = student.name
                    break
            homework['time'] = thw.time
            homework['score'] = thw.score
            root = Meta.objects.get(key = 'root')
            homework_path = os.path.dirname(root) + '/' + course.semester + '/' + course.name + '/' + 'homeworks' + '/' + homework.name + '/' + homework['sender']
            homework_file = os.listdir(homework_path)
            homework['url'] = homework_path + '/' + homework_file[0]
            thw_list.append(homework)
	print thw_list
        final_response = {}
        final_response['team_homework_list'] = thw_list
        return JsonResponse(final_response)

def set_homework(request):
    if request.method == 'POST':
        print request.POST.keys()
        final_response = {}
        semester = Meta.objects.get(key = 'semester_name').value
        course_name = request.POST['course_name']

        course = None
        try:
            course = Course.objects.get(name = course_name, semester = semester)
        except ObjectDoesNotExist:
            HttpResponse('error')
        
        name = request.POST['name']
        start_time = datetime.datetime.strptime(request.POST['start_time'].replace('T', ' '), "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(request.POST['end_time'].replace('T', ' '), "%Y-%m-%d %H:%M:%S")
        score = request.POST['score']
        times = request.POST['times']
        content = request.POST['content']

        test_homework = None
        semester = Meta.objects.get(key = 'semester_name')
        try:
            test_homework = Homework.objects.get(name = course_name, course = course)
        except ObjectDoesNotExist:
            pass

        if test_homework != None:
            final_response['success'] = False
            return JsonResponse(final_response)
        else:
            Homework.objects.create(name=name, start_time=start_time, end_time=end_time, score=score, times=times, content=content, course = course)
            final_response['success'] = True

            attachment = request.FILES.get('file', None)
            if attachment != None:
                root = Meta.objects.get(key = 'root')
                attachment_dir = root + '/' + course.semester + '/' + course.name + '/homeworks' + '/' + name

                if not os.path.exists(attachment_dir):
                    os.mkdir(attachment_dir)
                    
                attachment_path = attachment_dir + '/' + attachment.name
                save_file(attachment, attachment_path)
            return JsonResponse(final_response)
'''
