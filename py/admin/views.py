# coding=utf8
import os

import xlrd
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, loader, get_object_or_404
from django.urls import reverse

from users.models import *


# Create your views here.



def index(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	return render(request, 'admin/index.html', {})


def set_semester(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	try:
		semester_model = Semester.objects.all()
		template = loader.get_template('admin/setSemester.html')
		return HttpResponse(template.render({'semester': semester_model}, request))
	except Exception as e:
		print(e)
		raise Http404("学期不存在！")


def add_semester(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	try:
		semester = Semester()
		semester.name = request.POST['name']
		semester.start_time = request.POST['start_time']
		semester.end_time = request.POST['end_time']
		semester.save()
		return HttpResponseRedirect(reverse('admin:set_semester'))
	except Exception as e:
		print(e)
		HttpResponse(status=500)


def edit_semester(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	semester_id = request.GET.get('id')
	semester = get_object_or_404(Semester, pk=semester_id)
	return render(request, 'admin/editSemester.html', {'semester': semester})


def edit_semester_i(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	semester_id = request.POST['id']
	semester = get_object_or_404(Semester, pk=semester_id)
	semester.name = request.POST['name']
	semester.start_time = request.POST['start_time']
	semester.end_time = request.POST['end_time']
	semester.save()
	return HttpResponseRedirect(reverse('admin:set_semester'))


def delete_semester(request):
	context = {}
	if request.session.get('user_id', None):
		semester_id = request.GET.get('id')
		semester = get_object_or_404(Semester, pk=semester_id)
		semester.delete()
		context['status'] = 'success'
		context['info'] = 'delete semester success'
		return JsonResponse(context)
	context['status'] = 'error'
	context['info'] = 'you have not login'
	return JsonResponse(context)


def set_course(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	try:
		course_model = Course.objects.all()
		semester_list = Semester.objects.all()
		return render(request, 'admin/setCourse.html', {'course': course_model, 'semester_list': semester_list})
	except Exception as e:
		print(e)
		raise Http404("课程或学期不存在！")


def add_course(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	course = Course()
	course.name = request.POST['name']
	semester_id = request.POST['semester_id']
	semester = get_object_or_404(Semester, pk=semester_id)
	course.semester = semester
	course.credit = request.POST['credit']
	course.weeks = request.POST['weeks']
	course.time = request.POST['time']
	course.address = request.POST['address']
	course.status = '开启'
	course.save()
	print(course.id)
	semester_list = Semester.objects.all()
	return HttpResponseRedirect('/admin/edit_course/?id=' + str(course.id),
								{'course': course, 'semester_list': semester_list})


def edit_course(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	request.session['course_id'] = request.GET.get('id')
	course_id = request.GET.get('id')
	course = get_object_or_404(Course, pk=course_id)
	semester_list = Semester.objects.all()
	teacher = Teacher.objects.all()
	select_course_teacher = CourseTeacher.objects.filter(course__id=course_id)
	select_course_teacher_list = []
	for i in select_course_teacher:
		select_course_teacher_list.append(int(i.teacher.id))
	whether_techer_select_course_list = []
	for i in teacher:
		if i.id in select_course_teacher_list:
			whether_techer_select_course_list.append(1)
		else:
			whether_techer_select_course_list.append(0)
	print(whether_techer_select_course_list)
	test=zip(teacher,whether_techer_select_course_list)

	print(test)
	student = Student.objects.all()
	student_selected = SelectCourse.objects.filter(course__id=course_id)
	stu_select_list = []
	temp = True
	for i in student:
		temp = True
		for j in student_selected:
			if (j.student.id == i.id):
				temp = False
		if temp:
			stu_select_list.append(i.id)
	student_un_select = Student.objects.filter(id__in=stu_select_list)
	print(student_un_select)
	return render(request, 'admin/editCourse.html',
				  {'course': course, 'semester_list': semester_list, 'teacher': test,
				   'student_un_select': student_un_select,
				   'student_selected': student_selected,
				   'whether_techer_select_course_list': whether_techer_select_course_list})


def edit_course_i(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	request.session['course_id'] = request.GET.get('id')
	course_id = request.POST['id']
	course = get_object_or_404(Course, pk=course_id)
	course.name = request.POST['name']
	semester_id = request.POST['semester_id']
	semester = get_object_or_404(Semester, pk=semester_id)
	course.semester = semester
	course.credit = request.POST['credit']
	course.weeks = request.POST['weeks']
	course.time = request.POST['time']
	course.address = request.POST['address']
	# course.team_people_upper_limit = request.POST['team_people_upper_limit']
	# course.team_people_lower_limit = request.POST['team_people_lower_limit']
	course.status = '开启'
	course.save()
	return HttpResponseRedirect(reverse('admin:set_course'))


def delete_course(request):
	context = {}
	if request.session.get('user_id', None):
		course_id = request.GET.get('id')
		course = get_object_or_404(Course, pk=course_id)
		course.delete()
		context['status'] = 'success'
		context['info'] = 'delete course success'
		return JsonResponse(context)
	context['status'] = 'error'
	context['info'] = 'you have not login'
	return JsonResponse(context)


def close_course(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	return HttpResponseRedirect(reverse('admin:index'))


def course_add_teacher(request):
	courseid = request.session['course_id']
	course = Course.objects.get(id=courseid)
	teacherid = int(request.GET.get('teacher_id'))
	teacher = Teacher.objects.get(id=teacherid)
	alread_course_teacher = CourseTeacher.objects.filter(teacher__id=teacherid, course__id=courseid)
	alread_course_teacher_list = []
	for i in alread_course_teacher:
		alread_course_teacher_list.append(i.teacher.id)
		print(i.teacher.id)
	if teacherid in alread_course_teacher_list:
		print("#######")
	else:
		courseTeacher = CourseTeacher()
		courseTeacher.course = course
		courseTeacher.teacher = teacher
		courseTeacher.save()
	return HttpResponseRedirect(reverse('admin:set_course'))


def course_add_student(request):
	courseid = request.session['course_id']
	course = Course.objects.get(id=courseid)
	studentid = request.GET.get('student_id')
	student = Student.objects.get(id=studentid)
	selectCourse = SelectCourse()
	selectCourse.course = course
	selectCourse.student = student
	selectCourse.save()
	return HttpResponseRedirect(reverse('admin:set_course'))


def set_teacher(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	try:
		teacher_list = Teacher.objects.all()
		paginator = Paginator(teacher_list, 20)
	except Exception as e:
		print(e)

	page = request.GET.get('page')
	try:
		teachers = paginator.page(page)
	except PageNotAnInteger:
		teachers = paginator.page(1)
	except EmptyPage:
		teachers = paginator.page(paginator.num_pages)
	return render(request, 'admin/setTeacher.html', {'teacher': teachers})


def add_teacher(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	return render(request, 'admin/addTeacher.html', {})


def add_one_teacher(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	try:
		temp_usr = User.objects.get(id=request.POST['user_idd'])
		return HttpResponse("<script>alert('用户不能重复！');window.location.href='/admin/set_teacher/';</script>")
	except Exception as e:
		if request.POST['user_idd'] == "":
			return HttpResponse("<script>alert('必须填入工号！');window.location.href='/admin/set_teacher/';</script>")
		user = User()
		user.id = request.POST['user_idd']
		user.name = request.POST['name']
		user.role = 2
		user.password = request.POST['user_idd']
		user.email = request.POST['email']
		user.gender = request.POST['gender']
		user.address = request.POST['address']
		user.phone_number = request.POST['phone_number']
		user.save()

		teacher = Teacher()
		teacher.user = user
		teacher.position = request.POST['position']
		teacher.save()
		return HttpResponseRedirect(reverse('admin:set_teacher'))


def delete_teacher(request):
	context = {}
	if request.session.get('user_id', None):
		teacher_id = request.GET.get('id')
		teacher = get_object_or_404(Teacher, pk=teacher_id)
		user = teacher.user
		teacher.delete()
		user.delete()
		context['status'] = 'success'
		context['info'] = 'delete teacher success'
		return JsonResponse(context)
	return HttpResponse(status=500)


def edit_teacher(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	teacher_id = request.GET.get('id')
	teacher = get_object_or_404(Teacher, pk=teacher_id)
	return render(request, 'admin/editTeacher.html', {'teacher': teacher})


def edit_teacher_i(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	teacher_id = request.POST['t_id']
	teacher = get_object_or_404(Teacher, pk=teacher_id)
	user = teacher.user
	teacher.delete()
	user.delete()

	user = User()
	user.id = request.POST['user_id']
	user.name = request.POST['name']
	user.role = 2
	user.password = request.POST['user_id']
	user.email = request.POST['email']
	user.gender = request.POST['gender']
	user.address = request.POST['address']
	user.phone_number = request.POST['phone_number']
	user.save()

	teacher = Teacher()
	teacher.user = user
	teacher.position = request.POST['position']
	teacher.save()
	return HttpResponseRedirect(reverse('admin:set_teacher'))


def set_student(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	try:
		student_list = Student.objects.all()
		paginator = Paginator(student_list, 20)
	except Exception as e:
		print(e)

	page = request.GET.get('page')
	try:
		students = paginator.page(page)
	except PageNotAnInteger:
		students = paginator.page(1)
	except EmptyPage:
		students = paginator.page(paginator.num_pages)
	return render(request, 'admin/setStudent.html', {'student': students})


def add_student(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	return render(request, 'admin/addStudent.html', {})


def edit_student(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	student_id = request.GET.get('id')
	student = get_object_or_404(Student, pk=student_id)
	return render(request, 'admin/editStudent.html', {'student': student})


def edit_student_i(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	student_id = request.POST['s_id']
	student = get_object_or_404(Student, pk=student_id)
	user = student.user
	student.delete()
	user.delete()
	user = User()
	user.id = request.POST['user_id']
	user.name = request.POST['name']
	user.role = 3
	user.passwd = request.POST['user_id']
	user.email = request.POST['email']
	user.gender = request.POST['gender']
	user.address = request.POST['address']
	user.phone_number = request.POST['phone_number']
	user.save()

	student = Student()
	student.user = user
	student.major = request.POST['major']
	student.department = request.POST['department']
	student.class_name = request.POST['class_name']
	student.save()
	return HttpResponseRedirect(reverse('admin:set_student'))


def add_one_student(request):
	if not request.session.get('user_id', None):
		return HttpResponseRedirect(reverse('login'))
	user = User()
	user.id = request.POST['user_id']
	user.name = request.POST['name']
	user.role = 3
	user.passwd = request.POST['user_id']
	user.email = request.POST['email']
	user.gender = request.POST['gender']
	user.address = request.POST['address']
	user.phone_number = request.POST['phone_number']
	user.save()

	student = Student()
	student.user = user
	student.major = request.POST['major']
	student.department = request.POST['department']
	student.class_name = request.POST['class_name']
	student.save()

	return HttpResponseRedirect(reverse('admin:set_student'))


def delete_student(request):
	if request.session.get('user_id', None):
		student_id = request.GET.get('id')
		student = get_object_or_404(Student, pk=student_id)
		user = student.user
		student.delete()
		user.delete()
		context = {}
		context['status'] = 'success'
		context['info'] = 'delete student success'
		return JsonResponse(context)
	return HttpResponse(status=500)


def upload_students_info(request):
	if request.method == 'POST':
		file = request.FILES['student_file']
		if not file:
			return HttpResponse("<script>alert('请选择文件！');window.location.href='/admin/set_student/';</script>")
		savefile(file, 'temp/')
		data = xlrd.open_workbook('temp/' + file.name)
		table = data.sheets()[0]
		rows = table.nrows
		cols = table.ncols
		for i in range(1, rows):
			student = {}
			for j in range(cols):
				if table.row(0)[j].value == '学号':
					student['id'] = table.row(i)[j].value
				elif table.row(0)[j].value == '姓名':
					student['name'] = table.row(i)[j].value
				elif table.row(0)[j].value == '性别':
					student['sex'] = table.row(i)[j].value
				elif table.row(0)[j].value == '院系':
					student['department'] = table.row(i)[j].value
			user = User()
			user.id = str(student['id'])
			user.name = student['name']
			user.role = 3
			user.password = str(student['id'])
			user.gender = student['sex']
			user.save()
			dstudent = Student()
			dstudent.user = user
			dstudent.department = student['department']
			dstudent.save()
	return HttpResponseRedirect(reverse('admin:set_student'))


def upload_teachers_info(request):
	if request.method == 'POST':
		file = request.FILES['teacher_file']
		if not file:
			return HttpResponse("<script>alert('请选择文件！');window.location.href='/admin/set_student/';</script>")
		savefile(file, 'temp/')
		data = xlrd.open_workbook('temp/' + file.name)
		table = data.sheets()[0]
		rows = table.nrows
		cols = table.ncols
		for i in range(1, rows):
			teacher = {}
			for j in range(cols):
				if table.row(0)[j].value == '工号':
					teacher['id'] = table.row(i)[j].value
				elif table.row(0)[j].value == '姓名':
					teacher['name'] = table.row(i)[j].value
				elif table.row(0)[j].value == '学院':
					teacher['department'] = table.row(i)[j].value
				elif table.row(0)[j].value == '职称':
					teacher['position'] = table.row(i)[j].value
			user = User()
			user.id = str(teacher['id'])
			user.name = teacher['name']
			user.role = 2
			user.password = str(teacher['id'])
			user.save()
			dteacher = Teacher()
			dteacher.user = user
			dteacher.position = teacher['position']
			dteacher.save()
	return HttpResponseRedirect(reverse('admin:set_teacher'))


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


def set_password(request):
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

			return HttpResponse("<script>alert('修改成功!');window.location.href='./admin/';</script>")
		else:
			return HttpResponse("<script>alert('修改失败!');window.location.href='./admin/';</script>")
	else:
		return render(request, 'admin/setPassword.html', {})
