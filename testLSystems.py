
from LSystems import *
from LSystems_visualise import *       
import time

t0 = time.time()

nrOfIterations = 8
axiom = "F + + F + + F"
productions = ["F?F - F + + F - F"]        
# For the visualization (optional)
turtleDraw = True
delta = 60
initial = 0

##############################
#            MAIN            #
##############################

# Setup/Initialize
system = LSystem(axiom, productions)

# Generate the L-system
for j in range(0,nrOfIterations):
    gen = system.nextGeneration()
    
# Visualise the result
# if turtleDraw == True:
#     turtle_interpretation(gen,delta,initial)


print("It took:" , time.time()-t0)