# -*- coding: utf-8 -*-
"""
Created on 2019-04-02

@author: R.H.J. Gerritsen

LSystems_3D.py contains a 3D turtle graphics class and applies this to L-systems.
As a result 3D trees can be simulated using L-systems. The code also allows for 
the simulation of tropisms.

To see what this code can do, simply run the file and follow the instructions 
to see a few cases (trees and shrubs).

INSTALLATION: Put this file somewhere where Python can see it (e.g. in the 
              working directory.)

DEPENDENCIES: This module depends on LSystems.py and VPython
              VPython: https://vpython.org/ 

OVERVIEW:     This module contains a few examples that illustrate the use of a 
              3D turtle graphics class applied to L-systems.
"""
from vpython import *
from LSystems import *
import os

class Turtle3D:
    def __init__(self, pos=vector(0,0,0), heading = vector(0,1,0), leftDirection = vector(-1,0,0), upDirection = vector(0,0,1), width = 1):
        self.position        = pos
        self.heading         = heading
        self.leftDirection   = leftDirection
        self.upDirection     = upDirection
        self.isDrawing       = True
        self.curveStack      = []
        self.widthStack      = []
        self.colorStack      = []
        self.listOfVectors   = []
        self.width           = width
        self.polygon         = False
        self.currentColor    = vector(151/255,75/255,0)
        keys = ['pos', 'color' ,'radius']
        values = [self.position, self.currentColor, self.width]
        self.c               = curve(dict(zip(keys, values)))
        
    def forward(self, distance = 1):
        oldPosition = self.position
        self.position = self.position + distance * norm(self.heading)
        keys = ['pos', 'color' ,'radius']
        values = [self.position, self.currentColor, self.width]
        new_pos = dict(zip(keys, values))
        if self.isDrawing:
            self.c.append(new_pos)
        if self.polygon:
            self.listOfVectors.append(self.position)
    
    def turnLeft(self, angle = 22.5):
        self.leftDirection = self.leftDirection.rotate(radians(angle),self.upDirection)
        self.heading  = self.heading.rotate(radians(angle),self.upDirection)
    
    def turnRight(self, angle = 22.5):
        self.leftDirection = self.leftDirection.rotate(radians(-angle),self.upDirection)
        self.heading  = self.heading.rotate(radians(-angle),self.upDirection)
    
    def pitchUp(self, angle = 22.5):
        self.upDirection = self.upDirection.rotate(radians(angle),self.leftDirection)
        self.heading  = self.heading.rotate(radians(angle),self.leftDirection)
    
    def pitchDown(self, angle = 22.5):
        self.upDirection = self.upDirection.rotate(radians(-angle),self.leftDirection)
        self.heading  = self.heading.rotate(radians(-angle),self.leftDirection)
    
    def rollLeft(self, angle = 22.5):
        self.upDirection = self.upDirection.rotate(radians(angle),self.heading)
        self.leftDirection  = self.leftDirection.rotate(radians(angle),self.heading)
    
    def rollRight(self, angle = 22.5):
        self.upDirection = self.upDirection.rotate(radians(-angle),self.heading)
        self.leftDirection  = self.leftDirection.rotate(radians(-angle),self.heading)
        
    def xcor(self):
        return(self.position.x)
    
    def ycor(self):
        return(self.position.y)
    
    def zcor(self):
        return(self.position.z)
    
    def penUp(self):
        self.isDrawing = False
    
    def penDown(self):
        self.isDrawing = True
        # Start a new curve when we restart drawing
        keys = ['pos', 'color' ,'radius']
        values = [self.position, self.currentColor, self.width]
        new_pos = dict(zip(keys, values))
        self.c = curve(new_pos)
    
    def setHeading(self,heading):
        self.heading       = heading[0]
        self.leftDirection = heading[1]
        self.upDirection   = heading[2]
    
    def getHeading(self):
        return((self.heading, self.leftDirection, self.upDirection))
    
    def setPosition(self, pos):
        self.position = pos
    
    def getPosition(self):
        return(self.position)
    
    def pushCurve(self):
        self.curveStack.insert(0, self.c)
        self.widthStack.insert(0, self.width)
        self.colorStack.insert(0, self.currentColor)
        # start new curve
        keys = ['pos', 'color', 'radius']
        values = [self.position, self.currentColor, self.width]
        new_pos = dict(zip(keys, values))
        self.c = curve(new_pos)
    
    def popCurve(self):
        self.c = self.curveStack.pop(0)
        self.width = self.widthStack.pop(0)
        self.currentColor = self.colorStack.pop(0)

    def setWidth(self, width):
    	self.width = width
        
    def decrementDiameter(self, scaling):
        self.width = self.width*scaling
        
    def startPolygon(self):
        """Only works for convex polygons in a single plane."""
        self.polygon = True
        self.listOfVectors.append(self.position)
    
    def endPolygon(self):
        """Only works for convex polygons in a single plane.
        
        This is just simple fan triangulation
        """
        self.polygon = False
        for i in range(2,len(self.listOfVectors)):
            triangle(vs = [vertex(pos = self.listOfVectors[0], color = self.currentColor), 
                           vertex(pos = self.listOfVectors[i-1],color = self.currentColor), 
                           vertex(pos = self.listOfVectors[i],color = self.currentColor)])
        self.listOfVectors = []
        
    def setColor(self, rgb):
        self.currentColor = vector(rgb[0]/255,rgb[1]/255,rgb[2]/255)

    def applyTropism(self, tropismVec, tropismStrength):
    	correction = tropismStrength * cross(norm(self.heading),tropismVec)
    	self.heading +=  self.heading.rotate(mag(correction),correction)

    def drawGround(self, size):
    	box(pos=vector(0,0,0), length=size, height=-size/100, width=size, color = vector(10/255,85/255,0))
    

def turtle_interpretation_3D(scene, instructions, delta = 22.5, width = 0.3, widthScaling = 0.7, tropismVec = vector(0,0,0), tropismStrength = 0):
    """Interprets a set of instructions for a turtle to draw a tree in 3D. """    
    ############ INITIALIZATION #############
    bob = Turtle3D(width = width)
    
    turtlePosStack = []
    turtleHeadStack = []
    
    turtleXmax = 0
    turtleXmin = 0
    turtleYmax = 0 
    turtleYmin = 0
    turtleZmax = 0
    turtleZmin = 0
    
    ######### MAIN FUNCTION ##############
    for mod in instructions:
        if mod.symbol == "F":
        	bob.applyTropism(tropismVec, tropismStrength)
        	if mod.param == []:
        		bob.forward()
        	else:
        		bob.forward(mod.param[0])
        	#Note that we only need to update the max coordinates if the turtle has moved
        	turtleXmax = max(turtleXmax, bob.xcor())
        	turtleXmin = min(turtleXmin, bob.xcor())
        	turtleYmax = max(turtleYmax, bob.ycor())
        	turtleYmin = min(turtleYmin, bob.ycor())
        	turtleZmax = max(turtleZmax, bob.zcor())
        	turtleZmin = min(turtleZmin, bob.zcor()) 
        elif mod.symbol == "f":
        	bob.penUp()
        	if mod.param == []:
        		bob.forward()
        	else:
        		bob.forward(mod.param[0])
        	bob.penDown()
        elif mod.symbol == "+":
        	if mod.param == []:
        		bob.turnLeft(delta)
        	else:
        		bob.turnLeft(mod.param[0])
        elif mod.symbol == "-":
        	if mod.param == []:
        		bob.turnRight(delta)
        	else:
        		bob.turnRight(mod.param[0])
        elif mod.symbol == "&":
        	if mod.param == []:
        		bob.pitchDown(delta)
        	else:
        		bob.pitchDown(mod.param[0])
        elif mod.symbol == "^":
        	if mod.param == []:
        		bob.pitchUp(delta)
        	else:
        		bob.pitchUP(mod.param[0])
        elif mod.symbol == "\\":
        	if mod.param == []:
        		bob.rollLeft(delta)
        	else:
        		bob.rollLeft(mod.param[0])
        elif mod.symbol == "/":
        	if mod.param == []:
        		bob.rollRight(delta)
        	else:
        		bob.rollRight(mod.param[0])
        elif mod.symbol == "|":
            bob.turnLeft(180)
        elif mod.symbol == "[":
            turtlePosStack.insert(0,bob.getPosition())
            turtleHeadStack.insert(0,bob.getHeading())
            bob.pushCurve()
        elif mod.symbol == "]":
            bob.setPosition(turtlePosStack.pop(0))
            bob.setHeading(turtleHeadStack.pop(0)) 
            bob.popCurve()
        elif mod.symbol == "!":
        	if mod.param == []:
        		bob.decrementDiameter(widthScaling)
        	else:
        		bob.setWidth(mod.param[0])
        elif mod.symbol == "{":
            bob.startPolygon()
        elif mod.symbol == "}":
            bob.endPolygon()
        elif mod.symbol == "'":
            bob.setColor(mod.param)
    
    #point the camera to the center of our drawing
    xcenter = 0
    ycenter = (turtleYmax+turtleYmin)/2
    zcenter = 0
    scene.center=vector(xcenter,ycenter,zcenter)
    # draw some a ground plane
    bob.drawGround(max(turtleXmax,turtleZmax)*2)
    scene.ambient=color.gray(0.4)
    return 0

if __name__ == "__main__":
    print("")
    print("Welcome to the 3D examples of the LSystems.py module:")
    print("")
    print("Select one of the following cases by entering the corresponding number.")
    print("To exit a visualisation press enter in the command prompt.")
    print("To exit the program simply type 'exit' and press enter.")
    print("")
    print("CASES:")
    print("{:5} {:<5} {:<25} {:<22}".format("", "0)", "Shrub with leaves", "May take a while to fully render"))
    print("{:5} {:<5} {:<25} {:<22}".format("", "1)", "Simple tree 1", ""))
    print("{:5} {:<5} {:<25} {:<22}".format("", "2)", "Simple tree 2", ""))
    print("{:5} {:<5} {:<25} {:<22}".format("", "3)", "Tree with phototropism", "Shows an L-system visualised with a tropism"))
    user_input = ""
    while user_input != "exit":
        user_input = input("Enter case as a number or type 'exit' to close: ")
        if user_input == "exit":
                break
        try:
            choice = int(user_input)
            print("Running case: ", choice)
        except ValueError:
            print("That is not a valid choice, try again: ")
            continue #start again at the top of the while loop
        if choice == 0: #shrub with leaves
            axiom = "A"    
            productions = ["A?'(151,75,0) [ & F L ! A ] / / / / / '(151,75,0) [ & F L ! A ] / / / / / / / '(151,75,0) [ & F L ! A ]", 
                       "F?S / / / / / F",
                       "S?F L",
                       "L?[ '(12,102,0) ^ ^ { - f + f + f - | - f + f + f } ]"]
            nrOfIterations = 7
            width = 1
            definitions = []
            tropismVector   = vector(0,0,0)
            tropismStrength = 0
        elif choice == 1: #simple tree 1
            axiom = "A(10,1)"
            productions = ["A(l,w)?!(w) F(l) [ &(a0) B(l*r2,w*wr) ] /(137.5) A(l*r1,w*wr)", 
                       "B(l,w)?!(w) F(l) [ -(a2) $ C(l*r2,w*wr) ] C(l*r1,w*wr)",
                       "C(l,w)?!(w) F(l) [ +(a2) $ B(l*r2,w*wr) ] B(l*r1,w*wr)"] 
            nrOfIterations = 10
            width = 1
            definitions = [['r1', 0.9],
                          ['r2', 0.6],
                          ['a0', 45],
                          ['a2', 45],
                          ['d', 137.5],
                          ['wr', 0.707]
                          ]
            tropismVector   = vector(0,0,0)
            tropismStrength = 0
        elif choice == 2: #simple tree 2
            axiom = "A(10,1)"
            productions = ["A(l,w)?!(w) F(l) [ &(a0) B(l*r2,w*wr) ] /(d) A(l*r1,w*wr)", 
                       "B(l,w)?!(w) F(l) [ -(a2) $ C(l*r2,w*wr) ] C(l*r1,w*wr)",
                       "C(l,w)?!(w) F(l) [ +(a2) $ B(l*r2,w*wr) ] B(l*r1,w*wr)"] 
            nrOfIterations = 10
            width = 1
            definitions = [['r1', 0.9],
                          ['r2', 0.7],
                          ['a0', 30],
                          ['a2', -30],
                          ['d', 137.5],
                          ['wr', 0.707]
                          ]
            tropismVector   = vector(0,0,0)
            tropismStrength = 0
        elif choice == 3: #phototropism
            axiom = "!(1) F(200) /(45) A"
            productions = ["A?!(vr) F(50) [ &(a) F(50) A ] /(d1) [ &(a) F(50) A ] /(d2) [ &(a) F(50) A ]", 
                           "F(l)?F(l*lr)",
                           "!(w)?!(w*vr)"] 
            nrOfIterations = 6
            width = 1 * 1.732 ** (nrOfIterations + 0.5)
            definitions = [['d1', 180],
                          ['d2', 252],
                          ['a', 36],
                          ['lr', 1.07],
                          ['vr', 1.732],
                          ] 
            tropismVector   = vector(0.61,0.77,-0.19)
            tropismStrength = 0.4
        else:
            print("That is not a valid choice, try again: ")
            continue

        ########### MAIN #############

        # Initialize
        scene = canvas(width = 1280, height = 720) #Make screen ready for visualisation	
        system = LSystem(axiom,productions, definitions = definitions) #Setup L-system

        # Compute the generations
        for i in range(nrOfIterations):
            tree = system.nextGeneration()

        #visualise the result
        turtle_interpretation_3D(scene, tree, delta = 22.5, width = width, widthScaling = 0.57, tropismVec = tropismVector, tropismStrength = tropismStrength)
        print("Press enter to exit animation: ")
        input()
        scene.delete()
    os._exit(0)
