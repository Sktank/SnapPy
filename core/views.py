from StdSuites.AppleScript_Suite import record
from django.contrib.auth import logout
import json
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
import socket, os
from subprocess import Popen, PIPE
import subprocess
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from core.serializers import UserSerializer, GroupSerializer, CourseSerializer, LessonSerializer, SnapSerializer, WebUserSerializer, CourseLessonSerializer
from core.models import Course, Lesson, Snap, WebUser
from itertools import chain

#===========================================================================================
#                                      Snap Specific
#===========================================================================================

def base(request, template="core/base.html"):
    return render_to_response(template)

def visualizer(request, template="core/visualizer.html"):
    return render_to_response(template)

def web_exec_py2(request):
    print str(dict(request.GET.iterlists()))
    proc = subprocess.Popen(["python", "core/static/vis/v3/web_exec_py2.py", str(dict(request.GET.iterlists()))], stdout=PIPE)
    ret = proc.stdout.read()
    return HttpResponse(ret, content_type="text/plain")

def execute(command, the_stdin):
    proc = Popen(command.split(" "), stdin=PIPE, stdout=PIPE, stderr=PIPE)
    result = proc.communicate(input = the_stdin)
    return record(stdout = result[0].decode("UTF-8"),
        stderr = result[1].decode("UTF-8"),
        returncode = proc.returncode)


#===========================================================================================
#                                         Dashboard
#===========================================================================================


@login_required()
def dashboard(request, template="core/dashboard.html"):
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
#                                 Creating and Updating models
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


@login_required()
def get_lessons(request):
    if request.is_ajax():
        current_user = WebUser.objects.filter(userId = request.user.id)[0]
        course_id = request.GET.get('course_id', False)
        course = Course.objects.filter(id = course_id)[0]

        #security check
        if current_user not in course.teachers.all() and current_user not in course.students.all():
            return HttpResponse('error')

        #get lessons currently part of class
        lessons = Lesson.objects.filter(courses__id=course_id)
        lessonSet = set()
        for lesson in lessons:
            lessonSet.add(lesson.id)

        #get lessons not part of class
        allLessons = Lesson.objects.filter(user=current_user)
        allLessons = allLessons.exclude(id__in = lessonSet)

        currentLessonData = serializers.serialize("json", lessons)
        separateLessonDate = serializers.serialize("json", allLessons)
        return HttpResponse('[' + currentLessonData + ',' + separateLessonDate + ']')

@login_required()
def lesson_get_course_and_students(request):
    if request.is_ajax():
        course_id = request.GET.get('course_id', False)

        course_set = Course.objects.filter(id=course_id)
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
        student_id = request.GET.get('student_id', False)
        lesson_id = request.GET.get('lesson_id', False)
        print lesson_id
        lesson = Lesson.objects.filter(id=int(lesson_id))[0]
        print lesson

        if student_id:
            current_user = WebUser.objects.filter(userId = student_id)[0]
        else:
            current_user = WebUser.objects.filter(userId = request.user.id)[0]

        #get all the snaps with these fields
        snaps = Snap.objects.filter(lesson=lesson, user=current_user)

        if not snaps:
            snap_serial = 0
        else:
            snap_serial = serializers.serialize("json", snaps)

        return HttpResponse(snap_serial)


lesson_no_name_message = "Lesson name is required"
lesson_name_too_short_message = "Lesson name must be at least 5 characters"

lesson_no_guide_message = "Lesson guide is required"
lesson_guide_too_short_message = "Lesson guide must be at least 10 characters"
@login_required()
def create_lesson(request):
    if request.is_ajax():
        name = request.POST.get('name', False)
        description = request.POST.get('description', False)
        difficulty = request.POST.get('difficulty', False)
        guide = request.POST.get('guide', False)
        current_user = WebUser.objects.filter(userId = request.user.id)[0]

        errors = {}

        if not name:
            errors['name'] = lesson_no_name_message
        elif len(name.strip()) < 5:
            errors['name'] = lesson_name_too_short_message
        else:
            lessons = Course.objects.filter(name=name)
            if len(lessons) > 0:
                errors['name'] = name_taken_message

        if not guide:
            errors['guide'] = lesson_no_guide_message
        elif len(guide.strip()) < 10:
            errors['guide'] = lesson_guide_too_short_message

        if not errors:
            lesson = Lesson()
            lesson.name = name.strip()
            if description:
                lesson.description = description.strip()
            if difficulty:
                lesson.difficulty = int(difficulty)
            lesson.guide = guide.strip()
            lesson.user = current_user
            lesson.save()

        return HttpResponse(json.dumps(errors))

@login_required()
def manage_course_lessons(request):
    if request.is_ajax():
        course_id = request.POST.get('course_id', False)
        add_ids = request.POST.getlist('add_ids[]', False)
        remove_ids = request.POST.getlist('remove_ids[]', False)

        if course_id:
            course = Course.objects.filter(id = course_id)[0]

            if add_ids:
                for id in add_ids:
                    lesson = Lesson.objects.filter(id=id)[0]
                    lesson.courses.add(course)
                    lesson.save()

            if remove_ids:
                for id in remove_ids:
                    lesson = Lesson.objects.filter(id=id)[0]
                    lesson.courses.remove(course)
                    lesson.save()

        return HttpResponse(0)


@login_required()
def save_snap(request):
    if request.is_ajax():
        name = request.POST.get('name', False)
        lesson_id = request.POST.get('lesson_id', False)
        serial = request.POST.get('serial', False)

        lesson = Lesson.objects.filter(id=int(lesson_id))[0]
        current_user = WebUser.objects.filter(userId = request.user.id)[0]

        #get all the snaps with these fields
        snap = Snap.objects.filter(lesson=lesson, user=current_user, name=name)

        if not snap:
            response = createNewSnap(name, serial, lesson, current_user)
        elif len(snap) == 1:
            response = updateSnap(snap[0], name, serial)
        else:
            response = "shit there are duplicate snaps"

        return HttpResponse(response)


def createNewSnap(name, serial, lesson, current_user):
    snap = Snap()
    snap.name = name
    snap.serial = serial
    snap.lesson = lesson
    snap.user = current_user
    snap.save()
    return 0

def updateSnap(snap, name, serial):
    snap.serial = serial
    snap.save()
    return 0
#===========================================================================================
#                                      API serialization views
#===========================================================================================

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class WebUserViewSet(viewsets.ModelViewSet):
    serializer_class = WebUserSerializer

    def get_queryset(self):
        user = self.request.user
        return WebUser.objects.filter(userId=user.id)



class TeacherCourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(teachers__userId = user.id)

class StudentCourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(students__userId = user.id)

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    def get_queryset(self):
        return Course.objects.all()


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user1 = self.request.user
        webUser = WebUser.objects.filter(userId=user1.id)
        lessons = Lesson.objects.filter(user=webUser)
        return lessons

#This is now for students
class CourseLessonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
#    queryset = Lesson.objects.all()
    serializer_class = CourseLessonSerializer

    def get_queryset(self):
        user1 = self.request.user

        #find all your courses
        student_courses = Course.objects.filter(students__userId = user1.id)
        teacher_courses = Course.objects.filter(teachers__userId = user1.id)

        all_courses = list(chain(student_courses, teacher_courses))

        wantedLessons = set()

        allLessons = Lesson.objects.all()

        for course in all_courses:
            for lesson in allLessons:
                wanted_courses = lesson.courses.filter(id = course.id)
                if wanted_courses:
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

pathToCore = '/Users/spencertank/School/Thesis/imcode/core/'
coreToJs = 'static/js/'
snapDir = 'snap/'
codemirror1 = 'static/codemirror/lib/'
codemirror2 = 'static/codemirror/mode/python/'
snapPath = pathToCore + coreToJs + snapDir

def HttpResponseForFile(path, filename):
    abspath = open(path + filename,'r')
    response = HttpResponse(content=abspath.read())
    return response

def static_blocks(request):
    return HttpResponseForFile(snapPath, 'blocks.js')

def static_byob(request):
    return HttpResponseForFile(snapPath, 'byob.js')

def static_cloud(request):
    return HttpResponseForFile(snapPath, 'cloud.js')

def static_executeVisualizer(request):
    return HttpResponseForFile(snapPath, 'executeVisualizer.js')

def static_gui(request):
    return HttpResponseForFile(snapPath, 'gui.js')

def static_lists(request):
    return HttpResponseForFile(snapPath, 'lists.js')

def static_locale(request):
    return HttpResponseForFile(snapPath, 'locale.js')

def static_morphic(request):
    return HttpResponseForFile(snapPath, 'morphic.js')

def static_objects(request):
    return HttpResponseForFile(snapPath, 'objects.js')

def static_paint(request):
    return HttpResponseForFile(snapPath, 'paint.js')

def static_sha512(request):
    return HttpResponseForFile(snapPath, 'sha512.js')

def static_store(request):
    return HttpResponseForFile(snapPath, 'store.js')

def static_threads(request):
    return HttpResponseForFile(snapPath, 'threads.js')

def static_widgets(request):
    return HttpResponseForFile(snapPath, 'widgets.js')

def static_xml(request):
    return HttpResponseForFile(snapPath, 'xml.js')

def static_codemirror1(request):
    return HttpResponseForFile(pathToCore + codemirror1, 'codemirror.js')

def static_codemirror2(request):
    return HttpResponseForFile(pathToCore + codemirror2, 'python.js')





