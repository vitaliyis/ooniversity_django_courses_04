from django.conf.urls import patterns, include, url
from courses import views

urlpatterns = patterns('',
	#url(r'^(?P<id>\d+)/$', views.course_detail, name='detail'),
	url(r'^(\d+)/$', views.course_detail, name='detail'),
)
