from django.conf.urls import patterns, url

from django.conf.urls.defaults import *

from django.contrib.auth import views as auth_views
from rest_framework import routers

from core import views

user_re = '[\w\.-]+'

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'students', views.StudentViewSet)
router.register(r'teachers', views.TeacherViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'lessons', views.LessonViewSet)
router.register(r'snaps', views.SnapViewSet)


urlpatterns = patterns('',
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^snap$', views.base, name='base'),
    url(r'^logout', views.user_logout, name='logout'),
    url(r'^vis$', views.visualizer, name='visualizer'),
    url(r'^web_exec_py2.py$', views.web_exec_py2, name='web_exec_py2.py'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)