#-*- coding:utf-8 -*-
from models import *
from django.shortcuts import render, render_to_response, HttpResponse
from django.http import  JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import datetime
import string
from function.zip import InMemoryZip
import os, json, time
from importlib import import_module
import humanfriendly
from django.conf import settings
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
#返回所有学生的课程信息,需要传入学生的用户名 D
def stuAllCourse(request):
    if request.method == 'POST':
        print request.POST['session_key']
        #返回数据列表
        dataList = []
        #判断是否登录
        session = get_session(request.POST['session_key'])
        print session
        if session is None:
            return HttpResponse('2')
        #获取当前登录用户
        username = session['username']
        #查表操作
        enrollList = Enroll.objects.filter(student__user__username = username)
        #数据添加
        for enroll in enrollList:
            infoList = {}
            infoList['course_name'] = enroll.course.name
            infoList['start_time'] = enroll.course.start_week
            infoList['end_time'] = enroll.course.end_week
            infoList['credit'] = enroll.course.credit
            infoList['course_code'] = enroll.course.code
            infoList['teacher'] = tnConnect(enroll.course.id)
            infoList['course_id'] = enroll.course.id
            currentSemester = False
            try:
                currentSemester = Meta.objects.get(key='semester_name').value
            except ObjectDoesNotExist:
                pass
            if enroll.course.semester.name == currentSemester:
                infoList['isActive'] = True
            else:
                infoList['isActive'] = False
            dataList.append(infoList)
        print dataList
        return HttpResponse(json.dumps(dataList, ensure_ascii=False), content_type='application/json; charset=utf-8')
    return HttpResponse('error', content_type='application/json; charset=utf-8')

#获取课程详细信息，需要传入课程code
def courseDetail(request):
    if request.method == 'POST':
        # 返回数据列表
        dataList = {}
        # 判断是否登录
        session = get_session(request.POST['session_key'])
        if session is None:
            return HttpResponse('2')
        # 获取当前课程id
        id = int(request.POST['course_id'])
        # 查表操作
        course = None
        try:
            course = Course.objects.get(id=id)
        except ObjectDoesNotExist:
            return HttpResponse('error')
        #数据添加
        dataList['name'] = course.name
        dataList['code'] = course.code
        dataList['credit'] = course.credit
        dataList['teacher'] = tnConnect(id)
        dataList['semester'] = course.semester.name
        dataList['start_week'] = course.start_week
        dataList['end_week'] = course.end_week
        dataList['quantity'] = Enroll.objects.filter(course__id=id).count()
        dataList['info'] = course.info
        dataList['description'] = course.description
        dataList['outline'] = ''
        # 读取课程大纲html文件
        try:
            path = u'G:/大三下/软件开发实践/code/mooc/teacherPlatform/static/root/{0}/{1}/outline.html'.format(course.semester.name, course.name)
            with open(path) as file_object:
                dataList['outline'] = file_object.read()
        except:
            pass
        return HttpResponse(json.dumps(dataList, ensure_ascii=False), content_type='application/json; charset=utf-8')
    return HttpResponse('error')

#将某个课程下的老师姓名连接
def tnConnect(id):
    teacherList = Teach.objects.filter(course__id=id)
    name = ''
    flag = True
    for teacher in teacherList:
        if flag == True:
            name += teacher.teacher.user.name
            flag = False
        else:
            name += u'、' + teacher.teacher.user.name
    return name

#获取学生所有作业，需要传入学生的用户名和课程code Done
def stuAllHomework(request):
    if request.method == 'POST':
        # 返回数据列表
        dataList = []
        # 判断是否登录
        session = get_session(request.POST['session_key'])
        if session is None:
            return HttpResponse(2)
        # 获取当前课程id和用户
        course_id = int(request.POST['course_id'])
        username = session['username']
        # 查表操作
        course = None
        homeworkList = Homework.objects.filter(course__id=course_id)
        #数据添加操作
        for homework in homeworkList:
            hwList = {}
            hwList['homework_id'] = homework.id
            hwList['homework_name'] = homework.name
            hwList['start_time'] = homework.start_time.strftime('%Y-%m-%d %H:%M:%S')
            hwList['end_time'] = homework.end_time.strftime('%Y-%m-%d %H:%M:%S')
            hwList['max_times'] = homework.times
            hwList['perfect_score'] = homework.score
            hwList['homework_code'] = homework.id
            hwList['submit_times'] = 0
            hwList['student_score'] = u'无'
            #找到当前学生所在团队的该课程作业记录
            teamHomework = None
            #获取当前team
            try:
                teamMember = TeamMember.objects.get(student__user__username='username')
                teamHomework = TeamHomework.objects.get(homework=homework, team=teamMember.team)
                hwList['submit_times'] = teamHomework.times
                hwList['student_score'] = teamHomework.score
            except ObjectDoesNotExist:
                pass
            dataList.append(hwList)
        return HttpResponse(json.dumps(dataList, ensure_ascii=False), content_type='application/json; charset=utf-8')
    return HttpResponse('error')

#获取作业详细信息，需要传入作业id和学生用户名
def homeworkDetail(request):
    if request.method == 'POST':
        #返回的数据列表
        dataList = {}
        # 判断是否登录
        session = get_session(request.POST['session_key'])
        if session is None:
            return HttpResponse('2')
        #接受的数据
        id = int(request.POST['homework_id'])
        username = session['username']
        #查表操作
        homework = None
        try:
            homework = Homework.objects.get(id=id)
        except ObjectDoesNotExist:
            HttpResponse('404 Not Found')
        #数据添加
        dataList['homework_id'] = homework.id
        dataList['homework_name'] = homework.name
        dataList['start_time'] = homework.start_time.strftime('%Y-%m-%d %H:%M:%S')
        dataList['end_time'] = homework.end_time.strftime('%Y-%m-%d %H:%M:%S')
        dataList['max_times'] = homework.times
        dataList['id'] = homework.id
        dataList['homework_context'] = homework.content
        dataList['perfect_score'] = homework.score
        dataList['flag'] = True
        if homework.start_time > datetime.datetime.now() or datetime.datetime.now() > homework.end_time:
            dataList['flag'] = False
        #教师作业附件
        teacherAttachmentPath = []
        #教师附件所在文件夹
        staticPath = u'http://10.138.203.21:1234/static/root/{0}/{1}/homeworks/{2}/'.format(homework.course.semester.name, homework.course.name, homework.name)#静态目录
        path = u'G:/大三下/软件开发实践/code/mooc/teacherPlatform/static/root/{0}/{1}/homeworks/{2}/'.format(homework.course.semester.name, homework.course.name, homework.name)#系统目录
        try:
            for filename in os.listdir(path):
                if os.path.isfile(path + filename):
                    teacherAttachmentPath.append(staticPath + filename.encode('utf-8'))
        except:
            pass
        dataList['teacher_attachment_path'] = teacherAttachmentPath
        #学生作业提交数据
        dataList['submit_times'] = 0
        dataList['student_score'] = None
        dataList['student_submit_homework'] = None
        teacherModifiedHomework = []
        studentAttachmentPath = []
        try:
            course = Course.objects.get(homework__id=id)
            teamMember = TeamMember.objects.get(student__user__username=username, team__course=course)
            teamHomework = TeamHomework.objects.get(homework__id=id, team=teamMember.team)
            dataList['submit_times'] = teamHomework.times
            dataList['student_score'] = teamHomework.score
            dataList['teacher_opinion'] = teamHomework.comment
            dataList['student_submit_homework'] = teamHomework.content
            #学生上传的作业附件
            staticPath = u'http://10.138.203.21:1234/static/root/{0}/{1}/homeworks/{2}/{3}/'.format(homework.course.semester.name, homework.course.name, homework.name, teamMember.team.name)  # 此处应为静态资源根目录
            path = u'G:/大三下/软件开发实践/code/mooc/teacherPlatform/static/root/{0}/{1}/homeworks/{2}/{3}/'.format(homework.course.semester.name, homework.course.name, homework.name, teamMember.team.name) #系统目录
            print path
            try:
                for filename in os.listdir(path):
                    print path + filename
                    if os.path.isfile(path + filename):
                        if filename.find('modified_') == -1:#教师修改前的作业
                            studentAttachmentPath.append(staticPath + filename.encode('utf-8'))
                        else:#教师修改后的作业
                            teacherModifiedHomework.append(staticPath + filename.encode('utf-8'))
            except:
                pass
        except ObjectDoesNotExist:
            pass
        dataList['student_attachment_path'] = studentAttachmentPath
        dataList['teacher_modified_homework'] = teacherModifiedHomework
        dataList['gradeDone'] = False
        try:
            weight = Weight.objects.get(teamhomework__homework__id=id, done=True,
                                        student__user__username=username)
            dataList['gradeDone'] = True
        except ObjectDoesNotExist:
            pass
        print dataList
        return HttpResponse(json.dumps(dataList, ensure_ascii=False), content_type='application/json; charset=utf-8')
    return HttpResponse('404 Not Found')

#作业提交，需要传入作业id和学生用户名
def homeworkSubmit(request):
    if request.method == 'POST':
        #返回数据列表
        dataList = []
        # 判断是否登录
        session = get_session(request.POST['session_key'])
        if session is None:
            return HttpResponse('2')
        #获取参数
        username = session['username']
        id = int(request.POST['homework_id'])
        #获取前端数据
        content = request.POST['homework_content']
        #数据库操作
        time = datetime.datetime.now()
        #未加入团队不能提交作业
        teamMember = None
        try:
            teamMember = TeamMember.objects.get(student__user__username=username)
        except ObjectDoesNotExist:
            return HttpResponse('您还未加入一个团队，不能提交作业')
        try:
            #作业已存在，更新作业
            teamHomework = TeamHomework.objects.get(homework__id=id, team=teamMember.team)
            if teamHomework.times >= teamHomework.homework.times:
                return HttpResponse('提交次数已达上限')
            if teamHomework.homework.end_time < time:
                return HttpResponse('提交时间已截止')
            if teamHomework.homework.start_time > time:
                return HttpResponse('作业尚未开始')
            teamHomework.content = content
            teamHomework.time = time
            teamHomework.times += 1
            teamHomework.save()
        except ObjectDoesNotExist:
            #作业不存在创建
            try:
                homework = Homework.objects.get(id=id)
                TeamHomework.objects.create(team=teamMember.team, homework=homework, content=content, time=time, times=1)
            except ObjectDoesNotExist:#异常情况
                return HttpResponse('error')
        return HttpResponse('提交成功')
    return HttpResponse('error')

#作业提交页面的初始化 Done
def homeworkSubmitInit(request):
    if request.method == 'POST':
        dataList = {}
        # 判断是否登录
        session = get_session(request.POST['session_key'])
        if session is None:
            return HttpResponse(2)
        id = int(request.POST['homework_id'])
        dataList['homework_content'] = '暂无'
        try:
            homework = Homework.objects.get(id = id)
            dataList['homework_content'] = homework.content
        except ObjectDoesNotExist:
            return HttpResponse('error')
        return HttpResponse(json.dumps(dataList, ensure_ascii=False), content_type='application/json; charset=utf-8')
    return HttpResponse('error')

#获取个人所加入的所有团队，需要传入一个username Done
def allMyTeam(request):
    if request.method == 'POST':
        #返回的数据列表
        dataList = []
        # 判断是否登录
        session = get_session(request.POST['session_key'])
        if session is None:
            return HttpResponse(2)
        #需要接收username
        username = session['username']
        #数据库查表操作
        try:
            teamMember = TeamMember.objects.filter(student__user__username=username)
            for tm in teamMember:
                team = {}
                team['team_name'] = tm.team.name
                team['team_id'] = tm.team.id
                team['course_name'] = tm.team.course.name
                dataList.append(team)
        except ObjectDoesNotExist:
            return HttpResponse('error')
        return HttpResponse(json.dumps(dataList, ensure_ascii=False), content_type='application/json; charset=utf-8')
    return HttpResponse('error')

#初始化团队详细信息，需要传入一个团队id Done
def teamInfo(request):
    if request.method == 'POST':
        #返回的数据列表
        dataList = {}
        # 判断是否登录
        session = get_session(request.POST['session_key'])
        if session is None:
            return HttpResponse(2)
        #接收一个团队id
        id = int(request.POST['team_id'])
        #数据库查表操作
        teamMember = TeamMember.objects.filter(team__id=id)
        #队伍不存在
        if len(teamMember) == 0:
            return HttpResponse('error')
        #数据传输
        else:
            dataList['student_id'] = session['username']
            dataList['captain_id'] = ''
            memberList = []
            for tm in teamMember:
                if tm.verified == True:#只显示通过审核的成员
                    memberInfo = {}
                    memberInfo['student_id'] = tm.student.user.username
                    memberInfo['student_role'] = tm.role
                    memberInfo['student_name'] = tm.student.user.name
                    if tm.role == 'sm':
                        dataList['captain_id'] = tm.student.user.username
                    memberList.append(memberInfo)
            dataList['memberList'] = memberList
            dataList['team_id'] = teamMember[0].team.id
            dataList['team_name'] = teamMember[0].team.name
            dataList['team_status'] = teamMember[0].team.verified
            dataList['flag'] = True
            if teamMember[0].team.course.team_ddl < datetime.datetime.now():
                dataList['flag'] = False
            return HttpResponse(json.dumps(dataList, ensure_ascii=False), content_type='application/json; charset=utf-8')
    return HttpResponse('error')

#查看当前队伍的申请人员，需要传入一个团队id Done
def teamApply(request):
    if request.method == 'POST':
        #返回的数据列表
        dataList = []
        # 判断是否登录
        session = get_session(request.POST['session_key'])
        if session is None:
            return HttpResponse(2)
        #接收前端数据
        id = int(request.POST['team_id'])
        #数据库查表操作
        teamMember = TeamMember.objects.filter(team__id=id, verified=0)
        for tm in teamMember:
            memberInfo = {}
            memberInfo['student_name'] = tm.student.user.name
            memberInfo['student_id'] = tm.student.user.username
            memberInfo['student_role'] = tm.role
            dataList.append(memberInfo)
        return HttpResponse(json.dumps(dataList, ensure_ascii=False), content_type='application/json; charset=utf-8')
    return HttpResponse('error')

#向老师提交组队申请，需要传入一个团队id 和一个当前正在登陆的用户username Done
def teamSubmit(request):
    if request.method == 'POST':
        # 判断是否登录
        session = get_session(request.POST['session_key'])
        if session is None:
            return HttpResponse(2)
        #接收前端数据
        id = int(request.POST['team_id'])
        username = session['username']
        user = None
        #数据库操作
        #获取当前登录的用户
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponse('error')
        try:
            team = Team.objects.get(id=id)
            if datetime.datetime.now() > team.course.team_ddl:
                return HttpResponse('团队提交时间已结束')
            team.done = True
            team.save()
            #发送通知
            teachList = Teach.objects.filter(course__team=team)
            for teach in teachList:
                content = team.course.name + u'的' + team.name + u'小组已创建完毕，请求审核。'
                Message.objects.create(user_from=user, user_to=teach.teacher.user, content=content)
        except ObjectDoesNotExist:
            return HttpResponse('队伍不存在')
        return HttpResponse('提交成功')
    return HttpResponse('error')

#同意/不同意他人加入团队  ... Done
def teamCheck(request):
    if request.method == 'POST':
        # 判断是否登录
        session = get_session(request.POST['session_key'])
        if session is None:
            return HttpResponse(2)
        #接受前端数据
        student_username = request.POST['student_id']
        team_id = int(request.POST['team_id'])
        result = int(request.POST['result'])
        #正在登陆的用户名
        username = session['username']
        loginUser = None
        tarUser = None
        #数据库操作
        try:
            #获取目标学生和正在登陆的学生
            loginUser = User.objects.get(username=username)
            tarUser = User.objects.get(username=student_username)
        except ObjectDoesNotExist:
            return HttpResponse('error')
        try:
            teamMember = TeamMember.objects.get(team__id=team_id, student__user__username=student_username)
            if datetime.datetime.now() > teamMember.team.course.team_ddl:
                return HttpResponse('团队组建时间已结束')
            #同意操作
            print result
            if result == 1:
                teamMember.verified = True
                teamMember.save()
                content = u'您想要加入' + teamMember.team.name + u'团队的请求已被队长同意。'
                Message.objects.create(user_from=loginUser, user_to=tarUser, content=content)
                #同意需要删除该成员其他申请
                toDelete = TeamMember.objects.filter(student__user=tarUser, verified=False, team__course__id=teamMember.team.course.id)
                for tm in toDelete:
                    tm.delete()
            else:#拒绝操作
                teamMember.team.members -= 1#团队人数减一
                teamMember.save()
                teamMember.delete()
                content = u'您想要加入' + teamMember.team.name + u'团队的请求已被队长同意。'
                Message.objects.create(user_from=loginUser, user_to=tarUser, content=content)
            return HttpResponse('操作成功')
        except ObjectDoesNotExist:
            return HttpResponse('成员不存在')
    return HttpResponse('error')

#上传作业文件的后端,file为后端传回的二进制文件,还需要传入一个正在登陆的username和提交的作业id Done
def homeworkUpload(request):
    if request.method == 'POST':
        # 判断是否登录
        session = get_session(request.POST['session_key'])
        if session is None:
            return HttpResponse(2)
        #文件为空
        if request.FILES.getlist('file') != []:
            #接受正在登陆的username
            username = session['username']
            homework_id = int(request.POST['homework_id'])
            #数据库查表操作
            path = ''
            teamMember = None
            try:
                teamMember = TeamMember.objects.get(student__user__username=username, verified=True)
            except ObjectDoesNotExist:
                return HttpResponse('您还未加入团队，不能提交作业')
            try:
                teamHomework = TeamHomework.objects.get(homework__id=homework_id, team=teamMember.team)
                path = u'G:/大三下/软件开发实践/code/mooc/teacherPlatform/static/root/{0}/{1}/homeworks/{2}/{3}/'.format(
                    teamHomework.homework.course.semester.name, teamHomework.homework.course.name, teamHomework.homework.name, teamHomework.team.name)  # 系统目录
            except ObjectDoesNotExist:
                return HttpResponse('error')
            # 接受目标文件
            file = request.FILES.getlist('file')[0]
            try:
                #目录不存在创建目录
                if not os.path.exists(path):
                    os.makedirs(path)
                # 写入文件
                with open(path + file.name, 'wb+') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
            except:
                return  HttpResponse('error')
            return HttpResponse('上传成功')
        return  HttpResponse(u'您未选中任何文件', content_type='application/json; charset=utf-8')
    return HttpResponse('error')

#显示课程队伍,需要获取课程id和当前登录的username  Done
def courseTeam(request):
    if request.method == 'POST':
        #返回数据列表
        dataList = {}
        # 判断是否登录
        session = get_session(request.POST['session_key'])
        if session is None:
            return HttpResponse(2)
        #接收数据
        username = session['username']
        course_id = int(request.POST['course_id'])
        #查表操作
        dataList['course_id'] = course_id
        dataList['captain_name'] = ''
        dataList['captain_id'] = ''
        dataList['personal_team_status'] = 0#没有申请加入任何队伍
        memberList = []
        dataList['memberList'] = memberList
        try:
            teamMember = TeamMember.objects.get(student__user__username=username, verified=True, team__course__id=course_id)
            dataList['personal_team_status'] = 2#已经有队伍了
            dataList['team_name'] = teamMember.team.name
            allMember = TeamMember.objects.filter(team=teamMember.team, verified=True)
            #循环添加组员信息
            for tm in allMember:
                memberInfo = {}
                memberInfo['student_id'] = tm.student.user.username
                memberInfo['student_name'] = tm.student.user.name
                memberInfo['student_role'] = tm.role
                memberList.append(memberInfo)
                #添加队长信息
                if tm.role == 'sm':
                    dataList['captain_name'] = tm.student.user.name
                    dataList['captain_id'] = tm.student.user.username
        except ObjectDoesNotExist:
            teamMembers = TeamMember.objects.filter(student__user__username=username, verified=False, team__course__id=course_id)
            if len(teamMembers) > 0:
                dataList['personal_team_status'] = 1  # 正在申请
        appliedList = []
        otherList = []
        dataList['appliedList'] = appliedList#提交申请的团队列表
        dataList['otherList'] = otherList#未提交申请的团队列表sh
        allTeam = Team.objects.filter(course__id=course_id)
        for t in allTeam:
            teamInfo = {}
            teamInfo['team_name'] = t.name
            teamInfo['team_member_number'] = t.members
            teamInfo['team_id'] = t.id
            teamInfo['captain_name'] = ''
            #添加队长姓名
            try:
                captain = TeamMember.objects.get(team=t, role='sm')
                teamInfo['captain_name'] = captain.student.user.name
            except ObjectDoesNotExist:
                pass
            me = TeamMember.objects.filter(team=t, student__user__username=username)
            if len(me) > 0:#申请加入
                appliedList.append(teamInfo)
            else:#未申请加入
                otherList.append(teamInfo)
        return HttpResponse(json.dumps(dataList, ensure_ascii=False), content_type='application/json; charset=utf-8')
    return HttpResponse('error')

#创建团队，需要传入课程id和要创建的团队名和当前登录用户名 Done
def createTeam(request):
    if request.method == 'POST':
        # 判断是否登录
        session = get_session(request.POST['session_key'])
        if session is None:
            return HttpResponse(2)
        #接受数据
        course_id = request.POST['course_id']
        team_name = request.POST['team_name']
        username = session['username']
        #团队重名检测
        allTeam = Team.objects.filter(course__id=course_id)
        for each in allTeam:
            if each.name == team_name:
                return  HttpResponse('团队重名，请重新命名')
        #已在团队的学生不能创建团队
        if TeamMember.objects.filter(student__user__username=username, verified=True, team__course__id=course_id).count() > 0:
            return  HttpResponse('您已在团队中，不能创建团队')
        # 需要删除该成员其他申请
        user = User.objects.get(username = username)
        student = Student.objects.get(user = user)
        toDelete = TeamMember.objects.filter(student__user__id=student.id, team__course__id=course_id)
        for tm in toDelete:
            tm.delete()
        #获取当前课程最大编号
        code = Team.objects.filter(course__id=course_id).count()
        #获取课程和学生
        student = None
        course = None
        try:
            course = Course.objects.get(id=course_id)
            student = Student.objects.get(user__username=username)
        except ObjectDoesNotExist:
            return HttpResponse('error')
        # 创建团队
        team = Team.objects.create(course=course, code=code, name=team_name, verified=False, members=1, done=False)
        #创建团队队长
        TeamMember.objects.create(student=student, team=team,  role='sm', verified=True)
        return HttpResponse('创建成功')
    return HttpResponse('error')

#显示成员信息,接受一个团队id Done
def showTeamInfo(request):
    if request.method == 'POST':
        #返回数据列表
        dataList = {}
        # 判断是否登录
        session = get_session(request.POST['session_key'])
        if session is None:
            return HttpResponse(2)
        #接收前端数据
        team_id = int(request.POST['team_id'])
        #数据库操作
        try:
            team = Team.objects.get(id=team_id)
            dataList['team_name'] = team.name
        except ObjectDoesNotExist:
            return HttpResponse('队伍不存在')
        teamMember = TeamMember.objects.filter(team__id=team_id, verified=True)
        memberList = []
        dataList['captain_id'] = ''
        dataList['captain_name'] = ''
        #循环添加组内成员
        for tm in teamMember:
            memberInfo = {}
            memberInfo['student_id'] = tm.student.user.username
            memberInfo['student_name'] = tm.student.user.name
            memberInfo['student_role'] = tm.role
            memberList.append(memberInfo)
            #添加队长信息
            if tm.role == 'sm':
                dataList['captain_id'] = tm.student.user.username
                dataList['captain_name'] = tm.student.user.name
        dataList['memberList'] = memberList
        return HttpResponse(json.dumps(dataList, ensure_ascii=False), content_type='application/json; charset=utf-8')
    return HttpResponse('error')

#申请加入team,需要获取团队id和当前登录的用户username Done
def joinTeam(request):
    if request.method == 'POST':
        # 判断是否登录
        session = get_session(request.POST['session_key'])
        if session is None:
            return HttpResponse(2)
        #接受数据
        username = session['username']
        team_id = int(request.POST['team_id'])
        student_role = request.POST['student_role']
        #数据库操作
        #找出登录用户
        student = None
        team = None
        try:
            student = Student.objects.get(user__username=username)
            team = Team.objects.get(id=team_id)
        except ObjectDoesNotExist:
            return  HttpResponse('error')
        loginUser = None
        teamMember = None
        try:
            # 获取目标学生和正在登陆的学生
            loginUser = User.objects.get(username=username)
            teamMember = TeamMember.objects.get(team__id=team_id, role='sm')
            if teamMember.team.course.team_ddl < datetime.datetime.now():
                return HttpResponse('团队组建时间已截止')
        except ObjectDoesNotExist:
            return HttpResponse('error')
        TeamMember.objects.create(student=student, team=team, role=student_role, verified=False)
        #发送通知
        content = loginUser.name + u'同学申请加入您的团队' + teamMember.team.name + u'。'
        Message.objects.create(user_from=loginUser, user_to=teamMember.student.user, content=content)
        return HttpResponse('已发送申请')
    return HttpResponse('error')

#打包下载
def homeworkZip(request):
    if request.method != 'POST':
        # 获取文件全部名称
        path = request.GET['path']
        realPath = getPath(path)
        # 文件压缩
        zip = InMemoryZip()
        for file in os.listdir(realPath):
            if os.path.isfile(realPath + file):
                if path.find('modified') != -1:#下载修改后的作业
                    if file.find('modified') == 0:
                        zip.appendFile(realPath + file)
                    else:
                        pass
                else:#下载修改前的作业
                    if file.find('modified') == -1:
                        zip.appendFile(realPath + file)
                    else:
                        pass

        # 生成下载源
        data = zip.read()
        response = HttpResponse()
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment; filename="download.zip"'
        response["Content-Length"] = len(data)
        response.write(data)
        return response
    return HttpResponse('error')

#获取真实的路径
def getPath(path):
    i = 1
    index = len(path)
    for p in path:
        if p == '/':
            index = i
        i += 1
    return u'G:/大三下/软件开发实践/code/mooc/teacherPlatform/{0}'.format(path[path.find('static'): index])

#作业删除 Done
def homeworkDelete(request):
    if request.method == 'POST':
        # 判断是否登录
        session = get_session(request.POST['session_key'])
        if session is None:
            return HttpResponse(2)
        #接受数据
        username = session['username']
        homework_id = int(request.POST['homework_id'])
        homework_name = request.POST['homework_name']
        #查表操作
        try:
            homework = Homework.objects.get(id=homework_id)
            teamMember = TeamMember.objects.get(student__user__username=username, team__course=homework.course)
            if teamMember.role != 'sm':#只有sm可以删除作业
                return HttpResponse('只有队长可以删除作业')
            semesterName = homework.course.semester.name
            courseName = homework.course.name
            teamName = teamMember.team.name
            filename = u'G:/大三下/软件开发实践/code/mooc/teacherPlatform/static/root/{0}/{1}/homeworks/{2}/{3}/{4}'.format(
                semesterName, courseName, homework.name, teamName, homework_name)
            try:
                os.remove(filename)
                return HttpResponse('删除成功')
            except:
                return HttpResponse('error')
        except ObjectDoesNotExist:
            return HttpResponse('error')

#组内评分 Done
def gradeMate(request):
    if request.method == 'POST':
        #返回的数据列表
        dataList = {}
        # 判断是否登录
        session = get_session(request.POST['session_key'])
        if session is None:
            return HttpResponse(2)
        #接受数据
        homework_id = int(request.POST['homework_id'])
        username = session['username']
        #查表操作
        try:
            weight = Weight.objects.get(teamhomework__homework__id=homework_id, done=True,
                                        student__user__username=username)
            return HttpResponse('0')
        except ObjectDoesNotExist:
            pass
        try:
            homework = Homework.objects.get(id=homework_id)
            me = TeamMember.objects.get(student__user__username=username, verified=True, team__course=homework.course)
            teamMembers = TeamMember.objects.filter(team=me.team, verified=True)
            dataList['team_name'] = me.team.name
            memberList = []
            for tm in teamMembers:
                memberInfo = {}
                memberInfo['student_role'] = tm.role
                memberInfo['student_id'] = tm.student.user.username
                memberInfo['student_name'] = tm.student.user.name
                memberList.append(memberInfo)
            dataList['memberList'] = memberList
        except ObjectDoesNotExist:
            return  HttpResponse('error')
        return HttpResponse(json.dumps(dataList, ensure_ascii=False), content_type='application/json; charset=utf-8')
    return HttpResponse('error')

#组内评分处理函数 Done
def gradeMateAction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # 判断是否登录
        session = get_session(data['session_key'])
        if session is None:
            return HttpResponse(2)
        #接受前端数据
        studentIdList = data['student_id']
        studentScoreList = data['student_score']
        homework_id = data['homework_id']
        username = session['username']
        #获取正在登陆的用户
        student = None
        #循环评分
        i = 0
        for id in studentIdList:
            try:
                print id
                teamHomework = TeamHomework.objects.get(homework__id=homework_id)
                student = Student.objects.get(user__username=id)
                try:#该组员已被评过分
                    # 当前已被评分人数
                    count = Weight.objects.filter(teamhomework=teamHomework, done=True).count()
                    #修改评分系数
                    weight = Weight.objects.get(teamhomework=teamHomework, student=student)
                    weight.weight = float(float(studentScoreList[i]) + weight.weight * count) / (count + 1)
                    weight.save()
                except ObjectDoesNotExist:#该组员第一次被评分
                    Weight.objects.create(teamhomework=teamHomework, student=student, weight=studentScoreList[i], done=False)
                if id == username:
                    # 记下自己已评分
                    try:
                        weight = Weight.objects.get(teamhomework=teamHomework, student=student)
                        weight.done = True
                        weight.save()
                    except ObjectDoesNotExist:
                         HttpResponse('error')
            except ObjectDoesNotExist:#异常
                return  HttpResponse('error')
            i += 1
        return  HttpResponse('评分成功')
    return HttpResponse('error')

#sesion获取函数
def get_session(session_key):
    s = None
    try:
        s = SessionStore(session_key = session_key)
    except:
        pass
    return s

'''
#登录测试函数
def login(request):
    s = None
    try:
        s = SessionStore(session_key=request.POST['session_key'])
    except:
        s = SessionStore()
        s['username'] = request.GET['username']
        s.create()
    dataList = {}
    dataList['session_key'] = s.session_key
    return HttpResponse(json.dumps(dataList, ensure_ascii=False), content_type='application/json; charset=utf-8')
'''

#资源浏览
def getResources(request):
    # return a json object contains:
    # contents which is a file list contains:
    # name, size, modified
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
        course_id = int(request.POST['course_id'])

        relPath = request.POST['relpath']

        course = None
        try:
            course = Course.objects.get(id=course_id)
        except ObjectDoesNotExist:
            final_response['status'] = 1
            return JsonResponse(final_response)

        resources_base = u'G:/大三下/软件开发实践/code/mooc/teacherPlatform/static/root/{0}/{1}/resources/{2}'.format(course.semester.name, course.name, relPath)

        resources_file_list = []
        file_name_list = os.listdir(resources_base)
        for file_name in file_name_list:
            file_dict = {}
            file_abs_path = os.path.join(resources_base, file_name)
            file_dict['name'] = file_name
            if os.path.isfile(file_abs_path):
                file_dict['size'] = humanfriendly.format_size(os.stat(file_abs_path).st_size)
            struct_time = time.gmtime(os.path.getmtime(file_abs_path))
            format_time = '%s/%s/%s %s:%s' % (
            struct_time.tm_year, struct_time.tm_mon, struct_time.tm_mday, struct_time.tm_hour, struct_time.tm_min);
            file_dict['modified'] = format_time
            resources_file_list.append(file_dict)

        final_response['contents'] = resources_file_list
        final_response[
            'base_url'] = '/root' + '/' + course.semester.name + '/' + course.name + '/' + 'resources'
        final_response['status'] = 0
        return JsonResponse(final_response)

'''
#测试
def test(request):
    path = u'G:/大三下/软件开发实践/code/mooc/teacherPlatform/static/root/2016-2017summer/软件开发实践/homeworks/test/RSNDM/homework.txt'
    realPath = getPath(path)
    # 文件压缩
    print realPath
    zip = InMemoryZip()
    for file in os.listdir(realPath):
        zip.appendFile(realPath + file)

    # 生成下载源
    data = zip.read()
    response = HttpResponse()
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename="download.zip"'
    response["Content-Length"] = len(data)
    response.write(data)
    return response
'''
