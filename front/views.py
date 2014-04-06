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
    names = ['Introduction To Snappy', 'Drawing Shapes: The Hard Way', 'Drawing Shapes: The Easy Way', 'Introduction To Python', 'Drawing a Spiral With Python: Part 1', 'Drawing a Spiral With Python: Part 2']
    descriptions = [desc1, desc2, desc3, desc4, desc5, desc6]
    difficulties = [1,1,2,2,3,3]
    num = len(names)
    guides = [guide1, guide2, guide3, guide4, guide5, guide6]

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




guide1 = "<h3>Welcome!</h3><p>Hello there and welcome to the first Snappy Lesson! Snappy is a graphical environment that will allow you " \
         "to explore the fundamentals of programming while building awesome graphical creations. \
</p>\
<p>\
Lets start off with a quick introduction to some of the different tools available to you in the snappy programming\
 environment. In the following bullet points, mouse over the titles to highlight the location of each corresponding section.\
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
$('#highlight-blocks').mouseenter(function() {ide.highlightBlocks(this, true)})\
.mouseleave(function() {ide.highlightBlocks(this, false)});\
\
$('#highlight-scripts').mouseenter(function() {ide.highlightScripts(this, true)})\
.mouseleave(function() {ide.highlightScripts(this, false)});\
\
$('#highlight-save').mouseenter(function() {ide.highlightItem(this, true, 'saveBtn')})\
.mouseleave(function() {ide.highlightItem(this, false, 'saveBtn')});\
\
})</script>"
desc1 = 'An introduction to the basic features of snappy and how to use them. Key terms: stage, sprite, palette, block, scripts editor, script, saving.'


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
  your sprite forward, turning it left or right, and resetting it back to the middle. Additionally, if you ever \
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
desc2 = "Learn how to draw and create shapes. Key terms: movement, pen, operators."

guide3 = "<h3>Shapes Continued</h3>\
<p>\
In this lesson we will learn about two of programmings most powerful tools: loops and variables.  Loops and\
 variables make it possible to program using significantly less code.\
</p>\
<br>\
</hr>\
<h4>Circles and Loops</h4>\
If you tried making a circle in the previous lesson, you will have noticed \
that to complete the circle, you have to click your block a lot of times. This \
is because drawing regular convex polygons (triangles, squares, pentagons, etc.) \
requires 1 click per each side, and circles are just regular convex polygons with \
many sides. Therefore, the more perfect your circle becomes, the more clicks you need to make it.\
</p>\
<br>\
<p>\
Obviously we don't want to sit and click our block hundreds of times, so we need some way to automate the process.\
 The solution to this problem is a loop. A loop allows you to execute a certain script for a set period of time\
  (or forever).\
</p>\
<br>\
<p>\
In Snap, you can find loop blocks in the control category. Loop blocks are shaped like a 'C' and allow you to put\
things inside of them. Based on the type of loop, the blocks inside of the loop will be run a certain amount of\
times. The three types of loops that snap provides are:\
<br>\
<ul>\
<li><b>Forever:</b> Continues to execute the code inside of the loop block forever until you tell it to stop.\
<li><b>Repeat 10:</b> Executes the code inside of the loop block 10 times. Note that 10 is only the default\
value and can be changed to any number of times.\
<li><b>Repeat until:</b> Executes the code inside of the loop block until a condition is met. As these \
conditions usually involve variables, we will look at this type of loop more in the future.\
</ul>\
<br>\
Now, lets make a circle with a loop. To start, we need to recreate the code we used to make shapes in the \
previous lesson. To do this you will need a move block, a turn block, and a division operator block. Once\
 you have done this, drag the repeat 10 block into your scripts editor and place your previous code inside \
 of it. Then, change the loop's parameter, 10, to the value of your division block's divisor. Clicking once \
 on this new script should create the entire shape! Try increasing the values of your divisor and loop parameter. \
 As you do this you should notice that your shape becomes more circular!\
</p>\
<br>\
<hr>\
<h4>Variables</h4>\
When creating circles in the previous section, if you wanted to draw the complete circle, you had to make \
sure that your operator divisor was equal to the number of loops that you were doing. Every time you wanted\
 to change the number of sides, both of these values had to be updated. While this is not such a hassle \
 here, in large programs, the same number is referenced in hundreds of places. In this case, changing one \
 value requires changing the other hundreds of locations as well. Variables solve this problem of referencing \
 the same value in multiple places. Rather than setting our parameters as numbers, we can set our parameters \
 to be variables, and then set value of those variables. </p>\
<br>\
<p>\
To use variables in snap, go to the variables category. Once there, click on the block that says, 'Make a \
variable.' This allows you to create your own  variable. You are allowed to name is whatever you want, \
however keep in mind that the best names are ones that are compact, descriptive, and contain no spaces. Once \
you have created a variable, notice that a new block representing your variable appears in your palette. You \
can drag this block and drop it in any parameter spot on other blocks. To use our variable, we first need to set\
 its value. This can be done with the set block, located directly below your variable's block.\
</p>\
<br>\
<p>\
To see how we might actually use variables, lets go back to our shape drawing exercise. Rather than \
entering a value for the divisor and repeat value, drop your variable in those parameter slots. Then\
, before everything, add a set block that sets your variable to a number. If you click this new script \
you will notice that it will draw a shape with as many sides as you set your variable to be. Changing the \
amount of sides is as easy as changing the value of your variable!\
</p>\
<br>\
<hr>\
<h4>Putting It All Together</h4>\
<h5>Drawing all Shapes</h5>\
<p>\
In this last example, we will use our knowledge of loops and variables to draw many shapes, \
with an increasing number of sides, all at once. To do this, we must use the concepts of nested \
loops, variable increments, and conditional loops.\
<ul>\
<li><b>Nested Loop:</b>\
A nested loop is simply when you put one loop inside of another. When doing this, for every \
iteration of the outer loop, the inner loop must complete all of its iterations.\
<li><b>Variable Increments:</b>\
This is when you increase the value of your variable. In snap you can do this with change \
by block, which is below the set block in the variables category.\
<li><b>Conditional Loops:</b> A conditional loop is when, rather than specifying the number \
of loop iterations up front, you loop until a condition is met. In many cases this condition\
 will depend on the value of one or more variables.\
</ul>\
<p>\
To make all of our shapes in order, try creating with blocks what I describe with words. \
First, you want to set a variable, let us call it 'numSides,' to 3, the minimum number of \
sides needed to make a polygon. Below this, add a loop that will repeat until numSides is \
equal to 20. The equality block can be found in the operators category. Nested inside this \
outer loop you should place your loop for creating a shape with a variable number of sides.\
 Make sure that in this loop, the number of sides is governed by the 'numSides' variable. \
 After completing this inner loop, change the 'numSides' variable by 1. If you have done this \
 correctly, you should be able to draw all the regular convex polygons with between 3 and 20 \
 sides. To change the size of the shapes, alter how much we move by to create each side. To \
 create polygons with up to 100 sides, change our conditional loop to stop when 'numSides' \
 equals 100. To start with polygons of more sides than 3, set 'numSides' to a larger value in the beginning.\
</p>\
</br>\
<hr>\
<h5>Congratulations!</h5>\
<p>You may not have realized it, but you now know some of the most important concepts behind every \
program. At this point, feel free to experiment making awesome designs. When you are ready, go on to \
the next lesson where we will see how concepts such as loops and variables are used in my favorite programming \
language, python!"
desc3 = "Use programming techniques to create shapes with ease. Key terms: loops, variables, conditions."

guide4 = "<h3>Introduction to Python</h3><p>\
In this lesson we will begin learning the python programming language! Why do this? \
Well, the reason is that while snap is awesome for making designs, it can be overly \
bulky and tedious for many problems. Furthermore, snap blocks can only be used inside \
this application, where as a textual programming language like python was used to build \
this application. In fact, many popular websites such as Youtube and Reddit are built with \
python. Luckily for us, many of the concepts we used to draw shapes, such as scripts, parameters, " \
         "variables and loops have direct counterparts in python.</p><br><hr><p><h4>The Code View</h4>\
As you probably noticed, when you were snapping blocks together in the scripts Editor, code was being " \
         "generated in the pane below. This pane is called the code view and the code generated inside " \
         "of it is actually python code! Furthermore, this code is a direct representation in python of " \
         "your snap blocks. Try building some block scripts and check out what the equivalent code in python" \
         " looks like. While the python syntax requires memorization, you should see that, if read out loud, " \
         "many of the python commands are relatively intuitive. If you are curious about which block a line of" \
         " python code corresponds to, simply mouse over the python code and the corresponding block will get " \
         "highlighted.</p><br><hr><h4>Executing Python</h4>\
Snappy also gives you the ability to execute your python code directly. To see how this works, try dragging out a" \
         " [move 10 steps] block into the scripts editor. Find the corresponding python code that is generated and" \
         " click the edit button that is next to it. This will bring up the Code Editor. The Code Editor allows you " \
         "to edit your python scripts. Only moving 10 steps forward is hardly noticeable, so try changing the 10 to " \
         "100. </p><br>\
<p>Before executing your script, notice that the first line says, 'import turtle.' This line of code allows " \
         "us to use the turtle library. Because most programming languages have so many capabilities, and at" \
         " any given time you will only be using a few of them, it would be wasteful to include everything by" \
         " default.  Therefore, libraries are used to allow a user to include only what they need for a project." \
         " The turtle library allows us to manipulate a turtle, another name for our sprite. Libraries allow us " \
         "to use, functions. Functions are similar in many respects to snap blocks.  You pass functions parameters " \
         "and they either return something (like an operator) or they do something (like a movement block). Forward " \
         "is an example of a function in the python turtle library that does something. To run functions that are" \
         " part of a library, the syntax is:<br><br><b>library.function(parameters)</b><br><br>\
For example, to move forward 100 steps, we must type turtle.forward(100).</p><br>\
<p>To run python code, click the Visualize Execution button. This will bring you to the python visualizer, a place " \
         "for you to run your python code and see how your sprite is affected. The visualizer gives you the option " \
         "to step line by line through the python code or begin an automatic execution. When automating the execution " \
         "process, the execution speed can be changed using the execution speed slider. Additionally, you can stop the " \
         "automatic execution at any point with the red stop button.</p><br><hr><p>\
At this point you should be able to (1) drop blocks in the scripts editor, (2) see the corresponding python code appear " \
         "in the code view, (3) edit this code in the code editor, and (4) execute this code with the python visualizer." \
         "  Try performing this series of steps with different combinations of movement blocks to see how these blocks " \
         "correspond to python statements. While the python code looks different, you  should notice that the same types" \
         " of sprite manipulations can be done.</p><br><p>\
In the next lesson we will see how different snap blocks, such as variables, loops, and operators, are expressed in python."

desc4 = "Learn how to execute python code in Snappy. Key terms: code view, code editor, library, function, python visualizer."


guide5 = "<h3>Python Spirals</h3>\
In this lesson we will explore how python handles some more of snap's blocks. We will do this by trying to user python to draw a" \
         " square spiral, which will require a combination of loops and variables.</p><br>\
<h4>Drawing a Square with Variables</h4>\
If you have a piece of paper in front of you, try drawing a square spiral on it. You will notice that it is very" \
         " similar to drawing a square, however after every two sides drawn, the side length increases. Therefore," \
         " the first part of drawing a square spiral is drying the sides of a square where the side length is based" \
         " on a variable. To start off, make a variable and set this variable to 1. Then, put your pen down, move " \
         "a number of steps based on your variable, and turn 360 / 4 = 90 degrees. When moving forward, I recommend" \
         " using the multiplication operator to move forward 10 times your variable. Once you have created this, " \
         "clicking on it 4 times should draw a complete square. Increasing the value of your variable will make " \
         "this square larger. </p><br>\
<p>\
Now lets take a look at the python code generated for this script. In python, the way to set a variable to a " \
         "value is by using the = sign. For example, to set a variable named, myVar, to 5, I would write: " \
         "myVar = 5. When doing this, a variable must always be on the left side of the equals sign. The = " \
         "sign then sets the variable on the left side to the value of whatever is on the right side. " \
         "Alternatively, as we will see later, if we want to check if two values are equal, we use the == operator.\
</p><br>\
<p>After setting the value of our variable, we put our pen down. This is done by calling the pendown function from " \
         "the turtle library. Functions are noticeable in python because they always have parenthesis after them. " \
         "These parenthesis are where you would put a function's parameters. However, because the pendown function" \
         " does not take any parameters, nothing will be inside of its parameters. </p><br><p>\
The next command is the turtle.forward function that moves our sprite forward. The parameter here is how far forward " \
         "we want to go. When drawing a side, we want to move forward the value of our parameter times 10. To do this " \
         "in python, just pass as a parameter your variable multiplied by the number 10. To reference a variable, " \
         "just type its name. To multiply it by something, use the '*' key. In general, python allows you to add " \
         "two values with '+', subtract one value from another with '-', multiply two values with '*', and divide " \
         "one value by another with '/'.  Lastly, we want to use the turtle function right to turn right 90 degrees.\
At this point, try executing your python code with the python visualizer by using the forward button. When you " \
         "have done this, go back to the code editor and assign different values to your variable. How do you " \
         "expect this to change your side lengths? If you want, you can also try changing how far you move by " \
         "using operators other than '*'.</p><br>" \
         "You may not realize it, but using this code we can make a spiral with a bit of manual labor. To see this, " \
         "try running it twice, incrementing your variable by 1, and then "\
         "running it twice again. You will notice that this creates the beginnings of a spiral! In the next lesson we" \
         " will see how we can completely automate this process using python."
desc5="Use python to begin drawing a spiral. Key terms: python variables, assignment, python operators."

guide6 = "<h3>Drawing a Complete Spiral</h3>\
Welcome to the last snappy lesson. In this lesson we will finish making our spiral in python. " \
         "In the previous lesson we saw how code to draw a square could be used to draw a spiral. However, " \
         "we definitely wouldn't want to draw a big spiral with this code because it would require manual labor to draw every side. " \
         "Therefore, like we did previously when drawing polygons, lets automate this process with loops. Before we begin," \
         "recreate your code from last lesson here. As a refresher, it should use a variable to draw one side of a square and then turn 90" \
         "degrees.</p><br>\
<p>\
The first thing to consider is that we want to draw two sides of the same length before incrementing the length. " \
         "To do this, use a repeat 10 loop block, but instead of repeating 10 times, repeat twice. Since we only " \
         "want to repeat our movements twice, do not put the set variable or pendown blocks inside this loop. " \
         "Clicking on this new script should draw two sides of a square.\
</p><br><p>\
Lets look at the python code for this script. The only new piece is the loop which in python is represented " \
         "by, 'for _ in range(0,2):'. When actually running this, the _ should be replaced by the name of a " \
         "new variable. When the loop is run, it creates a variable with the name you put in place of the _ " \
         "and sets this variable to the first range parameter (i.e. 0). Then, after every iteration of the " \
         "loop, it increments this variable by 1, and runs the loop again if this variable is less than the second " \
         "parameter given for range (i.e. 2).</p><br><p>\
In this specific loop, the _ variable will be set to 0 first. Since 0 is less than 2, we will run everything in " \
         "the loop. Then the variable will be set to 1. Since 1 is less than 2, everything in the loop will be " \
         "run again. The variable will then be set to 2. Since 2 is not less than 2, the loop will not be run " \
         "again.</p><br><p>\
<p>The last question is how to specify what is inside of a loop in python. In snap, things inside a loop are " \
         "contained within its 'C'. In python, this is done using indentation. To define code as part of a " \
         "loop, we indent it after defining the loop. Typically we use one tab, or four spaces, to indent.</p><br><p>\
If you are confused about how loop variables are, try running our current python. To do this, click the edit " \
         "button in the code view, replace the _ with a variable name in the code editor, and start the python " \
         "visualizer. This time, notice that on the right side of the visualizer, the current state of your " \
         "variables is shown as you step through your python code. Using this, watch how your loop variable " \
         "changes with every iteration of your loop.</p><br><p>\
The last step in making a spiral is to repeat this whole process for a certain number of times, each " \
         "time increasing the side length. We are going to do this the same way we created lots of " \
         "different sized polygons at the same time: with a conditional loop that stops when our variable " \
         "gets to be a certain value. To do this, use the 'repeat until' loop and repeat our current loop " \
         "until the side length variable equals 10. </p><br><p>\
The last thing to do is to increment our side length variable by 1 after drawing two sides of the same " \
         "length. This incrementation of our variable should be done outside our inner loop, but inside " \
         "our outer conditional loop. Clicking on this script should automate the process of drawing a " \
         "spiral!</p><br><p>\
Now, before we finish, lets see how this works in python. To use a conditional loop in python, we use " \
         "the syntax 'while condition:'. This repeats the loop as long as the condition is still true. " \
         "If we want to repeat the loop only while the condition is false, as in this case, we write " \
         "'while not condition:'. The condition that we are stopping on is when our variable equals 10. " \
         "Notice that python uses '==' to check if two values are equal (because = is used for assignment). " \
         "Also notice that everything inside the outer loop is indented once, and everything inside the inner " \
         "loop is indented twice. This is because we run the complete inner loop every time we run the outer " \
         "loop once. </p><br><p>\
Lastly, notice that we use 'myVar += 1' to increment myVar by 1. The '+=1' operator is simply shorthand \
for 'myVar = myVar + 1'. This works by assigning the value of myVar + 1 to myVar. In this case we are using " \
         "1 as an example, but it is possible to increment our variable by any amount by replacing 1 with " \
         "that amount.</p><br>\
<p>\
You've now written the code to draw a spiral in python! To get a deeper understanding of what is " \
         "going on, try stepping through your program with the python visualizer. </p><br><hr><p>\
<h4>The End!</h4>\
Unfortunately, this concludes the official snappy tutorial. Hopefully you've had a blast using snap " \
         "and python to draw polygons and spirals. While there are no more lessons, plenty of designs " \
         "such as ten pointed stars and crescent moons are waiting to be drawn. Additionally, if you " \
         "want to continue learning python outside of snappy, I recommend using " \
         "<a href='http://www.codecademy.com/tracks/python' target='_blank'>Codecademy</a>."
desc6="Use python to finish drawing a spiral. Key terms: python equality, python loops, incrementing python variables."