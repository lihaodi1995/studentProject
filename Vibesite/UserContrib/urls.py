
from django.urls import path

from . import views

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # 表单界面
    path(r'form/<int:conf_id>', views.form, name='form'),
    path(r'form/<int:conf_id>/<int:contrib_id>', views.form, name='form'),
    # 提交表单
    #path(r'submit/<int:user_id>/<int:conf_id>', views.submit, name='submit'),
    path(r'submit/<int:conf_id>', views.submit, name='submit'),#第一次提交
    path(r'submit/<int:conf_id>/<int:contrib_id>', views.submit, name='submit'),#修改
    # 下载
    path(r'download/<int:contrib_id>', views.download, name='download'),
    path(r'download2/<int:contrib_id>', views.download2, name='download2'),
    path(r'zipdownload/<int:conf_id>', views.zipdownload, name='zipdownload'),

    #上传消费凭证
    path(r'register_into_conference/<int:conf_id>/<int:contrib_id>',views.register_into_conference,name='register_into_conference'),

    # 会议详细信息
    path('contriblist/<int:conf_id>/',views.contriblist,name='contriblist'),

    path('listen/<int:conf_id>/',views.listen,name='listen'),
    path('paper_register/<int:conf_id>/<int:contrib_id>',views.paper_register,name='paper_register'),


    # path('<int:contribution_id>/', views.detail, name='contribution_id'),
    #path('<int:contribution_id>/', views.detail, name='contribution_id'),
    path('<int:conf_id>/<int:contrib_id>/contrib_detail', views.contrib_detail, name='contrib_detail'),

    path('<int:contrib_id>/info/', views.contribInfo),

    # 收藏会议
    path('subscribe/<int:conf_id>',views.subscribe,name='subscribe'),
    # 查询是否收藏
    path('ifsubscribe/<int:conf_id>',views.if_subscribe,name="ifsubscribe"),
    path('ifexpire/<int:conf_id>',views.ifexpire,name='ifexpire'),

    # 下载论文模板
    path(r'templatedownload/<int:conf_id>',views.template_download,name='templatedownload'),

    #错误处理
    path(r'error',views.error,name='templatedownload'),
]
