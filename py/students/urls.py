from django.conf.urls import url

from . import views

app_name = 'students'

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^set_group/', views.set_group, name='set_group'),
    url(r'^add_group/', views.add_group, name='add_group'),
    url(r'^my_group/', views.my_group, name='my_group'),
    url(r'^apply_group/', views.apply_group, name='apply_group'),
    url(r'^pass_apply/', views.pass_apply, name='pass_apply'),
    url(r'^add_member/', views.add_member, name='add_member'),
    url(r'^apply_to_teacher/', views.apply_to_teacher, name='apply_to_teacher'),
    url(r'^delete_apply/', views.delete_apply, name='delete_apply'),
    url(r'^refuse_apply/', views.refuse_apply, name='refuse_apply'),
    url(r'^delete_member/', views.delete_member, name='delete_member'),
    url(r'^disband_group/', views.disband_group, name='disband_group'),
    url(r'submit_ass/', views.submit_ass, name='submit_ass'),
    url(r'courseResource$', views.courseResource),
    url(r'courseInfo/(?P<course_id>\d+)$', views.courseInfo),
    url(r'student_info/', views.student_info, name='student_info'),
    url(r'download/(?P<file_id>\w+)', views.download),
    url(r'get_homework/(?P<course_id>\d+)$', views.get_homework, name='get_homework'),
    url(r'ass_detail/(?P<param1>\d+)$', views.ass_detail, name='ass_detail'),
    url(r'group_affair/', views.group_affair, name='group_affair'),
    url(r'set_weight/', views.set_weight, name='set_weight'),
    url(r'update_role/', views.update_role, name='update_role'),
    url(r'setPassword/', views.setPassword, name='setPassword'),
    url(r'select_via_tags/', views.select_via_tags, name='select_via_tags'),
    url(r'download_file_test/(\d+)', views.download_file_test, name='download_file_test'),    
]
