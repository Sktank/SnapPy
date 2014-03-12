
# Override of the python turtle module
# used for snap commands with visualizer

import math
import turtle_commands

# file to receive turtle commands and report them to visualizer
f = open('turtle_commands', 'w')



# global variables that keep track of turtle's state
x = 0.0
y = 0.0
orientation = 0.0
penSize = 1

# writes commands to file
def report(command):
    turtle_commands.setTurtleCommand(command + '\n')

#    f.seek(0)
#    f.write(command + '\n')
#    f.flush()


# The following are stub overrides of the python turtle module to be
# used by the python visualizer.

# These function stubs fall into the following categories:

#    Turtle motion
#       Move and draw
#           forward() | fd()
#           backward() | bk() | back()
#           right() | rt()
#           left() | lt()
#           goto() | setpos() | setposition()
#           setx()
#           sety()
#           setheading() | seth()
#           home()
#           circle()
#           dot()
#           stamp()
#           clearstamp()
#           clearstamps()
#           undo()
#           speed()
#       Tell Turtle's state
#           position() | pos()
#           towards()
#           xcor()
#           ycor()
#           heading()
#           distance()
#       Setting and measurement
#           degrees()
#           radians()
#    Pen control
#       Drawing state
#           pendown() | pd() | down()
#           penup() | pu() | up()
#           pensize() | width()
#           pen()
#           isdown()
#       Color control
#           color()
#           pencolor()
#           fillcolor()
#           Filling
#           fill()
#           begin_fill()
#           end_fill()
#       More drawing control
#           reset()
#           clear()
#           write()
#    Turtle state
#       Visibility
#           showturtle() | st()
#           hideturtle() | ht()
#           isvisible()
#       Appearance
#           shape()
#           resizemode()
#           shapesize() | turtlesize()
#           settiltangle()
#           tiltangle()
#           tilt()
#    Using events
#           onclick()
#           onrelease()
#           ondrag()
#           mainloop() | done()
#    Special Turtle methods
#           begin_poly()
#           end_poly()
#           get_poly()
#           clone()
#           getturtle() | getpen()
#           getscreen()
#           setundobuffer()
#           undobufferentries()
#           tracer()
#           window_width()
#           window_height()

#################################################################
#                        Turtle Motion                          #
#################################################################

# Move and Draw

def forward(distance):
    global x, y
    x += math.cos(orientation) * distance
    y += math.sin(orientation) * distance
    report("forward:" + str(distance))

def fd(distance):
    forward(distance)

def backward(distance):
    global x, y
    x -= math.cos(orientation) * distance
    y -= math.sin(orientation) * distance
    report("backward:" + str(distance))

def bk(distance):
    backward(distance)

def back(distance):
    backward(distance)

def right(angle):
    global orientation
    orientation -= angle
    orientation %= 360
    report("right:" + str(angle))

def rt(angle):
    right(angle)

def left(angle):
    global orientation
    orientation += angle
    orientation %= 360
    report("left:" + str(angle))

def lt(angle):
    left(angle)

def setpos(xpos, ypos):
    global x, y
    x = xpos
    y = ypos
    report("setpos:" + str(x) + ":" + str(y))

def goto(xpos, ypos):
    setpos(xpos, ypos)

def setposition(xpos, ypos):
    setpos(xpos, ypos)

def setx(xpos):
    global x
    x = xpos
    report("setx:" + str(x))

def sety(ypos):
    global y
    y = ypos
    report("sety:" + str(y))

def setheading(angle):
    global orientation
    orientation = angle
    orientation %= 360
    report("seth:" + str(orientation))

def seth(angle):
    setheading(angle)

def home():
    setpos(0.0,0.0)
    setheading(0)


#    Tell Turtle's state
def position():
    print "(" + str(x) + ',' + str(y) + ")"

def pos():
    position()

def towards(xcord, ycord):
    pass
    #Return the angle between the line from turtle position to position specified by (x,y), the vector or the other turtle.

def xcor():
    global x
    return x

def ycor():
    global y
    return y

def heading():
    global orientation
    return orientation

def distance():
    pass
    #Return the distance from the turtle to (x,y), the given vector, or the given other turtle, in turtle step units.

#################################################################
#                          Pen Control                          #
#################################################################

#   Drawing state

def clear():
    report("clear")

def pendown():
    report("pendown")

def pd():
    pendown()

def down():
    pendown()

def penup():
    report("penup")

def pu():
    penup()

def up():
    penup()


# how to handle case where user inputs a negative pensize?
def pensize(width=None):
    global penSize
    if not width:
        return penSize
    else:
        penSize = width
        report("pensize:" + str(penSize))

def width(width=None):
    pensize(width)

def stamp():
    report("stamp")





