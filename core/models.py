from django.db import models

# Create your models here.

class WebUser(models.Model):
    userId = models.IntegerField()
    firstName = models.CharField(max_length=30)
    LastName = models.CharField(max_length=30)
    username = models.CharField(max_length=100)

class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    teachers = models.ManyToManyField(WebUser, related_name="teachers")
    students = models.ManyToManyField(WebUser, related_name="students")

class Lesson(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    difficulty = models.IntegerField()
    user = models.ForeignKey(WebUser, default=None, blank=True, null=True)  # student not in class that lesson is apart of
    course = models.ForeignKey(Course, default=None, blank=True, null=True)

class Snap(models.Model):
    stuff = models.TextField()
    isCompleted = models.BooleanField()
    isStarted = models.BooleanField()
    lesson = models.ForeignKey(Lesson, default=-1, blank=True, null=True) # part of what lesson
    user = models.ForeignKey(WebUser, default=None, blank=True, null=True)

