from django.conf.urls import patterns, url
from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
from rest_framework import routers
from core import views

user_re = '[\w\.-]+'
SnapViewsPath = 'static/js/snap/'

#routes to be used by Django Rest API
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

    # Dashboard
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^logout', views.user_logout, name='logout'),
    url(r'^register_course', views.register_course, name="register_course"),
    url(r'^enroll_courses', views.enroll_courses, name="enroll_courses"),

    url(r'^get_courses_by_name', views.get_courses_by_name, name="get_courses_by_name"),
    url(r'^get_courses_by_teacher', views.get_courses_by_teacher, name="get_courses_by_teacher"),

    url(r'^get_lessons', views.get_lessons, name="get_lessons"),
    url(r'^lesson_get_course_and_students', views.lesson_get_course_and_students, name="lesson_get_course_and_students"),
    url(r'^lesson_get_snaps', views.lesson_get_snaps, name="lesson_get_snaps"),
    url(r'^create_lesson', views.create_lesson, name="create_lesson"),
    url(r'^manage_course_lessons', views.manage_course_lessons, name="manage_course_lessons"),
    url(r'^save_snap', views.save_snap, name="save_snap"),

    # Snap Specific
    url(r'^snap$', views.base, name='base'),
    url(r'^vis$', views.visualizer, name='visualizer'),
    url(r'^web_exec_py2.py$', views.web_exec_py2, name='web_exec_py2.py'),

    # Branch for Django Rest API
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Needed to dynamically serve Snap Javascript files upon load with jquery loadscript
    url(r'^' + SnapViewsPath + 'blocks.js', views.static_blocks, name='static_blocks'),
    url(r'^' + SnapViewsPath + 'byob.js', views.static_byob, name='static_byob'),
    url(r'^' + SnapViewsPath + 'cloud.js', views.static_cloud, name='static_cloud'),
    url(r'^' + SnapViewsPath + 'executeVisualizer.js', views.static_executeVisualizer, name='static_executeVisualizer'),
    url(r'^' + SnapViewsPath + 'gui.js', views.static_gui, name='static_gui'),
    url(r'^' + SnapViewsPath + 'lists.js', views.static_lists, name='static_lists'),
    url(r'^' + SnapViewsPath + 'locale.js', views.static_locale, name='static_locale'),
    url(r'^' + SnapViewsPath + 'morphic.js', views.static_morphic, name='static_morphic'),
    url(r'^' + SnapViewsPath + 'objects.js', views.static_objects, name='static_objects'),
    url(r'^' + SnapViewsPath + 'paint.js', views.static_paint, name='static_paint'),
    url(r'^' + SnapViewsPath + 'sha512.js', views.static_sha512, name='static_sha512'),
    url(r'^' + SnapViewsPath + 'store.js', views.static_store, name='static_store'),
    url(r'^' + SnapViewsPath + 'threads.js', views.static_threads, name='static_threads'),
    url(r'^' + SnapViewsPath + 'widgets.js', views.static_widgets, name='static_widgets'),
    url(r'^' + SnapViewsPath + 'xml.js', views.static_xml, name='static_xml'),
    url(r'^' + SnapViewsPath + 'codemirror1.js', views.static_codemirror1, name='static_codemirror1'),
    url(r'^' + SnapViewsPath + 'codemirror2.js', views.static_codemirror2, name='static_codemirror2'),
)