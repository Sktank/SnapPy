__author__ = 'spencertank'

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from core.models import Student, Teacher, Course, Lesson, Snap


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ('url', 'id', 'grade', 'age', 'firstName', 'LastName', 'user_id')


class TeacherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Teacher
        fields = ('url', 'id', 'firstName', 'lastName')

class CourseSerializer(serializers.HyperlinkedModelSerializer):
    teachers = serializers.HyperlinkedRelatedField(many=True, read_only=True,view_name='teacher-detail')
    students = serializers.HyperlinkedRelatedField(many=True, read_only=True,view_name='student-detail')

    class Meta:
        model = Course
        fields = ('url', 'id', 'name', 'description', 'teachers', 'students')


class LessonSerializer(serializers.HyperlinkedModelSerializer):
    teacher = serializers.HyperlinkedRelatedField(many=True, read_only=True,view_name='teacher-detail')
    student = serializers.HyperlinkedRelatedField(many=True, read_only=True,view_name='student-detail')

    class Meta:
         model = Lesson
         fields = ('url', 'id', 'name', 'description', 'isStarted', 'isCompleted', 'difficulty', 'teacher', 'student')

class SnapSerializer(serializers.HyperlinkedModelSerializer):
    lesson = serializers.HyperlinkedRelatedField(many=True, read_only=True,view_name='lesson-detail')

    class Meta:
        model = Snap
        fields = ('url', 'id', 'stuff', 'lesson')


#class Student(models.Model):
#    grade = models.IntegerField()
#    age = models.IntegerField()
#    firstName = models.CharField(max_length=30)
#    LastName = models.CharField(max_length=30)
#
#class Teacher(models.Model):
#    firstName = models.CharField(max_length=30)
#    LastName = models.CharField(max_length=30)
#
#class Course(models.Model):
#    name = models.CharField(max_length=50)
#    description = models.TextField()
#    teacher = models.ForeignKey(Teacher)
#    student = models.ForeignKey(Student)
#
#class Lesson(models.Model):
#    name = models.CharField(max_length=50)
#    isCompleted = models.BooleanField()
#    isStarted = models.BooleanField()
#    description = models.TextField()
#    difficulty = models.IntegerField()
#
#    course = models.ForeignKey(Course)  # class that lesson is apart of
#    student = models.ForeignKey(Student)  # student not in class that lesson is apart of
#
#
#
#class Snap(models.Model):
#    stuff = models.TextField
