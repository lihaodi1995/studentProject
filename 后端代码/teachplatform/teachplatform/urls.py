"""teachplatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from teachapp.views_yc import login
from teachapp.views_yc import get_course_list_teacher, get_course_info_teacher, edit_course_info_teacher
from teachapp.views_yc import upload_course_resource_teacher, delete_course_resource_teacher, view_course_resource_teacher, create_directory_teacher
from teachapp.views_yc import get_student_list_teacher
from teachapp.views_yc import get_team_list_teacher, get_team_member_teacher, edit_team_member_teacher, agree_team_application_teacher, reject_team_application_teacher
from teachapp.views_yc import add_homework_teacher, delete_homework_teacher, get_homework_list_teacher, get_homework_info_teacher, edit_homework_basic_info_teacher, edit_homework_content_teacher, view_homework_attachment_teacher, upload_homework_attachment_teacher, delete_homework_attachment_teacher
from teachapp.views_yc import get_team_homework_list_teacher, view_team_homework_info_teacher, score_team_homework_teacher, download_team_homework_zip_teacher, upload_modified_homework_teacher
from teachapp.views_yc import export_team_excel_teacher, export_homework_excel_teacher, export_n_homework_excel_teacher, export_score_excel_teacher

from teachapp.views_lwj import setSemester, setCurrentSemester, getSemester, getAllSemester, deleteSemester, getCurrentSemesterWeeks, setCourse, getCourse, getAllCourse, deleteCourse, setUser, getAllUser, getUser, deleteUser, importUser, importCourse, importUserOfCourse, getUserOfCourse, deleteUserOfCourse
from teachapp.views_lwj import searchUser, addRelationship, getRelationship, deleteRelationship
from teachapp.views_lwj import sendMessage, getNewMessage, getAllMessage, read

from teachapp import views_ghz

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', login),
    url(r'^get_course_list_teacher/$', get_course_list_teacher),
    url(r'^get_course_info_teacher/$', get_course_info_teacher),
    url(r'^edit_course_info_teacher/$', edit_course_info_teacher),
    url(r'^upload_course_resource_teacher/$', upload_course_resource_teacher),
    url(r'^delete_course_resource_teacher/$', delete_course_resource_teacher),
    url(r'^view_course_resource_teacher/$', view_course_resource_teacher),
    url(r'^create_directory_teacher/$', create_directory_teacher),
    url(r'^get_student_list_teacher/$', get_student_list_teacher),
    url(r'^get_team_list_teacher/$', get_team_list_teacher),
    url(r'^get_team_member_teacher/$', get_team_member_teacher),
    url(r'^edit_team_member_teacher/$', edit_team_member_teacher),
    url(r'^agree_team_application_teacher/$', agree_team_application_teacher),
    url(r'^reject_team_application_teacher/$', reject_team_application_teacher),
    url(r'^add_homework_teacher/$', add_homework_teacher),
    url(r'^delete_homework_teacher/$', delete_homework_teacher),
    url(r'^get_homework_list_teacher/$', get_homework_list_teacher),
    url(r'^get_homework_info_teacher/$', get_homework_info_teacher),
    url(r'^edit_homework_basic_info_teacher/$', edit_homework_basic_info_teacher),
    url(r'^edit_homework_content_teacher/$', edit_homework_content_teacher),
    url(r'^view_homework_attachment_teacher/$', view_homework_attachment_teacher),
    url(r'^upload_homework_attachment_teacher/$', upload_homework_attachment_teacher),
    url(r'^delete_homework_attachment_teacher/$', delete_homework_attachment_teacher),
    url(r'^get_team_homework_list_teacher/$', get_team_homework_list_teacher),
    url(r'^view_team_homework_info_teacher/$', view_team_homework_info_teacher),
    url(r'^score_team_homework_teacher/$', score_team_homework_teacher),
    url(r'^download_team_homework_zip_teacher/$', download_team_homework_zip_teacher),
    url(r'^upload_modified_homework_teacher/$', upload_modified_homework_teacher),
    url(r'^export_team_excel_teacher/$', export_team_excel_teacher),
    url(r'^export_homework_excel_teacher/$', export_homework_excel_teacher),
    url(r'^export_n_homework_excel_teacher/$', export_n_homework_excel_teacher),
    url(r'^export_score_excel_teacher/$', export_score_excel_teacher),
    ##### lwj start #####
    url(r'^setSemester/', setSemester),
    url(r'setCurrentSemester/', setCurrentSemester),
    url(r'getSemester/', getSemester),
    url(r'getAllSemester/', getAllSemester),
    url(r'^deleteSemester/', deleteSemester),

    url(r'^getCurrentSemesterWeeks/', getCurrentSemesterWeeks),
    url(r'^setCourse/', setCourse),
    url(r'getSemester/', getSemester),
    url(r'^getCourse/', getCourse),
    url(r'^getAllCourse/', getAllCourse),
    url(r'^deleteCourse/', deleteCourse),

    url(r'^setUser/', setUser),
    url(r'^getAllUser/', getAllUser),
    url(r'^getUser/', getUser),
    url(r'^getUserOfCourse/', getUserOfCourse),
    url(r'^deleteUserOfCourse/', deleteUserOfCourse),
    url(r'^deleteUser/', deleteUser),

    url(r'^importUser/', importUser),
    url(r'^importCourse/', importCourse),
    url(r'^importUserOfCourse/', importUserOfCourse),

    url(r'^searchUser/', searchUser),
    url(r'^addRelationship/', addRelationship),
    url(r'^getRelationship/', getRelationship),
    url(r'^deleteRelationship/', deleteRelationship),

    url(r'^sendMessage/', sendMessage),
    url(r'^getNewMessage/', getNewMessage),
    url(r'^getAllMessage/', getAllMessage),
    url(r'^read/', read),
    ##### lwj end #####
    url(r'^courseDetail/$', views_ghz.courseDetail),
    url(r'^stuAllCourse/$', views_ghz.stuAllCourse),
    url(r'^stuAllHomework/$', views_ghz.stuAllHomework),
    url(r'^homeworkDetail/$', views_ghz.homeworkDetail),
    url(r'^homeworkSubmit/$', views_ghz.homeworkSubmit),
    url(r'homeworkSubmitInit/$', views_ghz.homeworkSubmitInit),
    url(r'^allMyTeam/$', views_ghz.allMyTeam),
    url(r'^teamInfo/$', views_ghz.teamInfo),
    url(r'^teamApply/$', views_ghz.teamApply),
    url(r'^teamSubmit/$', views_ghz.teamSubmit),
    url(r'^teamCheck/$', views_ghz.teamCheck),
    url(r'^joinTeam/$', views_ghz.joinTeam),
    url(r'^showTeamInfo/$', views_ghz.showTeamInfo),
    url(r'^createTeam/$', views_ghz.createTeam),
    url(r'^courseTeam/$', views_ghz.courseTeam),
    url(r'^homeworkUpload/$', views_ghz.homeworkUpload),
    url(r'^homeworkZip/$', views_ghz.homeworkZip),
    url(r'^homeworkDelete/$', views_ghz.homeworkDelete),
    url(r'^gradeMate/$', views_ghz.gradeMate),
    url(r'^gradeMateAction/$', views_ghz.gradeMateAction),
    url(r'^getResources/$', views_ghz.getResources),
    
]
