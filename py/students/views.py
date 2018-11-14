# coding=utf8
import datetime
import os

from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

# Create your views here.
from users.models import *


def index(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	course_id = 1
	course = None
	selectCourseList = None
	try:
		course = Course.objects.get(id=course_id)
		selectCourseList = SelectCourse.objects.filter(student__user__id=request.session['user_id'])
	except Exception as e:
		print(e)
	return render(request, 'students/index.html', {'course': course, 'selectCourseList': selectCourseList})


def student_info(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	student = None
	selectCourseList = None
	try:
		student = Student.objects.get(user__id=request.session['user_id'])
		selectCourseList = SelectCourse.objects.filter(student__user__id=request.session['user_id'])

	except Exception as e:
		print(e)

	return render(request, 'students/studentInfo.html', {'student': student, 'selectCourseList': selectCourseList})


def courseInfo(request, course_id):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	request.session['course_id'] = course_id
	context = {}
	try:
		course = Course.objects.get(id=course_id)
		context['course'] = course
	except Exception as e:
		print(e)
	selectCourseList = SelectCourse.objects.filter(student__user__id=request.session['user_id'])
	context['selectCourseList'] = selectCourseList
	return render(request, 'students/courseInfo.html', context)


def courseResource(req):
    if not req.session.get('user_id', None):
        return HttpResponseRedirect(reverse('login'))
    courseid = req.session['course_id']
    filelist = []
    try:
        crs = Course.objects.get(id=courseid)
        cflist = CourseFile.objects.filter(course=crs)
        course_tag_list = Tag.objects.filter(course=crs)
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
    selectCourseList = SelectCourse.objects.filter(student__user__id=req.session['user_id'])
    return render(req, 'students/getResource.html',
                  {'course_tag_list': course_tag_list, 'courseid': courseid, 'filelist': filelist,
                   'selectCourseList': selectCourseList})

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
    return render(req, 'students/getResource.html', context)
	

def courseResourceTag(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	tagFileDict = {}
	course_id = 1
	course = Course.objects.get(id=course_id)
	tagList = Tag.objects.filter(course=course)
	for tag in tagList:
		tagRecord = TagRecord.objects.filter(tag=tag)
		templ = []
		for tr in tagRecord:
			templ.append(tr.file.name)
		print(templ)
		tagFileDict[tag.tag] = templ
		print(tagFileDict)
	selectCourseList = SelectCourse.objects.filter(student__user__id=request.session['user_id'])
	return render(request, 'students/courseResourceTag.html',
				  {'tagRecord': tagRecord, 'tagFileDict': tagFileDict, 'tagList': tagList,
				   'selectCourseList': selectCourseList})


def set_group(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	user_id = request.session.get('user_id', None)
	user = get_object_or_404(User, pk=user_id)
	student = Student.objects.get(user=user)
	apply = None
	team_list = Team.objects.all()
	my_team = None
	try:
		my_team = Team.objects.filter(head=student)
		apply = Apply.objects.get(apply_people=student)
	except Exception as e:
		print(e)
	selectCourseList = SelectCourse.objects.filter(student__user__id=request.session['user_id'])
	return render(request, 'students/setGroup.html',
				  {'team_list': team_list, 'my_apply': apply, "my_team": my_team, 'selectCourseList': selectCourseList})


def add_group(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	course_id = 1
	team = None
	student = None
	course = None
	try:
		course = Course.objects.get(id=course_id)
		user_id = request.session.get('user_id', None)
		user = get_object_or_404(User, pk=user_id)
		student = Student.objects.get(user=user)
		team = Team.objects.filter(head=student)
	except Exception as e:
		print(e)
	if team:
		return HttpResponse("<script>alert('你只能拥有一个团队!');window.location.href='/students/set_group/';</script>")
	else:
		team = Team()
		team.name = request.POST['name']
		team.head = student
		team.status = '组建中'
		team.people_number = 1
		team.course = course
		team.submitter = student
		team.save()
		team_info = StudentTeamInfo()
		team_info.team = team
		team_info.course = course
		team_info.student = student
		team_info.role = '负责人'
		team_info.save()
	return HttpResponseRedirect(reverse('students:set_group'))


def my_group(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	user_id = request.session.get('user_id', None)
	user = get_object_or_404(User, pk=user_id)
	student = Student.objects.get(user=user)
	selectCourseList = SelectCourse.objects.filter(student__user__id=request.session['user_id'])
	apply = None
	try:
		apply = Apply.objects.get(apply_people=student)
	except Exception as e:
		print(e)
	if apply:
		team = apply.team
		apply_list = Apply.objects.filter(team=team)
		return render(request, 'students/myGroup.html',
					  {'apply_list': apply_list, 'team': team, 'is_head': True, 'selectCourseList': selectCourseList})
	else:
		try:
			team = Team.objects.get(head=student)
			apply_list = None
			try:
				apply_list = Apply.objects.filter(team=team)
			except Exception as e:
				print(e)
			return render(request, 'students/myGroup.html', {'apply_list': apply_list, 'team': team, 'is_head': True,
															 'selectCourseList': selectCourseList})
		except Exception as e:
			print(e)
	return HttpResponse("<script>alert('你没有团队!');window.location.href='/students/set_group/';</script>")


def apply_group(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	user_id = request.session.get('user_id', None)
	user = get_object_or_404(User, pk=user_id)
	student = Student.objects.get(user=user)
	team_id = request.GET.get('id')
	team = get_object_or_404(Team, pk=team_id)
	student_team_info = StudentTeamInfo.objects.filter(student=student)
	if student_team_info:
		return HttpResponse("<script>alert('你已经拥有团队了!');window.location.href='/students/set_group/';</script>")
	else:
		apply_try = None
		try:
			apply_try = Apply.objects.get(apply_people=student)
		except Exception as e:
			print(e)
		if apply_try:
			return HttpResponse("<script>alert('你已经申请过团队了!');window.location.href='/students/set_group/';</script>")
		apply = Apply()
		apply.team = team
		apply.apply_status = '申请中'
		apply.apply_people = student
		apply.save()
	return HttpResponse("<script>alert('申请成功!');window.location.href='/students/set_group/';</script>")


def pass_apply(request):
	apply_id = request.GET.get('id')
	apply = get_object_or_404(Apply, pk=apply_id)
	apply.apply_status = '通过'
	apply.save()
	team_info = StudentTeamInfo()
	team_info.team = apply.team
	team_info.course = apply.team.course
	team_info.student = apply.apply_people
	team_info.role = '成员'
	team_info.save()
	return HttpResponseRedirect(reverse('students:my_group'))


def delete_member(request):
	student_id = request.GET.get('id')
	student = get_object_or_404(Student, pk=student_id)
	team_info = StudentTeamInfo.objects.filter(student=student)
	apply = Apply.objects.filter(apply_people=student)
	apply.delete()
	team_info.delete()
	return HttpResponseRedirect(reverse('students:my_group'))


def apply_to_teacher(request):
	team_id = request.GET.get('id')
	team = get_object_or_404(Team, pk=team_id)
	team.status = '申请中'
	team.save()
	return HttpResponseRedirect(reverse('students:my_group'))


def refuse_apply(request):
	apply_id = request.GET.get('id')
	apply = get_object_or_404(Apply, pk=apply_id)
	apply.apply_status = '拒绝'
	apply.save()
	return HttpResponseRedirect(reverse('students:my_group'))


def delete_apply(request):
	apply_id = request.GET.get('id')
	apply = get_object_or_404(Apply, pk=apply_id)
	apply.delete()
	return HttpResponseRedirect(reverse('students:set_group'))


def add_member(request):
	user_id = request.POST['user_id']
	team_id = request.POST['team_id']
	team = Team.objects.get(id=team_id)
	user = User.objects.filter(id=user_id)
	if user:
		student = Student.objects.get(user=user)
		apply = Apply.objects.filter(apply_people=student)
		if apply:
			return HttpResponse("<script>alert('该用户已经申请团队!');window.location.href='/students/my_group/';</script>")
		else:
			apply = Apply()
			apply.team = team
			apply.apply_status = '申请中'
			apply.apply_people = student
			apply.save()
			return HttpResponseRedirect(reverse('students:my_group'))
	else:
		return HttpResponse("<script>alert('未找到该用户!');window.location.href='/students/my_group/';</script>")


def disband_group(request):
	team_id = request.GET.get('id')
	team = get_object_or_404(Team, pk=team_id)
	team.delete()
	return HttpResponseRedirect(reverse('students:set_group'))


def group_affair(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	user_id = request.session.get('user_id', None)
	user = get_object_or_404(User, pk=user_id)
	student = Student.objects.get(user=user)
	team = None
	selectCourseList = SelectCourse.objects.filter(student__user__id=request.session['user_id'])
	try:
		team = Team.objects.get(head=student)
	except Exception as e:
		print(e)
	if team:
		team_info_list = StudentTeamInfo.objects.filter(team=team)
		return render(request, 'students/groupAffair.html',
					  {'team': team, 'team_info_list': team_info_list, 'selectCourseList': selectCourseList})
	else:
		return HttpResponse(
			"<script>alert('你不是负责人/组长，无法使用该功能哦 :P');window.location.href='/students/set_group/';</script>")


def set_weight(request):
	id = request.POST['id']
	weight = request.POST['weight']
	info = get_object_or_404(StudentTeamInfo, pk=id)
	info.weight = weight
	info.save()
	return HttpResponseRedirect(reverse('students:group_affair'))


def update_role(request):
	id = request.POST['id']
	role = request.POST['role']
	info = get_object_or_404(StudentTeamInfo, pk=id)
	info.role = role
	info.save()
	return HttpResponseRedirect(reverse('students:group_affair'))


def get_homework(request, course_id):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	request.session['course_id'] = course_id
	assignmentList = Assignment.objects.filter(course__id=course_id)
	selectCourseList = SelectCourse.objects.filter(student__user__id=request.session['user_id'])
	return render(request, 'students/getHomework.html',
				  {'assignmentList': assignmentList, 'selectCourseList': selectCourseList})


def get_resource(request):
	selectCourseList = SelectCourse.objects.filter(student__user__id=request.session['user_id'])
	return render(request, 'students/resources.html', {'selectCourseList': selectCourseList})


def ass_detail(request, param1):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	user_id = request.session.get('user_id', None)
	user = get_object_or_404(User, pk=user_id)
	student = Student.objects.get(user=user)
	ass = get_object_or_404(Assignment, pk=param1)
	upload_permission = False
	team_info = None
	team_id = None
	try:
		team_info = StudentTeamInfo.objects.get(student=student)
	except Exception as e:
		pass
	if team_info:
		if team_info.role == '负责人':
			upload_permission = True
			team_id = team_info.team.id
	if ass.type == '个人':
		upload_permission = True
	selectCourseList = SelectCourse.objects.filter(student__user__id=request.session['user_id'])
	return render(request, 'students/assignmentDetails.html', {'ass': ass, 'upload_permission': upload_permission,
															   'team_id': team_id,
															   'selectCourseList': selectCourseList})


def submit_ass(req):
	if not req.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	user_id = req.session.get('user_id', None)
	user = get_object_or_404(User, pk=user_id)
	student = Student.objects.get(user=user)
	course_id = req.session['course_id']
	if req.method == "POST":  # 请求方法为POST时，进行处理
		files_list_str = ""
		try:
			myFiles = req.FILES.getlist("stu_ass", None)  # 获取上传的文件，如果没有文件，则默认为None
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
				# dfile.submitter = req.session['id']
				dfile.submitter = 1
				dfile.size = os.path.getsize(tfile)
				dfile.save()  # 首次新建文件索引记录

				# print(dfile.id,'|||',dfile.type)
				tname = str(dfile.id) + str(dfile.type)
				newname = os.path.join(path, tname)
				os.rename(tfile, newname)
				dfile.address = newname
				dfile.save()  # 重命名文件，更新文件索引记录

				file_str = str(dfile.id)
				files_list_str += file_str + ','

		except Exception as e:
			print(e, 'z')
		ass_record = AssignmentSubmitRecord()
		ass_record.submitter = student
		ass_id = req.POST['ass_id']
		ass_up = Assignment.objects.get(id=ass_id)
		ass_record.assignment = ass_up
		ass_record.file_set = files_list_str
		ass_record.text = req.POST['ass_text']
		if ass_record.submit_times:
			ass_record.submit_times += 1
		else:
			ass_record.submit_times = 1
		ass_record.course = get_object_or_404(Course, pk=course_id)
		if req.POST['team_id']:
			try:
				team = Team.objects.get(id=req.POST['team_id'])
				ass_record.team = team
			except Exception as e:
				pass
		ass_record.time = datetime.date.today()
		ass_record.save()
	return HttpResponseRedirect('/students/get_homework/' + course_id)


def download(request, file_id):
	def file_iterator(file_name, chunk_size=512):
		with open(file_name, 'rb') as f:
			while True:
				c = f.read(chunk_size)
				if c:
					yield c
				else:
					break


	file = File.objects.get(id=file_id)  # 根据部署环境，更改文件地址（文件地址存在服务器中，但是要适配本地环境，有问题问冯嘉晨）
	the_file_name = str(file.address)
	response = StreamingHttpResponse(file_iterator(the_file_name))

	# 以下代码用于将浏览器读取的数据变成文件
	response['Content-Type'] = 'application/octet-stream'
	response['Content-Disposition'] = 'attachment;filename=%s' % file.name

	return response


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

			return HttpResponse("<script>alert('修改成功!');window.location.href='./students/';</script>")
		else:
			return HttpResponse("<script>alert('修改失败!');window.location.href='./students/';</script>")
	else:
		return render(request, 'students/setPassword.html')

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