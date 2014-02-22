
# Create your views here.
from StdSuites.AppleScript_Suite import record
from django.contrib.auth import logout
import json
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
#from core.static.vis.v3.web_exec_py2 import web_exec
import socket, os
from subprocess import Popen, PIPE
#from Websheet import record
import subprocess
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from core.serializers import UserSerializer, GroupSerializer, CourseSerializer, LessonSerializer, SnapSerializer, WebUserSerializer, CourseLessonSerializer
from core.models import Course, Lesson, Snap, WebUser

path_to_core = '/Users/spencertank/School/Thesis/imcode/core/'


def base(request, template="core/base.html"):
    return render_to_response(template)

def visualizer(request, template="core/visualizer.html"):
    return render_to_response(template)

def web_exec_py2(request):
    print str(dict(request.GET.iterlists()))
    proc = subprocess.Popen(["python", "core/static/vis/v3/web_exec_py2.py", str(dict(request.GET.iterlists()))], stdout=PIPE)
    ret = proc.stdout.read()
#    response = execute('web_exec', request)
    return HttpResponse(ret, content_type="text/plain")


def execute(command, the_stdin):
    proc = Popen(command.split(" "), stdin=PIPE, stdout=PIPE, stderr=PIPE)
    result = proc.communicate(input = the_stdin)
    return record(stdout = result[0].decode("UTF-8"),
        stderr = result[1].decode("UTF-8"),
        returncode = proc.returncode)


#===========================================================================================
#                                      Dashboard
#===========================================================================================


@login_required()
def dashboard(request, template="core/dashboard.html"):

    id = request.user.id

    values = {
        'username': request.user.username,
        'id': request.user.id
    }
    c = RequestContext(request, values)
    return render_to_response(template, c)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

#===========================================================================================
#                                      Creating and Updating models
#===========================================================================================

def response(code, message):
    return {
        "code":code,
        "message":message
    }

def createCourseLessons(course):
    names = ['Lesson 1', 'Lesson 2']
    descriptions = ['Movement', 'Variables']
    difficulties = [1,1]
    num = len(names)

    for i in range(0, num):
        lesson = Lesson()
        lesson.name = names[i]
        lesson.description = descriptions[i]
        lesson.difficulty = difficulties[i]
        lesson.course = course
        lesson.save()

short_name_message = "That name is too short! Name must be at least 5 character!"
name_taken_message = "That name is already taken. Please choose another!"
success_message = "Course Created!"
@login_required()
def register_course(request):
#    import pdb
#    pdb.set_trace()
    if request.method == "POST" and request.is_ajax():
        name = request.POST.get('name', False)

        if len(name) < 5:
            return HttpResponse(short_name_message)
        #check database for any courses with this name
        courses = Course.objects.filter(name=name)
        if len(courses) > 0:
            return HttpResponse(name_taken_message)
        else:
            course = Course()
            course.name = name
            current_user = WebUser.objects.filter(userId = request.user.id)[0]
            course.save()
            course.teachers.add(current_user)
            #add lessons
            course.save()
            createCourseLessons(course)
            return HttpResponse(success_message)


empty_message = "Your Course Queue is Currently Empty."
success_message = "Enrollment Successful!"
duplicate_message = "You are already enrolled in one of these classes. Please try again."
@login_required()
def enroll_courses(request):
    if request.method == "POST" and request.is_ajax():
        ids = request.POST.getlist('ids[]', False)

        if ids is False or len(ids) == 0:
            return HttpResponse(json.dumps(response(-1, empty_message)))

        current_user = WebUser.objects.filter(userId = request.user.id)[0]
        for id in ids:
            course = Course.objects.filter(id=id)[0]
            course.students.add(current_user)
            course.save()
        resp = response(0, success_message)
        print resp
        return HttpResponse(json.dumps(response(0, success_message)))


#this is unsafe
@login_required()
def get_lessons(request):
    if request.is_ajax():
        current_user = WebUser.objects.filter(userId = request.user.id)[0]
        course_id = request.POST.get('course_id', False)
        course = Course.objects.filter(id = course_id)[0]

        #security check
        if current_user not in course.teachers.all() and current_user not in course.students.all():
            return HttpResponse('error')

        lessons = Lesson.objects.filter(course=course)
        data = serializers.serialize("json", lessons)
        return HttpResponse(data)

@login_required()
def lesson_get_course_and_students(request):
    if request.is_ajax():
#        import pdb
#        pdb.set_trace()
        lesson_id = request.POST.get('lesson_id', False)
        lesson = Lesson.objects.filter(id=lesson_id)[0]
        course_set = Course.objects.filter(id=lesson.course.id)
        course =course_set[0]
        students = serializers.serialize("json", course.students.all())
        course_serial = serializers.serialize("json", course_set)

        #security check
        current_user = WebUser.objects.filter(userId = request.user.id)[0]
        if current_user not in course.teachers.all():
            return HttpResponse('error')

        return HttpResponse('[' + course_serial + ',' + students + ']')

@login_required()
def lesson_get_snaps(request):
    if request.is_ajax():
        lesson_id = request.POST.get('lesson_id', False)
        lesson = Lesson.objects.filter(id=lesson_id)[0]
        current_user = WebUser.objects.filter(userId = request.user.id)[0]

        #get all the snaps with these fields
        snaps = Snap.objects.filter(lesson=lesson, user=current_user)
        snap_serial = serializers.serialize("json", snaps)

        return HttpResponse(snap_serial)


    #===========================================================================================
#                                      API serialization views
#===========================================================================================

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class WebUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    serializer_class = WebUserSerializer

    def get_queryset(self):
        user = self.request.user
        return WebUser.objects.filter(userId=user.id)



class TeacherCourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    serializer_class = CourseSerializer
    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(teachers__userId = user.id)

class StudentCourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    serializer_class = CourseSerializer
    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(students__userId = user.id)

class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    serializer_class = CourseSerializer
    def get_queryset(self):
        return Course.objects.all()


class LessonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
#    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_queryset(self):
#        import pdb
#        pdb.set_trace()
        user1 = self.request.user
        webUser = WebUser.objects.filter(userId=user1.id)
        lessons = Lesson.objects.filter(user=webUser)
        return lessons

class CourseLessonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
#    queryset = Lesson.objects.all()
    serializer_class = CourseLessonSerializer

    def get_queryset(self):
        user1 = self.request.user
        #find all your courses
        courses = Course.objects.filter(teachers__userId = user1.id)
        wantedLessons = set()
        for lesson in Lesson.objects.all():
            if lesson.course in courses:
                wantedLessons.add(lesson.id)

        return Lesson.objects.filter(id__in = wantedLessons)

class SnapViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Snap.objects.all()
    serializer_class = SnapSerializer

#===========================================================================================
#                               Static Snap Javascript Views
#===========================================================================================

def static_blocks(request):
    abspath = open(path_to_core + 'static/js/blocks.js','r')
    response = HttpResponse(content=abspath.read())
    return response

def static_byob(request):
    abspath = open(path_to_core + 'static/js/byob.js','r')
    response = HttpResponse(content=abspath.read())
    return response

def static_cloud(request):
    abspath = open(path_to_core + 'static/js/cloud.js','r')
    response = HttpResponse(content=abspath.read())
    return response

def static_executeVisualizer(request):
    abspath = open(path_to_core + 'static/js/executeVisualizer.js','r')
    response = HttpResponse(content=abspath.read())
    return response

def static_gui(request):
    abspath = open(path_to_core + 'static/js/gui.js','r')
    response = HttpResponse(content=abspath.read())
    return response

def static_lists(request):
    abspath = open(path_to_core + 'static/js/lists.js','r')
    response = HttpResponse(content=abspath.read())
    return response

def static_locale(request):
    abspath = open(path_to_core + 'static/js/locale.js','r')
    response = HttpResponse(content=abspath.read())
    return response

def static_morphic(request):
    abspath = open(path_to_core + 'static/js/morphic.js','r')
    response = HttpResponse(content=abspath.read())
    return response

def static_objects(request):
    abspath = open(path_to_core + 'static/js/objects.js','r')
    response = HttpResponse(content=abspath.read())
    return response

def static_paint(request):
    abspath = open(path_to_core + 'static/js/paint.js','r')
    response = HttpResponse(content=abspath.read())
    return response

def static_sha512(request):
    abspath = open(path_to_core + 'static/js/sha512.js','r')
    response = HttpResponse(content=abspath.read())
    return response

def static_store(request):
    abspath = open(path_to_core + 'static/js/store.js','r')
    response = HttpResponse(content=abspath.read())
    return response

def static_threads(request):
    abspath = open(path_to_core + 'static/js/threads.js','r')
    response = HttpResponse(content=abspath.read())
    return response

def static_widgets(request):
    abspath = open(path_to_core + 'static/js/widgets.js','r')
    response = HttpResponse(content=abspath.read())
    return response

def static_xml(request):
    abspath = open(path_to_core + 'static/js/xml.js','r')
    response = HttpResponse(content=abspath.read())
    return response

def static_codemirror1(request):
    abspath = open(path_to_core + 'static/codemirror/lib/codemirror.js','r')
    response = HttpResponse(content=abspath.read())
    return response

def static_codemirror2(request):
    abspath = open(path_to_core + 'static/codemirror/mode/python/python.js','r')
    response = HttpResponse(content=abspath.read())
    return response





