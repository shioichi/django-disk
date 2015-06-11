from django.conf.urls import patterns, url
from online import views


urlpatterns = patterns('',
    url(r'^$', views.login, name='login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^regist/$', views.regist, name='regist'),
    url(r'^index/$', views.index, name='index'),
    url(r'^index/(\S+)', views.index, name='index_files'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^xiugai/$', views.sendmail, name='send'),
    url(r'^validate/$', views.validate, name='validate'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^folder_new/$', views.create_fr, name='folder_new'),
    url(r'^folder_info/$', views.folder_info, name='folder_info'),
    url(r'^html/$', views.html_test, name='testhtml'),
    url(r'user_info/$', views.user_info, name='user_info'),
)