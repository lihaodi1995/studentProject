from django.conf.urls import url

from . import views

app_name = 'teachers'

urlpatterns = [
	url(r'^$', views.course_index, name='index'),
	url(r'^index/', views.course_index, name='course_index'),
	url(r'^course_session/(.+)/', views.course_session, name='course_index'),
	url(r'^manage_resources/', views.manage_resources, name='manage_resources'),
	url(r'^check_assignment/', views.check_assignment, name='check_assignment'),
	url(r'^edit_homework/', views.edit_homework, name='edit_homework'),
	url(r'^approve_team/', views.approve_team, name='approve_team'),
	url(r'^fine_tune_team/', views.fine_tune_team, name='fine_tune_team'),
	url(r'^watch_team/', views.watch_team, name='watch_team'),
	url(r'^return_index/', views.return_index, name='return_index'),
	url(r'^course_index/', views.course_index, name='course_index'),
	url(r'^course_info/', views.course_info, name='course_info'),
	url(r'^add_one_assignment/', views.add_one_assignment, name='add_one_assignment'),
	url(r'^show_team_assignment/(.+)/', views.show_team_assignment, name='show_team_assignment'),
	url(r'^upload_resource/', views.upload_resource, name='upload_resource'),
	url(r'^check_online/(\d+)', views.check_online, name='check_online'),
	url(r'^download_resource/(\d+)', views.download_resource, name='download_resource'),
	url(r'^delete_resource/', views.delete_resource, name='delete_resource'),
	url(r'^add_tag/', views.add_tag, name='add_tag'),
	url(r'^assignment_form/(\d*)', views.assignment_form, name='assignment_form'),
	url(r'^modify_course/', views.modify_course, name='modify_course'),
	url(r'^teacher_info/', views.teacher_info, name='teacher_info'),
	url(r'^setPassword/', views.setPassword, name='setPassword'),
	url(r'^get_all_no_select_stu/', views.get_all_no_select_stu, name='get_all_no_select_stu'),
	url(r'^agree_team/', views.agree_team, name='agree_team'),

	url(r'^test/', views.check_assignment, name='test'),

	# url(r'^ass_list/', views.ass_list, name='ass_list'),
	url(r'^manage_team/', views.manage_team, name='manage_team'),
	url(r'^add_assignment/', views.add_assignment, name='add_assignment'),
	url(r'^upload_grades/', views.upload_grades, name='upload_grades'),
	url(r'^set_assignment_rate/', views.set_assignment_rate, name='set_assignment_rate'),
	url(r'^add_grade_item/', views.add_grade_item, name='add_grade_item'),

	url(r'^manage_grade/', views.manage_grade, name='manage_grade'),
	url(r'^modify_grade_item/', views.modify_grade_item, name='modify_grade_item'),
	url(r'^remove_grade_item/(\d+)/', views.remove_grade_item, name='remove_grade_item'),
	url(r'^show_edit_assignment/(\d+)/', views.show_edit_assignment, name='show_edit_assignment'),
	url(r'^edit_assignment/(\d+)/', views.edit_assignment, name='edit_assignment'),
	url(r'^select_via_tags/', views.select_via_tags, name='select_via_tags'),
	url(r'^input_item_score/(.+)', views.input_item_score, name='input_item_score'),
	url(r'^add_revise_record/(\d+)/', views.add_revise_record, name='add_revise_record'),
	url(r'^download_file_test/(?P<param>\d+)$', views.download_file_test, name='download_file_test'),
	url(r'^get_team_info/', views.get_team_info, name='get_team_info'),
	url(r'^upload_grade_item/(.+)', views.upload_grade_item, name='upload_grade_item'),
	url(r'^download_grade_excel/(\d)/$', views.download_grade_excel, name='download_grade_excel'),
	url(r'^set_grades/(\d)/(\d+)/$', views.set_grades, name='set_grades'),
	url(r'^export_assignment_report/(\d+)/$', views.export_assignment_report, name='export_assignment_report'),

	url(r'submit_team/', views.submit_team, name='submit_team'),
	url(r'export_excel_total_grade/', views.export_excel_total_grade, name='export_excel_total_grade'),
]
