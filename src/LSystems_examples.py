# -*- coding: utf-8 -*-
"""
Created on 2019-04-01

@author: R.H.J. Gerritsen

LSystems_examples.py illustrates the use of LSystems.py (and LSystems_visualise.py).
One can simply run 'run_test(number)' with a number in the range [1,7] to see one 
of the 7 test cases visualised with turtle graphics. For a more complex example and 
a more complex visualisation one can try 'run_Anabaena()' which shows the development 
of the bacteria Anabaena Catenula.


INSTALLATION: Put this file somewhere where Python can see it (e.g. in the 
              working directory.)

DEPENDENCIES: This module depends on LSystems.py and LSystems_visualise.py.
              Which depend respectively on py_expression_eval  and graphics.py

              py_expression_eval: https://github.com/Axiacore/py-expression-eval
              graphics:           https://mcsp.wartburg.edu/zelle/python/graphics.py

OVERVIEW:     This module contains a few examples that illustrate the use of LSystems.py
"""

from LSystems import *
from LSystems_visualise import *

def run_test(choice):
    """Given a choice for a case it will run the case and display the result."""
    ##############################
    #            CASES           #
    ##############################
    # DOL-systems
    ignore = ""
    if choice == 1: #Koch's snowflake
        # Specification of L-system
        nrOfIterations = 5
        axiom = "F + + F + + F"
        productions = ["F?F - F + + F - F"]        
        # For the visualization (optional)
        turtleDraw = True
        delta = 60
        initial = 0
    elif choice == 2: #Dragon curve
        # Specificaton of L-system
        nrOfIterations = 13
        axiom = "Fl"
        productions = ["Fl?Fl + Fr +", 
                       "Fr?- Fl - Fr"]
        # For the visualization (optional)
        turtleDraw = True
        delta = 90
        initial = 0
    elif choice == 3: #Islands and lakes
        # Specificaton of L-system
        nrOfIterations = 3
        axiom = "F + F + F + F"
        productions = ["F?F + f - F F + F + F F + F f + F F - f + F F - F - F F - F f - F F F",
                       "f?f f f f f f"]
        # For the visualization (optional)
        turtleDraw = True
        delta = 90
        initial = 0        
    # Bracketed DOL-system
    elif choice == 4: #Plant
        # Specification of L-system
        nrOfIterations = 2
        axiom = "F"
        productions = ["F?F F - [ - F + F + F ] + [ + F - F - F ]"]
        # for the visualization (optional)
        turtleDraw = True
        delta = 22.5
        initial = 90        
    # Parametric DOL-system
    elif choice == 5: #Triangle filling curve
        # Specification of L-system
        axiom = "F(1,0)"
        productions = ["F(x,t):t==0?F(x*0.3,2) + F(x*0.458,1) - - F(x*0.458,1) + F(x*0.7,0)",
                    "F(x,t):t>0?F(x,t-1)"]
        nrOfIterations = 10
        # for the visualization (optional)
        turtleDraw = True
        delta = 86
        initial = 0
    elif choice == 6: #Splitting tree
        # Specification of L-system
        axiom = "A(1)"
        productions = ["A(s)?F(s) [ + A(s/1.456) ] [ - A(s/1.456) ]"]
        nrOfIterations = 10
        # for the visualization (optional)
        turtleDraw = True
        delta = 85
        initial = 90
    elif choice == 7: #splitting tree with context
        # Specification of L-system
        axiom = "F 1 F 1 F 1"
        productions = ["0<0>0?1",
                       "0<0>1?1 [ - F 1 F 1 ]",
                       "0<1>0?1",
                       "0<1>1?1",
                       "1<0>0?0",
                       "1<0>1?1 F 1",
                       "1<1>0?1",
                       "1<1>1?0",
                       "+?-",
                       "-?+"]
        ignore   = "+-F"
        nrOfIterations = 30
        # for the visualization (optional)
        turtleDraw = True
        delta = 22.5
        initial = 90    
    elif choice == 8: #stochastic branching
        axiom = "F"
        productions = ["F?0.33;F [ + F ] F [ - F ] F;0.33;F [ + F ] F;0.34;F [ - F ] F"]
        nrOfIterations = 5
        # for the visualization
        turtleDraw = True
        delta = 23
        initial = 90
    ##############################
    #            MAIN            #
    ##############################
    
    # Setup/Initialize
    system = LSystem(axiom, productions,ignore)

    # Generate the L-system
    for j in range(0,nrOfIterations):
        gen = system.nextGeneration()
        
    # Visualise the result
    if turtleDraw == True:
        turtle_interpretation(gen,delta,initial)
    else:
        printGeneration(gen) 
        
def run_Anabaena():
    # System specification 
    axiom = "F(1,0,900) F(4,1,900) F(1,0,900)"
    productions = ["F(s,t,c):t==1 and s>=6?F(s/3*2,2,c) f(1) F(s/3,1,c)",
                   "F(s,t,c):t==2 and s>=6?F(s/3,2,c) f(1) F(s/3*2,1,c)",
                   "F(h,i,k)<F(s,t,c)>F(o,p,r):(s>3.9 or c>0.4) and t!=0?F(s+0.1,t,c+0.25*(k+r-3*c))",
                   "F(h,i,k)<F(s,t,c)>F(o,p,r):s<3.9 and c<0.4 and t!=0?F(1,0,900)",
                   "F(s,t,c):t==0 and s<=3?F(s*1.1,t,c)"]
    nrOfIterations = 200
    ignore         = "f ~ H"
    
    #Setup/Initialize
    visualisation = Anabaena(50,50,20)
    system = LSystem(axiom, productions,ignore)

    # Generate the L-system
    for j in range(0,nrOfIterations):
        gen = system.nextGeneration()
        if j%5 == 0: #display every 5th generation
            visualisation.drawGeneration(gen,newLineDistance = 22)
    
    visualisation.done() #closes visualisation on mouseclick
    
if __name__ == "__main__":
    user_input = ""
    print("")
    print("Welcome to the examples of the LSystems.py module:")
    print("")
    print("Select one of the following cases by entering the corresponding number.")
    print("To exit a visualisation simply click in the center of the image.")
    print("To exit the program simply type 'exit' and press enter.")
    print("")
    print("CASES:")
    print("{:5} {:<5} {:<25} {:<22}".format("", "0)", "Anabaena catenula", "Parametric 2L-system"))
    print("{:5} {:<5} {:<25} {:<22}".format("", "1)", "Koch's snowflake", "DOL-system"))
    print("{:5} {:<5} {:<25} {:<22}".format("", "2)", "Dragon curve", "DOL-system"))
    print("{:5} {:<5} {:<25} {:<22}".format("", "3)", "Islands and lakes", "DOL-system"))
    print("{:5} {:<5} {:<25} {:<22}".format("", "4)", "Simple plant", "Bracketed DOL-system"))
    print("{:5} {:<5} {:<25} {:<22}".format("", "5)", "Triangle filling curve", "Para. DOL-system"))
    print("{:5} {:<5} {:<25} {:<22}".format("", "6)", "Filling curve (tree)", "Para.Bra. DOL-system"))
    print("{:5} {:<5} {:<25} {:<22}".format("", "7)", "Plant", "Bracketed 2L-system"))
    print("{:5} {:<5} {:<25} {:<22}".format("", "8)", "Plant", "Stochastic DOL-system"))
    while user_input != "exit":
        user_input = input("Enter case as a number or type 'exit' to close: ")
        if user_input == "exit":
                break
        try:
            val = int(user_input)
            print("Running case: ", val)
        except ValueError:
            print("That is not a valid choice, try again: ")
            continue #start again at the top of the while loop
        if val == 0:
            print("An example of L-systems applied to the development of Anabaena catenula.")
            run_Anabaena()
        elif val < 9:
            run_test(val)
        else:
            print("That is not a valid choice, try again: ")