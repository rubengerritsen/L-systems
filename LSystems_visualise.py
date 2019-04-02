# -*- coding: utf-8 -*-
"""
Created on 2019-04-01

@author: R.H.J. Gerritsen

LSystems_visualise.py is a module for visualising simple L-systems.
It contains a function for turtle interpretation of L-systems in 2D 
and functions/classes for visualising some particular L-systems (e.g. development of Anabaena catenula)


For code that computes L-systems: LSystems.py
For examples please refer to:     LSystems_examples.py

INSTALLATION: Put this file somewhere where Python can see it (e.g. in the 
		working directory.)

DEPENDENCIES: 1) This module depends on the graphics module 
              by John Zelle. Which can be downloaded from:
              https://mcsp.wartburg.edu/zelle/python/graphics.py

              2) Further, we only need the turtle package

OVERVIEW:     This module consists of a special class for the visualisation of 
              Anabaena Catenula and a function that interprets L-System output as 
              turtle graphics in 2D.
"""

import turtle 
from graphics import *

class Anabaena:
    """Class to draw the development of Anabaena catenula. """
    def __init__(self,x,y,height):
        self.win = GraphWin("Anabaena catenula", 1500, 1000)
        self.win.setBackground(color_rgb(0,0,0))
        self.cursorX = x
        self.cursorY = y
        self.height  = height

    def rectangle(self, width, color = 255):
        r = Rectangle(Point(self.cursorX,self.cursorY),Point(self.cursorX + width, self.cursorY + self.height))
        r.setFill(color_rgb(color,0,max(255-4*color,0)))
        r.draw(self.win)
        self.cursorX = self.cursorX + width + 2     
        
    def circle(self, diameter, color = []):
        c = Circle(Point(self.cursorX + (diameter)/2, self.height/2 + self.cursorY),(diameter)/2)
        c.setFill("red")
        c.draw(self.win)
        self.cursorX = self.cursorX + diameter + 2
        
    def setX(self,x):
        self.cursorX = x
                   
    def pause(self):
        self.win.getMouse()
        
    def nextLine(self, height):
        self.cursorY = self.cursorY + height
        self.cursorX = 50
        
    def done(self):
        #close on click
        update()
        self.win.getMouse() # Pause to view result
        self.win.close()    # Close window when done

    def drawGeneration(self, instructions, newLineDistance = 22):
        #obtain length of cells on line, to compute center
        length = 0
        for mod in instructions:
            if mod.symbol == "F" and mod.param[1] != 0:
                length = length + 4*mod.param[0] + 2
            elif mod.symbol == "F" and mod.param[1] == 0:
                length = length + 6*mod.param[0] + 2
        #set cursor to starting position
        self.setX(750-length/2)
        for mod in instructions:
            if mod.symbol == "F" and mod.param[1] != 0:
                self.rectangle(4*mod.param[0],int(255*mod.param[2]/(mod.param[2]+100)))
            elif mod.symbol == "F" and mod.param[1] == 0:
                self.circle(6*mod.param[0])
        self.nextLine(newLineDistance)



def turtle_interpretation(instructions, delta = 90, initialAngle = 90, distance = 1, width = 1):
    """Interprets a list of modules as a set of instructions for a turtle to draw a tree. """    
    ############ INITIALIZATION #############
    turtle.TurtleScreen._RUNNING = True
    turtle.tracer(0,0) #only display the result
    turtle.setup(1000,1000) #make the result a square with 1:1 ratios
    turtle.down()  #set the pen to drawing ("pen up" vs. "pen down")
    turtle.mode("world")
    turtle.setheading(initialAngle)
    turtle.width(width)
    turtleXmax = 0
    turtleXmin = 0
    turtleYmax = 0
    turtleYmin = 0

    turtlePosStack = []
    turtleHeadStack = []
    
    ######### MAIN FUNCTION ##############
    for mod in instructions:
        if mod.symbol[0] == "F":
            if mod.param == []:
                turtle.forward(distance)
            else:
                turtle.forward(float(mod.param[0]))
        elif mod.symbol == "f":
            turtle.up()
            if mod.param == []:
                turtle.forward(distance)
            else:
                turtle.forward(float(mod.param[0]))
            turtle.down()
        elif mod.symbol == "+":
            if mod.param == []:
                turtle.left(delta)
            else:
                turtle.left(mod.param[0])
        elif mod.symbol == "-":
            if mod.param == []:
                turtle.right(delta)
            else:
                turtle.right(mod.param[0])
        elif mod.symbol == "[":
            turtlePosStack.insert(0,turtle.pos())
            turtleHeadStack.insert(0,turtle.heading())
        elif mod.symbol == "]":
            turtle.up()
            turtle.goto(turtlePosStack.pop(0))
            turtle.setheading(turtleHeadStack.pop(0)) 
            turtle.down()
        turtleXmax = max(turtleXmax, turtle.xcor())
        turtleXmin = min(turtleXmin, turtle.xcor())
        turtleYmax = max(turtleYmax, turtle.ycor())
        turtleYmin = min(turtleYmin, turtle.ycor())

    # update screen and display size
    turtle.hideturtle()
    turtle.update() 
    # make sure the ratio of the picture is 1:1
    if (turtleXmax-turtleXmin) > (turtleYmax-turtleYmin):
        turtleYmax = turtleYmin + (turtleXmax-turtleXmin)
    else:
        turtleXmax = turtleXmin + (turtleYmax-turtleYmin)  
    margin = (turtleYmax-turtleYmin)*0.02 #margin is always 2 percent of picture width
    turtle.setworldcoordinates(turtleXmin-margin, turtleYmin-margin, turtleXmax+margin, turtleYmax+margin)

    ####### CLEANUP ###########
    # print("Press a key to continue:")
    # input()
    # turtle.bye()
    turtle.exitonclick()
    return 0



if __name__ == "__main__":
    print("For examples refer to: LSystems_examples.py")