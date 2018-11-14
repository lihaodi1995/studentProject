from django.conf.urls import url

from . import views

app_name = 'admin'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^set_semester/', views.set_semester, name='set_semester'),
	url(r'^add_semester/', views.add_semester, name='add_semester'),
	url(r'^edit_semester/', views.edit_semester, name='edit_semester'),
	url(r'^edit_semester_i/', views.edit_semester_i, name='edit_semester_i'),
	url(r'^delete_semester/', views.delete_semester, name='delete_semester'),

	url(r'^set_teacher/', views.set_teacher, name='set_teacher'),
	url(r'^add_teacher/', views.add_teacher, name='add_teacher'),
	url(r'^add_one_teacher/', views.add_one_teacher, name='add_one_teacher'),
	url(r'^delete_teacher/', views.delete_teacher, name='delete_teacher'),
	url(r'^edit_teacher/', views.edit_teacher, name='edit_teacher'),
	url(r'^edit_teacher_i/', views.edit_teacher_i, name='edit_teacher_i'),

	url(r'^set_student/', views.set_student, name='set_student'),
	url(r'^add_student/', views.add_student, name='add_student'),
	url(r'^add_one_student/', views.add_one_student, name='add_one_student'),
	url(r'^delete_student/', views.delete_student, name='delete_student'),
	url(r'^edit_student/', views.edit_student, name='edit_student'),
	url(r'^edit_student_i/', views.edit_student_i, name='edit_student_i'),

	url(r'^set_course/', views.set_course, name='set_course'),
	url(r'^add_course/', views.add_course, name='add_course'),
	url(r'^edit_course/', views.edit_course, name='edit_course'),
	url(r'^edit_course_i/', views.edit_course_i, name='edit_course_i'),
	url(r'^delete_course/', views.delete_course, name='delete_course'),

	url(r'^upload_students_info/', views.upload_students_info, name='upload_students_info'),
	url(r'^upload_teachers_info/', views.upload_teachers_info, name='upload_teachers_info'),
	url(r'^set_password/', views.set_password, name='set_password'),

	url(r'^course_add_teacher/', views.course_add_teacher, name='course_add_teacher'),
	url(r'^course_add_student/', views.course_add_student, name='course_add_student'),
]
