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
    descriptions = ['An introduction to the basic features of snappy and how to use them. Key terms: stage, sprite, palette, block, scripts editor, script, saving', 'Variables', 'Conditionals', 'Loops', 'Circle', 'Spiral']
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
 environment. The main areas we will be using are the palette (left), scripts editor (top center), and stage (top right).\
</p>\
<br>\
<ul>\
<li><span id='highlight-stage'><b>Stage:</b></span> The stage is located in the top right. It has a white background with an 'arrow' in the middle. This \
is the place where our drawings are going to go.\
</li><br>\
<li><b id='highlight-sprite'>Sprite:</b> This is the 'arrow' in the middle of the stage. Later we will see how to create code that moves the \
sprite around to create all sorts of cool designs.\
</li><br>\
<li><b id='highlight-palette'>Palette:</b> The palette is located on the left side. It is filled with 'blocks' that allow you to manipulate \
the sprite in our stage.  The top most block should say 'move 10 steps.' If this is not the case, you probably \
clicked on a block category other than motion. You can access different block categories by clicking on the category \
buttons, located directly above the list of blocks. Try clicking on a different category to see different types of\
 blocks. When you are done, go back to the motion category.\
</li><br>\
<li><b id='highlight-blocks'>Blocks:</b> Blocks allow you to move the sprite around and create things in the stage. Try clicking \
on the block that says [move 10 steps] and watch as the sprite moves forward in the direction it is facing. \
Sometimes blocks also have a feature that you can change known as a parameter. In the [move 10 steps] block, \
change the 10 to 100 and see what happens when you click on it. Woah! The sprite went much further this time. \
If ever your sprite goes off the stage, you can always bring it back to the middle by clicking the block [go to x:0, y:0].\
</li></br>\
<li><b id='highlight-scripts'>Scripts Editor:</b> The scripts editor is located in the center of the screen. It is directly above the section\
 labeled 'Generated Python Code' (which we will discuss later). The scripts editor allows you to create scripts, which\
  are a combination of one or more blocks. To do this, drag a block from the palette and drop it onto the scripts editor.\
   Next, drag another block from the palette and attach it to the first. Now, clicking this script will execute both \
   blocks, one after the other, starting from the top.\
</li><br>\
<li><b>Example Script:</b> Try dragging the [move 10 steps] block onto the scripts editor and then attaching the\
 [turn left 15 degrees] block to it. Now, each time you click this script, your sprite will move forward and turn\
  left. If you want to move this way multiple times, this approach is significantly more convenient than alternating\
   between clicking the move forward and turn left blocks.\
</li><br>\
<li><b id='highlight-save'>Saving:</b> To save your progress on a particular lesson, click the button with the paper icon in the top\
 left and  select save. This will open a menu for you to enter a name for your creation and finish saving.\
</li>\
</ul>\
<hr>\
<p>\
Congratulations on completing your first snappy lesson! At this point you should understand the basics behind the\
 stage, a sprite, the palette, blocks, the scripts editor, scripts, and saving. If you don't understand one of these \
 terms, its probably a good idea to scroll up and reread the section on it. \
</p>\
<p>\
In the next lesson, we will make scripts to create shapes with our sprite.\
</p> \
<script> \
$('body').on('loaded', function() { \
\
$('#highlight-stage').mouseenter(function() {ide.highlightItem(this, true, 'stage');})\
.mouseleave(function() {ide.highlightItem(this, false, 'stage');});\
\
$('#highlight-sprite').mouseenter(function() {ide.highlightItem(this, true, 'currentSprite')})\
.mouseleave(function() {ide.highlightItem(this, false, 'currentSprite')});\
\
$('#highlight-palette').mouseenter(function() {ide.highlightItem(this, true, 'palette')})\
.mouseleave(function() {ide.highlightItem(this, false, 'palette')});\
\
$('#highlight-blocks').mouseenter(function() {ide.highlightItem(this, true, 'blocks')})\
.mouseleave(function() {ide.highlightItem(this, false, 'blocks')});\
\
$('#highlight-scripts').mouseenter(function() {ide.highlightItem(this, true, 'spriteEditor')})\
.mouseleave(function() {ide.highlightItem(this, false, 'spriteEditor')});\
\
$('#highlight-save').mouseenter(function() {ide.highlightItem(this, true, 'saveBtn')})\
.mouseleave(function() {ide.highlightItem(this, false, 'saveBtn')});\
\
})</script>"


guide2 = "<h3>Lesson 2</h3><p>Welcome to the second Snappy Lesson. In this lesson we are going to explore\
 different kinds of blocks and see how they can be used to create shapes like triangles, circles, and squares.\
</p>\
<br>\
<hr>\
<h3>Drawing</h3>\
<h5>Movement</h5>\
<p>\
The first lesson should have gotten you started with the basics of moving your sprite around. Sprite movement\
 important to drawing because we use our sprite to create lines! By this point, you should be familiar moving\
  your sprite forward, turning it left or right, and reseting it back to the middle. Additionally, if you ever \
  want to place your sprite at a specific spot, you can drag it anywhere in the stage with your mouse.\
</p>\
<br>\
<h5>Using Your Pen</h5>\
<p>\
As you probably noticed, when you move your sprite around, nothing is being drawn. To start drawing with our\
 sprite, we need to learn how to use the pen blocks. To do this select the Pen category in your palette. You \
 should now see blocks that are dark green, most of which contain the word pen. For now, the pen blocks you \
 should get comfortable using are:\
<ul>\
<br>\
<li><b>Clear:</b> Clears the stage of all pen drawings\
</li><br>\
<li><b>Pen Down:</b> Puts your pen down so that any sprite movement will draw a line in its wake.\
</li>\
<br>\
<li><b>Pen Up:</b> Brings your pen up so that your sprite can move without drawing a line.\
</li>\
<br>\
</ul>\
Try putting your pen down and then moving forward. Pretty cool eh? Don't like your first creation? \
No worries! You can always clear the screen with the clear block.\
</p>\
<br>\
<hr>\
<h3>Operators</h3>\
<p>Before we get too carried away making awesome designs, lets take a second and explore the power of \
operators. All of the operator blocks can be found in the Operators category, which is light green. \
Operators allow you to take advantage of math when creating designs. They allow you to do basic things \
such as addition and subtraction, but also give you more complex capabilities such as generating random numbers.\
</p>\
<br>\
<p>\
Notice that if you click on an operator, it will simply report its value and not affect anything on the screen. \
Furthermore, notice that operators cannot be attached to the bottom or top of another block. Instead, they can \
only be placed inside the editable part of another block.  Take a moment and try putting an operator inside of \
another block to see what happens.  For example, you could try putting the [pick random 1 to 10] block inside a \
[move forward] block. This should move your sprite forward by a random number of steps between 1 and 10.\
<br>\
<hr>\
<h3>Putting It All Together</h3>\
<h5>Drawing A Triangle</h5>\
<p>\
Now that we know how to draw lines and we know what operators are, lets combine these two skills to make \
scripts that draw some cool shapes.\
</p><br>\
<p>\
Lets start out by drawing a triangle. To do this, first make sure that your screen is clear and your \
sprite is centered in the middle. Next, attach a move forward block to the bottom of a pen down block \
and then attach a turn block to the bottom of that.  After you do this, place a division operator inside \
of the turn block. Since a triangle is comprised of 3 angles that add up to 360 degrees, each angle should \
be 360 / 3 = 60 degrees. Put 360 / 3 into your division statement and try clicking your script three times. \
If everything is correct, the result should be a triangle! You can change the size of the triangle by changing \
how many steps you move.\
</p>\
<br>\
<h5>More Shapes</h5>\
One of the greatest things about programming is how easy it is to build many things out of one solution. Using \
the same blocks that created our triangle, how would we draw a square? In a square, because there are four angles, \
each angle is 360 / 4 = 90 degrees. Therefore, if we divide by 4 rather than 3, we can make a square.\
</p>\
<br>\
<p>\
Try drawing more shapes by changing how much we divide 360 by. How does the drawn shape relate to the value \
of the divisor? Can you draw a circle?\
</p>\
<br>\
<hr>\
<p>\
If you tried making a circle, you will have noticed that the more circular your shape becomes, the more clicks\
 it requires to build. In the next lesson we will learn how to automate this process with loops and then learn \
 how to create spirals using loops and variables!\
</p>"