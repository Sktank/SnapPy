__author__ = 'spencertank'

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from core.models import Course, Lesson, Snap, WebUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class WebUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WebUser
        fields = ('url', 'id', 'firstName', 'LastName', 'userId', 'username')


class CourseSerializer(serializers.ModelSerializer):
    teachers = serializers.PrimaryKeyRelatedField(many=True)
    students = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = Course

class LessonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
         model = Lesson
         fields = ('url', 'id', 'name', 'description', 'difficulty', 'user')

class CourseLessonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
         model = Lesson
         fields = ('url', 'id', 'name', 'description', 'difficulty', 'course')

class SnapSerializer(serializers.HyperlinkedModelSerializer):
    lesson = serializers.HyperlinkedRelatedField(many=True, read_only=True,view_name='lesson-detail')

    class Meta:
        model = Snap
        fields = ('url', 'id', 'isStarted', 'isCompleted', 'stuff', 'lesson')

