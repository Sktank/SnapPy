from django.conf.urls import patterns, url

from django.conf.urls.defaults import *

from django.contrib.auth import views as auth_views
from rest_framework import routers

from core import views

user_re = '[\w\.-]+'

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'webusers', views.WebUserViewSet, base_name='webuser')
router.register(r'studentcourses', views.StudentCourseViewSet, base_name='studentcourse')
router.register(r'teachercourses', views.TeacherCourseViewSet, base_name='teachercourse')
router.register(r'courses', views.CourseViewSet, base_name='course')

router.register(r'lessons', views.LessonViewSet, base_name='lesson')
router.register(r'courselessons', views.CourseLessonViewSet, base_name='courselesson')
router.register(r'snaps', views.SnapViewSet, base_name='snap')


urlpatterns = patterns('',
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^snap$', views.base, name='base'),
    url(r'^logout', views.user_logout, name='logout'),
    url(r'^vis$', views.visualizer, name='visualizer'),
    url(r'^register_course', views.register_course, name="register_course"),
    url(r'^enroll_courses', views.enroll_courses, name="enroll_courses"),
    url(r'^get_lessons', views.get_lessons, name="get_lessons"),
    url(r'^lesson_get_course_and_students', views.lesson_get_course_and_students, name="lesson_get_course_and_students"),
    url(r'^lesson_get_snaps', views.lesson_get_snaps, name="lesson_get_snaps"),


    url(r'^web_exec_py2.py$', views.web_exec_py2, name='web_exec_py2.py'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),


    url(r'^static/js/blocks.js', views.static_blocks, name='static_blocks'),
    url(r'^static/js/byob.js', views.static_byob, name='static_byob'),
    url(r'^static/js/cloud.js', views.static_cloud, name='static_cloud'),
    url(r'^static/js/executeVisualizer.js', views.static_executeVisualizer, name='static_executeVisualizer'),
    url(r'^static/js/gui.js', views.static_gui, name='static_gui'),
    url(r'^static/js/lists.js', views.static_lists, name='static_lists'),
    url(r'^static/js/locale.js', views.static_locale, name='static_locale'),
    url(r'^static/js/morphic.js', views.static_morphic, name='static_morphic'),
    url(r'^static/js/objects.js', views.static_objects, name='static_objects'),
    url(r'^static/js/paint.js', views.static_paint, name='static_paint'),
    url(r'^static/js/sha512.js', views.static_sha512, name='static_sha512'),
    url(r'^static/js/store.js', views.static_store, name='static_store'),
    url(r'^static/js/threads.js', views.static_threads, name='static_threads'),
    url(r'^static/js/widgets.js', views.static_widgets, name='static_widgets'),
    url(r'^static/js/xml.js', views.static_xml, name='static_xml'),
    url(r'^static/js/codemirror1.js', views.static_codemirror1, name='static_codemirror1'),
    url(r'^static/js/codemirror2.js', views.static_codemirror2, name='static_codemirror2'),
)