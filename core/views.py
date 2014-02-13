
# Create your views here.
from StdSuites.AppleScript_Suite import record
from django.contrib.auth import logout
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
from core.serializers import UserSerializer, GroupSerializer, StudentSerializer, TeacherSerializer, CourseSerializer, LessonSerializer, SnapSerializer
from core.models import Student, Teacher, Course, Lesson, Snap



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
#    student = Student.objects.filter()

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

class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class LessonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class SnapViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Snap.objects.all()
    serializer_class = SnapSerializer


