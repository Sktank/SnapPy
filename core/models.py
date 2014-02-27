from django.db import models

loremIpsum = "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium,\
 totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt\
  explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur\
   magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor\
    sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam\
     aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit\
      laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate\
       velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla\
        pariatur? \n \n Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque\
         laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae\
          dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia\
           consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem\
            ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt\
             ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum\
              exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur?\
               Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur,\
                vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?"

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
    description = models.TextField(blank=True, null=True)
    difficulty = models.IntegerField(blank=True, null=True)
    guide = models.TextField(default=loremIpsum)
    user = models.ForeignKey(WebUser, default=None, blank=True, null=True)  # student not in class that lesson is apart of
    courses = models.ManyToManyField(Course, related_name="courses", default=None, blank=True, null=True)

class Snap(models.Model):
    name = models.CharField(max_length=50)
    serial = models.TextField()
    isCompleted = models.BooleanField()
    isStarted = models.BooleanField()
    lesson = models.ForeignKey(Lesson, default=-1, blank=True, null=True) # part of what lesson
    user = models.ForeignKey(WebUser, default=None, blank=True, null=True)


