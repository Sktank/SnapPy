from django.db import models

# Create your models here.

class Student(models.Model):
    user_id = models.IntegerField()
    grade = models.IntegerField()
    age = models.IntegerField()
    firstName = models.CharField(max_length=30)
    LastName = models.CharField(max_length=30)


class Teacher(models.Model):
    user_id = models.IntegerField()
    firstName = models.CharField(max_length=30)
    LastName = models.CharField(max_length=30)

class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    teachers = models.ForeignKey(Teacher)
    students = models.ForeignKey(Student)

class Lesson(models.Model):
    name = models.CharField(max_length=50)
    isCompleted = models.BooleanField()
    isStarted = models.BooleanField()
    description = models.TextField()
    difficulty = models.IntegerField()

    teacher = models.ForeignKey(Teacher, unique=True)  # class that lesson is apart of
    student = models.ForeignKey(Student, unique=True)  # student not in class that lesson is apart of

class Snap(models.Model):
    stuff = models.TextField()
    lesson = models.ForeignKey(Lesson, unique=True) # part of what lesson