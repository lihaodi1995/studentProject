# coding=utf8
import io
import os
import zipfile
import json

import xlrd
import xlwt
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from users.models import *


# Create your views here.

def check_assignment(req):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    courseid = req.session['course_id']
    try:
        crs = Course.objects.get(id=int(courseid))
        asnmt = Assignment.objects.filter(course=crs)
    except Exception as e:
        print(e)

    selectCourseList = CourseTeacher.objects.filter(teacher__user__id=req.session['user_id'])
    return render(req, 'teachers/checkAssignment.html',
                  {'courseid': courseid, 'assignmentlist': asnmt, 'selectCourseList': selectCourseList})


def show_team_assignment(req, param1):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    assignment_team_list_d = []
    try:
        # crs = Course.objects.get(id=int(param1))
        crs = Course.objects.get(id=int(req.session['course_id']))
        teamobjects = Team.objects.filter(course=crs)
        for tm in teamobjects:
            info = {}
            info['team_id'] = tm.id
            info['name'] = tm.name
            info['head'] = tm.head.id
            info['people_number'] = tm.people_number
            asnmt = Assignment.objects.get(id=int(param1))
            records = AssignmentSubmitRecord.objects.filter(team=tm, assignment=asnmt)
            record = None
            sub_times = -1
            for rec in records:
                if rec.submit_times > sub_times:
                    record = rec
                    sub_times = rec.submit_times
            if record != None:
                info['record_id'] = int(record.id)
            else:
                info['record_id'] = False
            assignment_team_list_d.append(info)

    except Exception as e:
        print(e)
    print(assignment_team_list_d)
    for team in assignment_team_list_d:
        print(team['name'], team['record_id'])
    selectCourseList = CourseTeacher.objects.filter(teacher__user__id=req.session['user_id'])
    return render(req, 'teachers/AssignmentTeamList.html',
                  {'assignment_team_list_d': assignment_team_list_d, 'courseid': req.session['course_id'],
                   'selectCourseList': selectCourseList})


def index(request):
    if not request.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    course_list = None
    try:
        course_list = Course.objects.all()
    except Exception as e:
        print(e)
    selectCourseList = CourseTeacher.objects.filter(teacher__user__id=request.session['user_id'])
    return render(request, 'teachers/index.html', {'course_list': course_list, 'selectCourseList': selectCourseList})


def course_session(req, param1):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    req.session['course_id'] = param1
    selectCourseList = CourseTeacher.objects.filter(teacher__user__id=req.session['user_id'])
    return render(req, 'teachers/courseIndex.html', {'courseid': param1, 'selectCourseList': selectCourseList})


def course_index(req):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    try:
        courseid = req.session['course_id']
    except Exception as e:
        print(e)
        req.session['course_id'] = 1
        courseid = req.session['course_id']

    selectCourseList = CourseTeacher.objects.filter(teacher__user__id=req.session['user_id'])
    return render(req, 'teachers/courseIndex.html', {'courseid': courseid, 'selectCourseList': selectCourseList})


def add_assignment(req):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    courseid = req.session['course_id']
    selectCourseList = CourseTeacher.objects.filter(teacher__user__id=req.session['user_id'])
    return render(req, 'teachers/addAssignment.html', {'courseid': courseid, 'selectCourseList': selectCourseList})


def add_one_assignment(req):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    context = {}
    if req.method == 'POST':
        try:
            assignment = Assignment()
            assignment.name = req.POST['name']
            assignment.type = req.POST['inline-radios']
            assignment.start_time = req.POST['start_time']
            assignment.end_time = req.POST['end_time']
            assignment.allow_submit_times = req.POST['allow_submit_times']
            assignment.score = req.POST['score']
            assignment.score_percentage = req.POST['score_percentage']
            assignment.type = req.POST['inline-radios']
            courseid = req.session['course_id']
            course = get_object_or_404(Course, pk=courseid)
            assignment.course = course
            assignment.save()

            gradeItem = GradeItem()
            gradeItem.course = course
            gradeItem.name = req.POST['name']
            gradeItem.maxscore = req.POST['score']
            gradeItem.ratio = req.POST['score_percentage']
            gradeItem.type = u"作业"
            gradeItem.save()

            context['courseid'] = courseid
        except Exception as e:
            print(e)
    return HttpResponseRedirect(reverse('teachers:check_assignment'))


def manage_resources(req):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    courseid = req.session['course_id']
    filelist = []
    try:
        crs = Course.objects.get(id=courseid)
        cflist = CourseFile.objects.filter(course=crs)
        course_tag_list = Tag.objects.filter(course=crs)
        print(course_tag_list)
        for cf in cflist:
            file = File.objects.get(id=cf.file.id)
            tag_record = TagRecord.objects.filter(file=file)
            tags = ""
            for tag in tag_record:
                tags += tag.tag.tag + " "
            info = {}
            info['tag_record'] = tag_record
            info['tags'] = tags
            info['id'] = file.id
            info['name'] = file.name
            info['submitter'] = file.submitter
            info['time'] = file.time
            info['address'] = file.address
            filelist.append(info)
    except Exception as e:
        print(e)
    print(course_tag_list)
    selectCourseList = CourseTeacher.objects.filter(teacher__user__id=req.session['user_id'])
    return render(req, 'teachers/manageResources.html',
                  {'course_tag_list': course_tag_list, 'courseid': courseid, 'filelist': filelist,
                   'selectCourseList': selectCourseList})


def edit_homework(req):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    courseid = req.session['course_id']
    selectCourseList = CourseTeacher.objects.filter(teacher__user__id=req.session['user_id'])
    return render(req, 'teachers/editHomework.html', {'courseid': courseid, 'selectCourseList': selectCourseList})


def upload_resource(req):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    courseid = req.session['course_id'];
    if req.method == "POST":  # 请求方法为POST时，进行处理
        try:
            myFiles = req.FILES.getlist("resources", None)  # 获取上传的文件，如果没有文件，则默认为None
            if not myFiles:
                return HttpResponse("no files for upload!")

            for f in myFiles:
                path = r".\attachments\\"
                tfile = os.path.join(path, f.name)
                destination = open(tfile, 'wb+')  # 打开特定的文件进行二进制的写操作
                for chunk in f.chunks():  # 分块写入文件
                    destination.write(chunk)
                destination.close()  # 文件存放到本地

                dfile = File()
                dfile.name = f.name
                dfile.type = os.path.splitext(f.name)[1]
                dfile.submitter = req.session['user_id']
                # dfile.submitter = 1
                dfile.size = os.path.getsize(tfile)
                dfile.save()  # 首次新建文件索引记录

                # print(dfile.id,'|||',dfile.type)
                tname = str(dfile.id) + str(dfile.type)
                newname = os.path.join(path, tname)
                os.rename(tfile, newname)
                dfile.address = newname
                dfile.save()  # 重命名文件，更新文件索引记录

                cf = CourseFile()
                cf.file = dfile
                cs = Course.objects.get(id=courseid)
                cf.course = cs
                cf.save()  # 新建课程资源上传记录

                tags = req.POST.getlist('tag')
                for tagname in tags:
                    tag_record = TagRecord()
                    tag_record.file = dfile
                    tag = Tag.objects.get(course=cs, tag=tagname)
                    tag_record.tag = tag
                    tag_record.save()

        except Exception as e:
            print(e, 'z')
    return HttpResponseRedirect(reverse('teachers:manage_resources'))


def upload_grades(req):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    courseid = req.session['course_id']

    try:
        course = get_object_or_404(Course, pk=courseid)
        asnmts = Assignment.objects.filter(course=course)
        ass_list = []
        for ass in asnmts:
            info = {}
            info['id'] = ass.id
            info['name'] = ass.name
            info['type'] = ass.type
            ass_list.append(info)
    except Exception as e:
        print(e)

    selectCourseList = CourseTeacher.objects.filter(teacher__user__id=req.session['user_id'])
    return render(req, 'teachers/uploadGrades.html',
                  {'course_id': courseid, 'ass_list': ass_list, 'selectCourseList': selectCourseList})


def approve_team(req):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    courseid = req.session['course_id']
    selectCourseList = CourseTeacher.objects.filter(teacher__user__id=req.session['user_id'])
    return render(req, 'teachers/approveTeam.html', {'courseid': courseid, 'selectCourseList': selectCourseList})


def fine_tune_team(req):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    courseid = req.session['course_id']
    selectCourseList = CourseTeacher.objects.filter(teacher__user__id=req.session['user_id'])
    return render(req, 'teachers/fineTuneTeam.html', {'courseid': courseid, 'selectCourseList': selectCourseList})


def watch_team(req):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    courseid = req.session['course_id']
    team_list_d = []
    try:
        teamobjects = Team.objects.filter(course__id=courseid)
        for tm in teamobjects:
            info = {}
            info['id'] = tm.id
            info['name'] = tm.name
            info['head'] = tm.head.user.name  # 从负责人id索引到学生再索引用户获取用户名
            info['people_number'] = tm.people_number
            mems = StudentTeamInfo.objects.filter(team=tm)
            members = []
            for mem in mems:
                stu = {}
                stu['name'] = mem.student.user.name
                stu['id'] = mem.student.user.id
                stu['role'] = mem.role
                stu['email'] = mem.student.user.email
                members.append(stu)  # 从学生组队关系索引到学生再索引用户获取用户名
            info['stu_list'] = members
            team_list_d.append(info)
    except Exception as e:
        print(e)
    print(team_list_d)

    selectCourseList = CourseTeacher.objects.filter(teacher__user__id=req.session['user_id'])
    return render(req, 'teachers/watchTeam.html',
                  {'team_list': team_list_d, 'courseid': courseid, 'selectCourseList': selectCourseList})


def return_index(req):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    del req.session['course_id']
    return HttpResponseRedirect(reverse('teachers:index'))


def check_online(req, param1):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    courseid = req.session['course_id']
    info = {}
    submission = []
    print(param1)
    try:
        rec_obj = AssignmentSubmitRecord.objects.get(id=int(param1))

        info['name'] = rec_obj.assignment.name
        info['team_no'] = str(rec_obj.team.id) + r"  " + str(rec_obj.team.name)
        info['detail'] = rec_obj.assignment.detail
        info['text'] = rec_obj.text
        file_id_set = rec_obj.file_set.split(",")
        print(file_id_set)
        for id in file_id_set:
            if id != '':
                f = get_object_or_404(File, pk=id)
                submission.append(f)
    except Exception as e:
        print('Exception in check_online', e)
    print('in check_online', info)
    context = {}
    context['courseid'] = courseid
    context['s'] = info
    context['submission'] = submission
    context['rec_id'] = param1
    print('in check_online: end!!!!!!!!!!!!!!!!')
    selectCourseList = CourseTeacher.objects.filter(teacher__user__id=req.session['user_id'])
    context['selectCourseList'] = selectCourseList
    return render(req, 'teachers/checkOnline.html', context)


def download_resource(req, param1):  ####等待测试
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    # do something...
    # try:
    # def file_iterator(file_name, chunk_size=512):
    #     with open(file_name, 'rb') as f:
    #         while True:
    #             c = f.read(chunk_size)
    #             if c:
    #                 yield c
    #             else:
    #                 break

    asnmt = Assignment.objects.get(id=param1)  # 该作业的数据对象
    teams = Team.objects.filter(course__id=asnmt.course.id)  # 需要做该作业的团队
    files = []
    for team in teams:  # 遍历每个团队
        rec_num = 0
        record = AssignmentSubmitRecord()  ####查询某个团队对该作业最新提交
        for rec in AssignmentSubmitRecord.objects.filter(team__id=team.id):
            if rec.submit_times > rec_num:
                rec_num = rec.submit_times
                record = rec  ####查询某个团队对该作业最新提交
        fileset = record.file_set.split(',')
        if fileset != ['']:
            for f in fileset:
                if f != '':
                    files.append(File.objects.get(id=f))
    if files != []:
        s = io.BytesIO()
        zf = zipfile.ZipFile(s, "w")
        for file in files:
            zip_inter_path = file.name
            # zip_path = os.path.join("attachment", file.name)
            zf.write(file.address, str(zip_inter_path))
        zf.close()
        resp = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
        z_name = "Assignment.zip"
        resp['Content-Disposition'] = 'attachment; filename=%s' % z_name
        return resp
    else:
        return HttpResponse('未查询到对应的文件')
    # except Exception as e:
    #     print(e)
    return HttpResponse('download_resource下载这里完全在瞎搞')


# fo = File.objects.get(id=param1)
# print(fo.name)
# fpath = fo.address
# response = StreamingHttpResponse(file_iterator(fpath))
#
# # 以下代码用于将浏览器读取的数据变成文件
# response['Content-Type'] = 'application/octet-stream'
# print('attachment;filename="{0}"'.format(str(fo.name)))
# response['Content-Disposition'] = ('attachment;filename="{0}"'.format(str(fo.name)).encode('utf-8'))
# return response


# return HttpResponse('404,heihei,views.download_resource异常')


def delete_resource(request):
    if not request.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    param1 = request.GET.get('id')
    try:
        fo = get_object_or_404(File, pk=param1)
        cf = CourseFile.objects.get(file=fo)
        cf.delete()
        fo.address = None
    except Exception as e:
        print(e)
    context = {'status': param1}
    return JsonResponse(context)


def add_tag(req):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    tag = Tag()
    courseid = req.session['course_id']
    course = Course.objects.get(id=courseid)
    tag.tag = req.POST['tag_name']
    tag.course = course
    tag.save()

    return HttpResponseRedirect(reverse('teachers:manage_resources'))


def course_info(req):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    courseid = req.session['course_id']
    info = {}
    try:
        course = Course.objects.get(id=courseid)
        info['name'] = course.name
        info['semester'] = course.semester.name
        info['weeks'] = course.weeks
        stu_set = SelectCourse.objects.filter(course=course)
        info['number'] = stu_set.__len__()
        info['time'] = course.time
        info['address'] = course.address
        info['credit'] = course.credit
        info['team_people_lower_limit'] = course.team_people_lower_limit
        info['team_people_upper_limit'] = course.team_people_upper_limit
        info['status'] = course.status
        info['outline'] = course.outline

    except Exception as e:
        print(e)
    context = {}
    context['course'] = info
    context['course_id'] = courseid
    print(info)
    selectCourseList = CourseTeacher.objects.filter(teacher__user__id=req.session['user_id'])
    context['selectCourseList'] = selectCourseList
    return render(req, 'teachers/courseInfo.html', context)


def assignment_form(req, param1="1"):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    courseid = req.session['course_id']
    ass_list = Assignment.objects.filter(course_id=courseid)

    teams = Team.objects.filter(course_id=courseid)
    teamlist = []
    asnmt = None
    for tm in teams:
        info = {}
        info['id'] = tm.id
        info['name'] = tm.name
        info['head'] = tm.head.id
        info['people_number'] = tm.people_number
        if param1 == "":
            param1 = 1
        asnmt = get_object_or_404(Assignment, pk=int(param1))
        records = AssignmentSubmitRecord.objects.filter(team=tm, assignment=asnmt)
        print(tm.name, asnmt.name)
        record = None
        sub_times = -1
        rec_id_list = []
        for rec in records:
            print('id:', rec.id)
            if rec.submit_times > sub_times:
                record = rec
                sub_times = rec.submit_times
            rec_id_list.append(rec.assignment.id)
        if record != None:
            info['record_id'] = int(record.id)
        else:
            info['record_id'] = False
        rec_id_set = set(rec_id_list)
        sub_num = rec_id_set.__len__()
        info['sub_num'] = sub_num
        teamlist.append(info)

    context = {}
    context['course_id'] = courseid
    context['ass_list'] = ass_list
    context['teams'] = teamlist
    context['asnmt'] = asnmt
    selectCourseList = CourseTeacher.objects.filter(teacher__user__id=req.session['user_id'])
    context['selectCourseList'] = selectCourseList
    return render(req, 'teachers/assignmentForm.html', context)


def modify_course(req):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    courseid = req.session['course_id']

    info = {}

    try:
        course = Course.objects.get(id=courseid)
        course.credit = req.POST['credit']
        course.time = req.POST['time']
        course.team_people_upper_limit = req.POST['team_people_upper_limit']
        course.team_people_lower_limit = req.POST['team_people_lower_limit']
        course.outline = req.POST['outline']
        course.save()
        return HttpResponse("<script>alert('修改成功！'); window.location.href='/teachers/course_info/';</script>")
    except Exception as e:
        print(e)
        return HttpResponseRedirect(reverse('teachers:course_info'))


# def ass_list(req):
#     if not req.session.get('user_id', None):
#         return HttpResponseRedirect(reverse('login'))
#     courseid = req.session['course_id']
#     context = {}
#     context['course_id'] = courseid
#     return render(req, 'teachers/manage_grade.html', context)


def manage_team(req):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    courseid = req.session['course_id']
    context = {}
    context['course_id'] = courseid
    selectCourseList = CourseTeacher.objects.filter(teacher__user__id=req.session['user_id'])
    context['selectCourseList'] = selectCourseList
    return render(req, 'teachers/manage_grade.html', context)


def set_assignment_rate(req):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    courseid = req.session['course_id']
    context = {}
    context['course_id'] = courseid
    selectCourseList = CourseTeacher.objects.filter(teacher__user__id=req.session['user_id'])
    context['selectCourseList'] = selectCourseList
    return render(req, 'teachers/manage_grade.html', context)


def manage_grade(req):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    courseid = req.session['course_id']
    percent = 0
    course = Course.objects.get(id=courseid)
    team_list = Team.objects.all()
    team_grade = []
    course_team_list = Team.objects.filter(course=course)
    grade_items = GradeItem.objects.filter(course=course)
    full_score = 0
    for item in grade_items:
        full_score += item.maxscore * item.ratio
    for course_team in course_team_list:
        temp = {}
        ass_records = ReviseRecord.objects.filter(team=course_team)
        sum = 0
        for ass in ass_records:
            sum += ass.score * ass.assignment.score_percentage / ass.assignment.score
        grade_item_record = GradeRecord.objects.filter(team=course_team).filter(course=course)
        for grade_item in grade_item_record:
            sum += grade_item.score * grade_item.gradeitem.ratio / grade_item.gradeitem.maxscore
        temp['id'] = course_team.id
        temp['name'] = course_team.name
        temp['grade'] = sum
        team_grade.append(temp)
    try:
        gradeItems = GradeItem.objects.filter(course__id=courseid)
        for item in gradeItems:
            percent += item.ratio
    except Exception as e:
        print(e)

    context = {}
    context['course_id'] = courseid
    context['gradeItems'] = gradeItems
    context['sum_rate'] = percent
    context['team_list'] = team_list
    context['team_grade'] = team_grade
    selectCourseList = CourseTeacher.objects.filter(teacher__user__id=req.session['user_id'])
    context['selectCourseList'] = selectCourseList
    return render(req, 'teachers/manageGrade.html', context)


def add_grade_item(req):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    courseid = req.session['course_id']
    try:
        gradeItem = GradeItem()
        gradeItem.type = req.POST['type']
        gradeItem.name = req.POST['name']
        gradeItem.maxscore = req.POST['full_mark']
        gradeItem.ratio = req.POST['score_percentage']
        course = Course.objects.get(id=courseid)
        gradeItem.course = course
        gradeItem.save()
    except Exception as e:
        print(e)

    context = {}
    context['course_id'] = courseid
    selectCourseList = CourseTeacher.objects.filter(teacher__user__id=req.session['user_id'])
    context['selectCourseList'] = selectCourseList
    return HttpResponseRedirect(reverse('teachers:manage_grade'))


def modify_grade_item(req):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    courseid = req.session['course_id']

    try:
        gradeItems = GradeItem.objects.filter(course__id=courseid)
        for item in gradeItems:
            data = req.POST.getlist(str(item.id), [])
            item.type = data[0]
            item.name = data[1]
            item.maxscore = data[2]
            item.ratio = data[3]
            item.save()
    except Exception as e:
        print(e)

    return HttpResponseRedirect(reverse('teachers:manage_grade'))


def remove_grade_item(req, param1):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    courseid = req.session['course_id']

    try:
        gradeItem = GradeItem.objects.get(id=param1)
        if gradeItem.type == u"作业":
            gradeItem.ratio = 0
            gradeItem.save()
        else:
            gradeItem.delete()

    except Exception as e:
        print(e)

        context = {}
        context['course_id'] = courseid
        selectCourseList = CourseTeacher.objects.filter(teacher__user__id=req.session['user_id'])
        context['selectCourseList'] = selectCourseList
        return HttpResponseRedirect(reverse('teachers:manage_grade'))


def teacher_info(req):
    user = User.objects.get(id=int(req.session['user_id']))
    teacher_info = Teacher.objects.get(user=user)
    selectCourseList = CourseTeacher.objects.filter(teacher__user__id=req.session['user_id'])
    return render(req, 'teachers/teacherInfo.html',
                  {'teacher_info': teacher_info, 'selectCourseList': selectCourseList})


def show_edit_assignment(req, param1):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    courseid = req.session['course_id']

    ass = {}
    try:
        asnmt = Assignment.objects.get(id=param1)
    except Exception as e:
        print(e)

    context = {}
    context['course_id'] = courseid
    context['ass_id'] = param1
    context['ass'] = asnmt
    selectCourseList = CourseTeacher.objects.filter(teacher__user__id=req.session['user_id'])
    context['selectCourseList'] = selectCourseList
    return render(req, 'teachers/editAssignment.html', context)


def edit_assignment(req, param1):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    courseid = req.session['course_id']

    ass = {}
    try:
        asnmt = Assignment.objects.get(id=param1)
        asnmt.name = req.POST['name']
        asnmt.type = req.POST['inline_radios']
        asnmt.start_time = req.POST['start_time']
        asnmt.end_time = req.POST['end_time']
        asnmt.allow_submit_times = req.POST['allow_submit_times']
        asnmt.score = req.POST['score']
        asnmt.score_percentage = req.POST['score_percentage']
        asnmt.detail = req.POST['detail']
        asnmt.save()

    except Exception as e:
        print(e)

        context = {}
        context['course_id'] = courseid
        context['ass'] = ass
        selectCourseList = CourseTeacher.objects.filter(teacher__user__id=req.session['user_id'])
        context['selectCourseList'] = selectCourseList
        return HttpResponseRedirect(reverse('teachers:check_assignment'))


def select_via_tags(req):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    checked_tags = req.POST.getlist('checked_tag')
    courseid = req.session['course_id']
    filelist = []
    try:
        crs = Course.objects.get(id=courseid)
        cflist = CourseFile.objects.filter(course=crs)
        course_tag_list = Tag.objects.filter(course=crs)
        checked_course_tag_list = []
        for t in checked_tags:
            for tag in course_tag_list.filter(tag=t).values('tag'):
                checked_course_tag_list.append(tag['tag'])
        for i in checked_course_tag_list:
            print(i)
        try:
            for checked_tag in checked_course_tag_list:
                mytag = Tag.objects.filter(course=crs).get(tag=checked_tag)
                tagged_files = TagRecord.objects.filter(tag=mytag)
                for file in tagged_files:
                    tag_record = TagRecord.objects.filter(file=file.file)
                    tags = ""
                    for tag in tag_record:
                        tags += tag.tag.tag + " "
                    info = {}
                    info['tag_record'] = tag_record
                    info['tags'] = tags
                    info['id'] = file.file.id
                    info['name'] = file.file.name
                    info['submitter'] = file.file.submitter
                    info['time'] = file.file.time
                    info['address'] = file.file.address
                    filelist.append(info)
        except Exception as e:
            print(e, 'aaaa')
    except Exception as e:
        print(e)
    context = {}
    context['course_tag_list'] = course_tag_list
    context['checked_course_tag_list'] = checked_course_tag_list
    context['courseid'] = courseid
    context['filelist'] = filelist
    return render(req, 'teachers/manageResources.html', context)


def input_item_score(req, param1):
    context = {}
    gradeitem = get_object_or_404(GradeItem, pk=param1)
    team_list = Team.objects.all()
    for team in team_list:
        score = req.POST["ID_" + str(team.id)]
        grade_record = GradeRecord()
        grade_record.course = get_object_or_404(Course, pk=req.session['course_id'])
        grade_record.score = score
        grade_record.team = team
        grade_record.gradeitem = gradeitem
        grade_record.save()
    return HttpResponseRedirect('/teachers/upload_grade_item/' + param1)


def download_file(req):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    # do something...
    try:
        def file_iterator(file_name, chunk_size=512):
            with open(file_name, 'rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        file_id = req.GET.get('id')
        fo = get_object_or_404(File, pk=file_id)
        fpath = fo.address
        response = StreamingHttpResponse(file_iterator(fpath))

        # 以下代码用于将浏览器读取的数据变成文件
        response['Content-Type'] = 'application/octet-stream'
        print('attachment;filename="{0}"'.format(str(fo.name)))
        response['Content-Disposition'] = ('attachment;filename="{0}"'.format(str(fo.name)).encode('utf-8'))
        return response
    except Exception as e:
        print(e)
        return HttpResponse('download_file下载这里完全在瞎搞')


def download_file_test(req, param):
    try:
        def file_iterator(file_name, chunk_size=512):
            with open(file_name, 'rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        file_id = param
        fo = get_object_or_404(File, pk=file_id)
        fpath = fo.address
        response = StreamingHttpResponse(file_iterator(fpath))

        # 以下代码用于将浏览器读取的数据变成文件
        response['Content-Type'] = 'application/octet-stream'
        print('attachment;filename="{0}"'.format(str(fo.name)))
        response['Content-Disposition'] = ('attachment;filename="{0}"'.format(str(fo.name)).encode('utf-8'))
        return response
    except Exception as e:
        print(e)
        return HttpResponse('download_file下载这里完全在瞎搞')

def agree_team(request):
    team_id = request.GET.get('id')
    team =get_object_or_404(Team,pk=team_id)
    team.status = '审核通过'
    team.save()
    return JsonResponse({})

def get_team_info(request):
    context = {}
    try:
        team_list = Team.objects.all().values()
        team = []
        for t in team_list:
            t['head_id'] = get_object_or_404(Student, pk=t['head_id']).user.name
            member_list = StudentTeamInfo.objects.filter(team_id=t['id']).values()
            team.append(t)
            member = []
            t['people_number']=member_list.count()
            for m in member_list:
                member.append(m)
                stu = get_object_or_404(Student, pk=m['student_id'])
                m['id'] = stu.id
                m['student_id'] = stu.user.name
                m['gender'] = stu.user.gender
            t['member_list'] = member
        context['team_list'] = team
    except Exception as e:
        print(e)
    return JsonResponse(context)


def get_all_no_select_stu(request):
    context = {}
    student_list = Student.objects.all().values()
    stu_list = []
    for s in student_list:
        sti = StudentTeamInfo.objects.filter(student_id=s['id'])
        del s['major']
        del s['department']
        del s['class_name']
        s__ = get_object_or_404(Student, pk=s['id']);
        s['stu_name'] = s__.user.name
        s['gender'] = s__.user.gender
        if not sti:
            stu_list.append(s)
    context['student_list'] = stu_list
    return JsonResponse(context)


def add_revise_record(req, param1):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    courseid = req.session['course_id']

    try:
        sub_rec = AssignmentSubmitRecord.objects.get(id=param1)
        rev_rec = ReviseRecord()
        rev_rec.course = Course.objects.get(id=courseid)
        rev_rec.assignment = sub_rec.assignment
        user = get_object_or_404(User, pk=req.session['user_id'])
        print('user.id:', user.id)
        teacher = Teacher.objects.get(user=user)
        rev_rec.teacher = teacher
        rev_rec.team = sub_rec.team
        rev_rec.score = req.POST["score"]
        rev_rec.comment = req.POST["revision_comment"]
        rev_rec.save()
    except Exception as e:
        print('出错了：', e)

    context = {}
    context['course_id'] = courseid
    s = str(sub_rec.assignment.id)
    return HttpResponseRedirect('/teachers/show_team_assignment/' + s + '/')


def upload_grade_item(req, param1):
    gradeitem = GradeItem.objects.get(id=param1)
    courseid = req.session['course_id']

    course = Course.objects.get(id=courseid)
    team_list = Team.objects.filter(course=course)
    graderecords = GradeRecord.objects.filter(course=course).filter(gradeitem=gradeitem)

    team_score_list = []
    for team in team_list:
        t = {}
        t['id'] = team.id
        t['name'] = team.name
        temp = graderecords.filter(team=team)
        if temp:
            for i in temp:
                t['score'] = i.score
        else:
            t['score'] = 0
        team_score_list.append(t)
    print(team_score_list)
    context = {}
    context['team_score_list'] = team_score_list
    context['action'] = "/teachers/input_item_score/" + param1
    selectCourseList = CourseTeacher.objects.filter(teacher__user__id=req.session['user_id'])
    context['selectCourseList'] = selectCourseList
    return render(req, 'teachers/uploadGradeRecord.html', context)


def setPassword(request):
    result = False
    if request.POST:
        try:
            user = User.objects.get(id=request.session['user_id'], password=request.POST['oldPassword'])
            result = True
        except Exception as e:
            result = False
            print(e)
        if result:
            user.password = request.POST['newPassword']
            user.save()

            return HttpResponse("<script>alert('修改成功!');window.location.href='./teachers/';</script>")
        else:
            return HttpResponse("<script>alert('修改失败!');window.location.href='./teachers/';</script>")
    else:
        return render(request, 'students/setPassword.html')
    selectCourseList = CourseTeacher.objects.filter(teacher__user__id=req.session['user_id'])
    return render(req, 'teachers/setPassword.html', {'selectCourseList': selectCourseList})


def download_grade_excel(req, param1):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))

    courseid = req.session['course_id']

    try:
        def file_iterator(file_name, chunk_size=512):
            with open(file_name, 'rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        excel = xlwt.Workbook()
        sheet = excel.add_sheet(u"登分表")
        param1 = int(param1)
        if param1 == 1:
            sheet.write(0, 0, u'学号')
            sheet.write(0, 1, u'姓名')
            sheet.write(0, 2, u'分数')
            teaminfos = StudentTeamInfo.objects.filter(course__id=courseid)
            for cnt, info in enumerate(teaminfos):
                sheet.write(cnt + 1, 0, info.student.user.id)
                sheet.write(cnt + 1, 1, info.student.user.name)
            ename = u"个人成绩登分表.xls"
        elif param1 == 2:
            sheet.write(0, 0, u'团队编号')
            sheet.write(0, 1, u'团队名')
            sheet.write(0, 2, u'分数')
            teams = Team.objects.filter(course__id=courseid)
            for cnt, team in enumerate(teams):
                sheet.write(cnt + 1, 0, team.id)
                sheet.write(cnt + 1, 1, team.name)
            ename = u"团队成绩登分表.xls"
        else:
            raise Exception(u"没有对应的编号，无法下载excel")

        filepath = os.path.join(r"attachments", ename)
        excel.save(filepath)
        response = StreamingHttpResponse(file_iterator(filepath))
        response['Content-Type'] = 'application/octet-stream'
        print('attachment;filename="{0}"'.format(str(ename)))
        response['Content-Disposition'] = ('attachment;filename="{0}"'.format(str(ename)).encode('utf-8'))
        return response
    except Exception as e:
        print(e)
        return HttpResponse('download_file下载这里完全在瞎搞')


def set_grades(req, param1, param2):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    user_id = req.session["user_id"]
    courseid = req.session['course_id']
    try:
        if req.method == 'POST':
            file = req.FILES['grade_file']
            if not file:
                return HttpResponse("<script>alert('请选择文件！');window.location.href='/teachers/upload_grades/';</script>")
            savefile(file, 'temp/')
            data = xlrd.open_workbook('temp/' + file.name)
            table = data.sheets()[0]
            rows = table.nrows
            cols = table.ncols
            ass = get_object_or_404(Assignment, pk=param2)
            course = Course.objects.get(id=courseid)
            param1 = int(param1)
            if param1 == 1:
                pass
            elif param1 == 2:
                for i in range(1, rows):
                    gra_rec = GradeRecord()
                    rev_rec = ReviseRecord()
                    rev_rec.assignment = ass
                    rev_rec.course = course
                    teacher = Teacher.objects.get(user_id=user_id)
                    rev_rec.teacher = teacher
                    for j in range(cols):
                        if table.row(0)[j].value == u'团队编号':
                            team = Team.objects.get(id=table.row(i)[j].value)
                            rev_rec.team = team
                            gra_rec.team = team
                        elif table.row(0)[j].value == '分数':
                            rev_rec.score = table.row(i)[j].value
                            gra_rec.score = table.row(i)[j].value
                        gradeItem = GradeItem.objects.get(course_id=courseid, name=ass.name)
                        gra_rec.gradeitem = gradeItem
                        gra_rec.course = course
                    rev_rec.save()
                    gra_rec.save()
            else:
                raise Exception("网址参数不对")
    except Exception as e:
        print('set_grades：', e)
    return HttpResponseRedirect(reverse('teachers:upload_grades'))


def savefile(f, filedirpath):
    file_name = ""
    try:
        # 如果课程作业所在的文件夹不存在，生成一个文件夹
        if not os.path.exists(filedirpath):
            os.makedirs(filedirpath)

        file_name = filedirpath + f.name
        destination = open(file_name, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
    except Exception as e:
        print(e)
        return False
    return True


def export_assignment_report(req, param1):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))

    courseid = req.session['course_id']

    try:
        def file_iterator(file_name, chunk_size=512):
            with open(file_name, 'rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        excel = xlwt.Workbook()
        sheet = excel.add_sheet(u"累计作业列表")
        sheet.write(0, 0, u'团队编号')
        sheet.write(0, 1, u'团队名称')
        sheet.write(0, 2, u'团队负责人')
        sheet.write(0, 3, u'完成作业数')
        teams = Team.objects.filter(course__id=courseid)
        for cnt, tm in enumerate(teams):
            sheet.write(cnt + 1, 0, tm.id)
            sheet.write(cnt + 1, 1, tm.name)
            sheet.write(cnt + 1, 2, tm.head.user.name)
            sub_id_list = []
            recs = AssignmentSubmitRecord.objects.filter(course__id=courseid, team=tm)
            for rec in recs:
                sub_id_list.append(rec.assignment.id)
            sub_id_set = set(sub_id_list)
            sheet.write(cnt + 1, 3, sub_id_set.__len__())
        ename = u"个人成绩登分表.xls"

        filepath = os.path.join(r"attachments", ename)
        excel.save(filepath)
        response = StreamingHttpResponse(file_iterator(filepath))
        response['Content-Type'] = 'application/octet-stream'
        print('attachment;filename="{0}"'.format(str(ename)))
        response['Content-Disposition'] = ('attachment;filename="{0}"'.format(str(ename)).encode('utf-8'))
        return response
    except Exception as e:
        print('export_assignment_report:', e)
        return HttpResponse('download_file下载这里完全在瞎搞')


def submit_team(request):
    context = {}
    jsonstr = request.POST['json']
    team_list = json.loads(jsonstr)
    for team in team_list['team']:
        team_id = int(team['team_id'])
        team_obj = Team.objects.get(pk=team_id)
        student_team_info = StudentTeamInfo.objects.filter(team=team_obj)
        course_id = None
        for sti in student_team_info:
            course_id=sti.course.id
            sti.delete()
        for stu in team['stu_id']:
            stu_id = int(stu['id'])
            stu_obj = Student.objects.get(pk=stu_id)
            course_obj = Course.objects.get(pk=course_id)
            sti_info = StudentTeamInfo()
            sti_info.team = team_obj
            sti_info.role = '成员'
            sti_info.course = course_obj
            sti_info.student = stu_obj
            sti_info.save()
    return JsonResponse(context)

def export_excel_total_grade(req):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    courseid = req.session['course_id']

    def file_iterator(file_name, chunk_size=512):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    excel = xlwt.Workbook()
    sheet1 = excel.add_sheet(u"团队分数表")
    sheet2 = excel.add_sheet(u"个人分数表")
    ename = u"成绩登分表.xls"

    sheet1.write(0,0,u'团队编号')
    sheet1.write(0,1,u'团队名称')
    sheet1.write(0,2,u'团队分数')

    idlist = req.POST.getlist('idlist')
    namelist = req.POST.getlist('namelist')
    gradelist = req.POST.getlist('gradelist')
    len = list(idlist).__len__()
    for cnt in range(0,len):
        sheet1.write(cnt+1,0,idlist[cnt])
        sheet1.write(cnt+1,1,namelist[cnt])
        sheet1.write(cnt+1,2,gradelist[cnt])

    sheet2.write(0, 0, u'学号')
    sheet2.write(0, 1, u'姓名')
    sheet2.write(0, 2, u'分数')
    cnt = 1
    for index,id in enumerate(idlist):
        members = StudentTeamInfo.objects.filter(team__id=id)
        for mem in members:
            sheet2.write(cnt, 0, mem.student.user.id)
            sheet2.write(cnt, 1, mem.student.user.name)
            sheet2.write(cnt, 2, float(gradelist[index])*mem.weight)
            cnt += 1


    filepath = os.path.join(r"attachments", ename)
    excel.save(filepath)
    response = StreamingHttpResponse(file_iterator(filepath))
    response['Content-Type'] = 'application/octet-stream'
    print('attachment;filename="{0}"'.format(str(ename)))
    response['Content-Disposition'] = ('attachment;filename="{0}"'.format(str(ename)).encode('utf-8'))
    return response
