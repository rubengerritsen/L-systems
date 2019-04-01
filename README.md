# L-systems

`LSystems.py` is a module for determenistic L-systems.
Everything from DOL-systems to parametric context-sensitive L-systems is covered.

The aim of this library is to provide an easy tool for L-system exploration. 
To this end, user input is kept very simple, while still allowing for very complex 
production rules. 

`LSystems_examples.py` is a module that illustrates the use of the LSystems module.
`LSystems_visualise.py` is a module for quick visualisations of some L-systems.

## What are L-systems:
For a quick intro into the world of L-systems see: 
*The Algorithmic Beauty Of Plants* by Przemyslaw Prusinkiewicz and Aristid Lindenmayer.
Almost all examples in the code are based on examples from this book.  
online: http://algorithmicbotany.org/papers/abop/abop.pdf

## How to use the LSystems module:
An L-system is defined by an axiom, a set of production rules and an optional ignore statement. Axioms and production rules are made up of *modules* (objects containing both the *letter/symbol* and the *parameters*). The axioms, production rules and ignore statement are all entered as strings.
##### Formatting the axioms and production rules
General formatting rules:
- Modules are seperated by spaces
- Parameters are seperated by commas
- Arrows are replaced by question marks

An example: the axiom B(2)CA(4,4) should be entered as `"B(2) C A(4,4)"` (C is a module with no parameters).
Production rules are of the following form: *left_context\<predecessor\>right_context:condition?successor*
If a certain part is not needed in the production rule it can be left out. For example a context free rule would be of the form *predecessor:condition?successor*. A production rule without context and condition would be *predecessor?succesor*. Note that **the successor is always preceded by a questionmark** and **the condition is always preceded by a colon**.

### Two examples
#### Koch's snowflake (simple L-system)
```python
# Specify the L-system
axiom = "F + + F + + F"
productions = ["F?F - F + + F - F"] 
nrOfIterations = 5
# Initialize
system = LSystem(axiom,productions)
# Generate the L-system generations
for j in range(0,nrOfIterations):
    gen = system.nextGeneration()
```
After visualisation that bit of code results in:
![alt text](https://github.com/RHJG/L-systems/blob/master/example1.PNG "Koch's snowflake")
for the use of the visualisation tools see: `LSystems_examples.py`
#### Anabaena catenula (complex L-system)
```python
# specify the L-system
axiom = "F(1,0,900) F(4,1,900) F(1,0,900)"
productions = ["F(s,t,c):t==1 and s>=6?F(s/3*2,2,c) f(1) F(s/3,1,c)",
               "F(s,t,c):t==2 and s>=6?F(s/3,2,c) f(1) F(s/3*2,1,c)",
               "F(h,i,k)<F(s,t,c)>F(o,p,r):(s>3.9 or c>0.4) and t!=0?F(s+0.1,t,c+0.25*(k+r-3*c))",
               "F(h,i,k)<F(s,t,c)>F(o,p,r):s<3.9 and c<0.4 and t!=0?F(1,0,900)",
               "F(s,t,c):t==0 and s<=3?F(s*1.1,t,c)"]
nrOfIterations = 200
ignore         = "f ~ H"
# Initialize
system = LSystem(axiom, productions,ignore)
# Generate the L-system generations
for j in range(0,nrOfIterations):
    gen = system.nextGeneration()
```
After visualisation that bit of code results in:
![alt text](https://github.com/RHJG/L-systems/blob/master/example2.PNG "Anabaena catenula")
on how to use the visualisation tools see: `LSystems_examples.py`

### Bonus:
In the jupyter notebook `3D Turtle Graphics + Application to L-systems.ipynb` an example of a 3D turtle applied to an L-system is presented.
A possible result:

![alt text](https://github.com/RHJG/L-systems/blob/master/example3.PNG "3D_tree")

## Acknowledgements
This project uses two modules from other authors. They are included here for completeness. It concerns the module `graphics.py` written by John Zelle and the module `py-expression-eval.py` written by Vera Mazhuga
