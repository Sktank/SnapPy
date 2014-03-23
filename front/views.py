# Create your views here.

# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from core.models import WebUser, Lesson
from front.forms import RegistrationForm, LoginForm
from django.contrib.auth.models import User


def front_index(request, template="front/index.html"):
    values = {
        'index': True,
    }
    c = RequestContext(request, values)
    return render_to_response(template, c)

def front_about(request, template="front/about.html"):
    values = {
        'about': True,
    }
    c = RequestContext(request, values)
    return render_to_response(template, c)

def front_register(request, template="front/register.html"):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(username, email, password)
            new_user = authenticate(username=username, password=password)

            # create a web user
            webUser = WebUser()
            webUser.userId = user.id
            webUser.username = user.username
            webUser.save()

            # create a bunch of lessons for web user
            createLessons(webUser)

            login(request, new_user)

            #send a confirmation message
            messages.success(request, "Account Created!")
            return HttpResponseRedirect(reverse("dashboard"))



    else:
        form = RegistrationForm()

    values = {
        'form': form,
        'register': True,
    }
    c = RequestContext(request, values)
    return render_to_response(template, c)

def front_login(request, template="front/login.html"):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = LoginForm()

    values = {
        'form':form,
        'login': True,
    }
    c = RequestContext(request, values)
    return render_to_response(template, c)


def createLessons(webUser):
    names = ['Introduction To Snappy', 'Lesson 2', 'Lesson 3', 'Lesson 4', 'Lesson 5', 'Lesson 6' ]
    descriptions = ['An introduction to the basic features of snappy and how to use them. Key terms: stage, sprite, pallet, block, scripts editor, script, saving', 'Variables', 'Conditionals', 'Loops', 'Circle', 'Spiral']
    difficulties = [1,1,2,2,3,3]
    num = len(names)
    guides = [guide1]

    for i in range(0, num):
        lesson = Lesson()
        lesson.name = names[i]
        lesson.description = descriptions[i]
        lesson.difficulty = difficulties[i]
        lesson.user = webUser
        lesson.isCompleted = False
        lesson.isStarted = False

        if i < len(guides):
            lesson.guide = guides[i]

        lesson.save()




guide1 = "<p>Hello there and welcome to the first Snappy Lesson! Snappy is a graphical environment that will allow you " \
         "to explore the fundamentals of programming while building awesome graphical creations. \
</p>\
<p>\
Lets start off with a quick introduction to some of the different tools available to you in the snappy programming\
 environment. The main areas we will be using are the pallet (left), editor (top center), and stage (top right).\
</p>\
<br>\
<ul>\
<li><b>Stage:</b> The stage is located in the top right. It has a white background with an 'arrow' in the middle. This \
is the place where our drawings are going to go.\
</li><br>\
<li><b>Sprite:</b> This is the 'arrow' in the middle of the stage. Later we will see how to create code that moves the \
sprite around to create all sorts of cool designs.\
</li><br>\
<li><b>Palette:</b> The pallet is located on the left side. It is filled with 'blocks' that allow you to manipulate \
the sprite in our stage.  The top most block should say 'move 10 steps.' If this is not the case, you probably \
clicked on a block category other than motion. You can access different block categories by clicking on the category \
buttons, located directly above the list of blocks. Try clicking on a different category to see different types of\
 blocks. When you are done, go back to the motion category.\
</li><br>\
<li><b>Blocks:</b> Blocks allow you to move the sprite around and create things in the stage. Try clicking \
on the block that says [move 10 steps] and watch as the sprite moves forward in the direction it is facing. \
Sometimes blocks also have a feature that you can change known as a parameter. In the [move 10 steps] block, \
change the 10 to 100 and see what happens when you click on it. Woah! The sprite went much further this time. \
If ever your sprite goes off the stage, you can always bring it back to the middle by clicking the block [go to x:0, y:0].\
</li></br>\
<li><b>Scripts Editor:</b> The scripts editor is located in the center of the screen. It is directly above the section\
 labeled 'Generated Python Code' (which we will discuss later). The scripts editor allows you to create scripts, which\
  are a combination of one or more blocks. To do this, drag a block from the pallet and drop it onto the scripts editor.\
   Next, drag another block from the pallet and attach it to the first. Now, clicking this script will execute both \
   blocks, one after the other, starting from the top.\
</li><br>\
<li><b>Example Script:</b> Try dragging the [move 10 steps] block onto the scripts editor and then attaching the\
 [turn left 15 degrees] block to it. Now, each time you click this script, your sprite will move forward and turn\
  left. If you want to move this way multiple times, this approach is significantly more convenient than alternating\
   between clicking the move forward and turn left blocks.\
</li><br>\
<li><b>Saving:</b> To save your progress on a particular lesson, click the button with the paper icon in the top\
 left and  select save. This will open a menu for you to enter a name for your creation and finish saving.\
</li>\
</ul>\
<hr>\
<p>\
Congratulations on completing your first snappy lesson! At this point you should understand the basics behind the\
 stage, a sprite, the pallet, blocks, the scripts editor, scripts, and saving. If you don't understand one of these \
 terms, its probably a good idea to scroll up and reread the section on it. \
</p>\
<p>\
In the next lesson, we will make scripts to create shapes with our sprite.\
</p>"
