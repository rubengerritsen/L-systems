# -*- coding: utf-8 -*-
"""
Created on 2019-04-01

@author: R.H.J. Gerritsen

LSystems.py is a module for L-systems.
Everything from DOL-systems to parametric 2L-systems is covered,
also stochastic production rules are supported.

The aim of this library is to provide an easy tool for L-system exploration. 
To this end, user input is kept very simple, while still allowing for very complex 
production rules. 

The language used to describe L-systems here is based on the language used in the book:
'The Algorithmic Beauty of Plants' by Przemyslaw prusinkiewicz &  Aristid Lindenmayer

For examples please refer to LSystems_examples.py

INSTALLATION: Put this file somewhere where Python can see it (e.g. in the 
			  working directory.)

DEPENDENCIES: This library heavily depends on the py_expression_eval module 
              by Vera Mazhuga. Which can be downloaded from:
              https://github.com/Axiacore/py-expression-eval
              Further, we only need regular expressions from re.

OVERVIEW:     This module consists of the classes: Module, Rule and LSystem.
              Module is used to store modules (a letter/symbol and its parameters)
              Rule is used to contain production rules and methods to determine
              if the rule is applicable and what the replacement (successor) is.
              LSystem is the class that represent the actual L-system.

              Besides the classes there are a lot of functions for parsing string input
              to useable axioms and production rules. 

              Thereafter, we have some functions for finding context and finally
              some auxiliary functions (e.g. for printing output, debugging etc.).

"""

import re     
from py_expression_eval import Parser
from random import random

########################################
#               CLASSES                #
########################################

class Module:
    """Module is a word in the alphabet together with its parameters.
    
    symbol is a string that represents the symbol.
    param is a list containing all parameters (either symbolic or numeric)
    An example:  A(2,3) implies symbol = "A" and param = [2,3]
    If a module has no parameters: param = []
    """
    def __init__(self, symbol, param = []):
        self.symbol = symbol
        self.param = param


class Rule:
    """Rule represents a replacement rule with its predecessor, condition and successor.

	Rule can contain any type of production rule. The type is indicated by a number.
	If a rule does not use left_context or right_context an empty module can be passed. 
	The condition can be given as a string. The successor is a list of replacement instructions.
    """
    def __init__(self, ruleType, left_context, predecessor, right_context, condition = "", successor = [], probs = []):
        # RuleTypes:
        self.TYPE_OL            = 0                    #context free rule
        self.TYPE_L1L           = 1                    #left context rule
        self.TYPE_R1L           = 2                    #right context rule
        self.TYPE_2L            = 3                    #left and right context rule      
        # assigning variables        
        self.ruleType           = ruleType                      
        self.parser             = Parser()
        self.predecessorSymbol  = predecessor.symbol   # the symbol of the predecessor
        self.symParam           = predecessor.param    # a list of symbolic representations of variables
        self.successor          = successor            # list of symbols and for every parameter an expression [[ "symbol",   [param]], [...]]  in case of stochastic a list of lists
        self.left_context       = left_context
        self.right_context      = right_context
        self.isStochastic       = (probs != []) 
        self.probs              = probs                # if stochastic then this contains a list of the probabilities
        # if the condition is non-empty parse it to an expression
        if condition != "":
            self.condition      = self.parser.parse(condition)  # the condition in string form
        else:
            self.condition      = condition
            
    def checkCondition(self, left_context, mod, right_context):
        """Checks whether the condition in the rule is true or false"""
        if self.condition == "":
            return(True)
        else:
            if self.ruleType == self.TYPE_OL:
                keys = self.symParam
                values = mod.param 
            elif self.ruleType == self.TYPE_L1L:
                keys = self.left_context.param + self.symParam
                values = left_context.param + mod.param     
            elif self.ruleType == self.TYPE_R1L:
                keys = self.symParam + self.right_context.param
                values =  mod.param + right_context.param
            elif self.ruleType == self.TYPE_2L:
                keys = self.left_context.param + self.symParam + self.right_context.param
                values = left_context.param + mod.param + right_context.param
            new_dict = dict(zip(keys,  values))       
            return(self.condition.evaluate(new_dict))
 

    def isApplicable(self, left_context, mod, right_context):
        """Check if this rule is applicable to mod."""    
        if self.predecessorSymbol != mod.symbol: 
            return(False)
        else:
            if self.ruleType == self.TYPE_OL:
                if self.checkCondition(left_context, mod, right_context):
                    return(True)
                else:
                    return(False)
            elif self.ruleType == self.TYPE_L1L:
                if self.checkCondition(left_context, mod, right_context) and self.left_context.symbol == left_context.symbol:
                    return(True)
                else:
                    return(False)
            elif self.ruleType == self.TYPE_R1L:
                if self.checkCondition(left_context, mod, right_context) and self.right_context.symbol == right_context.symbol:
                    return(True)
                else:
                    return(False)
            elif self.ruleType == self.TYPE_2L:
                if self.checkCondition(left_context, mod, right_context) and self.right_context.symbol == right_context.symbol and self.left_context.symbol == left_context.symbol:
                    return(True)
                else:
                    return(False)               
                           
    
    def getReplacement(self, left_context, mod, right_context, definitions):
        """Get the lists of modules that should replace mod."""
        replacement = []
        if self.isStochastic:  #Choose a rule
            choice = random()
            cumulative = 0
            for i in range(0,len(self.probs)):
                cumulative += self.probs[i]
                if cumulative > choice:
                    index = i
                    break
            currentRule = self.successor[index]
        else:
            currentRule = self.successor
        #Now convert the rule into a list of replacement modules
        for elem in currentRule:
            #generate replacement dictionary
            if self.ruleType == self.TYPE_OL:
                keys = self.symParam
                values = mod.param 
            elif self.ruleType == self.TYPE_L1L:
                keys = self.left_context.param + self.symParam
                values = left_context.param + mod.param     
            elif self.ruleType == self.TYPE_R1L:
                keys = self.symParam + self.right_context.param
                values =  mod.param + right_context.param
            elif self.ruleType == self.TYPE_2L:
                keys = self.left_context.param + self.symParam + self.right_context.param
                values = left_context.param + mod.param + right_context.param
            if definitions != []: #this means there are named variables with a definition in that case we add them to the variables
                keys = keys + [item[0] for item in definitions]
                values = values + [item[1] for item in definitions]
            new_dict = dict(zip(keys,  values))
            params = []
            for i in range(0, len(elem.param)):
                parExpr = elem.param[i]
                params.append(parExpr.evaluate(new_dict))
            #add to replacement as a module
            replacement.append(Module(elem.symbol,params))
        return(replacement)

class LSystem:
    def __init__(self, axiom, productions,ignore = [], definitions = []):
        self.word = stringToAxiom(axiom)
        self.productionRules = []
        for line in productions:
        	self.productionRules.append(stringToRule(line))
        self.ignore = ignore
        self.definitions = definitions

    def nextGeneration(self):
        """Computes and returns the next generation as a list of modules. """
        new_word = []
        for i in range(0,len(self.word)):
            mod = self.word[i]
            left_context = findLeftContext(self.word, i, self.ignore)
            right_context = findRightContext(self.word, i, self.ignore)
            foundOne = False
            for rule in self.productionRules: #find an applicable rule
                if rule.isApplicable(left_context, mod, right_context):
                    new_word = new_word + rule.getReplacement(left_context, mod, right_context,self.definitions)
                    foundOne = True
                    break
            if not foundOne: #then no replacement will occur
                new_word = new_word + [mod]
        self.word = new_word 
        return(self.word)



########################################
#          PARSING FUNCTIONS           #
########################################
def stringToMod(string):
    """Parse a string, containing a single module with numeric parameters, to a module."""
    string = string.strip() 
    i = 0
    symbol = ""
    # read the symbol
    while i < len(string) and string[i] != "(":
        symbol = symbol + string[i]
        i = i + 1
    # if parameters are present, get them
    if i< len(string) and string[i] == "(":   
        i = i + 1 # skip the opening bracket
        params = string[i:(len(string) - 1)].split(",")
        for i in range(0,len(params)):
            params[i] = float(params[i].strip())
        return(Module(symbol,params))
    else:
        return(Module(symbol,[]))

def stringToSymMod(string):
    """Parse a string, containing a single module with symbolic parameters, to a module."""
    string = string.strip() #delete all surrounding whitespaces
    i = 0
    symbol = ""
    # read the symbol
    while i < len(string) and string[i] != "(":
        symbol = symbol + string[i]
        i = i + 1
    # if parameters are present, get them
    if i< len(string) and string[i] == "(":   # If true then parameters will follow, else we are done
        i = i + 1 # skip the opening bracket
        params = string[i:(len(string) - 1)].split(",")
        for i in range(0,len(params)):
            params[i] = params[i].strip()
        return(Module(symbol,params))
    else:
        return(Module(symbol,[]))
    
def stringToSymModWithExpr(string):
    """Parse a string, containing a single module with symbolic parameters, to a module with expressions for parameters."""
    parser = Parser()
    string = string.strip() #delete all surrounding whitespaces
    i = 0
    symbol = ""
    # read the symbol
    while i < len(string) and string[i] != "(":
        symbol = symbol + string[i]
        i = i + 1
    # if parameters are present, get them
    if i < len(string) and string[i] == "(":   # If true then parameters will follow, else we are done
        i = i + 1 # skip the opening bracket
        params = string[i:(len(string) - 1)].split(",")
        for i in range(0,len(params)):
            params[i] = parser.parse(params[i].strip())
        return(Module(symbol,params))
    else:
        return(Module(symbol,[]))

def stringToPredecessor(string):
    splitted = re.split("[<>]+", string)
    if len(splitted) == 3:
        rule_type = 3
        return(rule_type, [stringToSymMod(splitted[0]), stringToSymMod(splitted[1]), stringToSymMod(splitted[2])])
    elif len(splitted) == 2:
        if "<" in string:
            rule_type = 1
            return(rule_type, [stringToSymMod(splitted[0]), stringToSymMod(splitted[1]), emptyModule()])
        elif ">" in string:
            rule_type = 2
            return(rule_type, [emptyModule(), stringToSymMod(splitted[0]), stringToSymMod(splitted[1])])
        else:
            print("error in parsing string to predecessor")
    elif len(splitted) == 1:
        rule_type = 0
        return(rule_type, [emptyModule(), stringToSymMod(splitted[0]), emptyModule()])
    else:
        print("error in parsing string to predecessor")
        return(-1)   

def stringToSuccessor(string):
    if string.find(";") == -1: # Then: non-stochastic rule
        probs = []
        successor = []
        splitted = string.split(" ")
        for mod in splitted:
            successor.append(stringToSymModWithExpr(mod.strip()))
        return(probs, successor)
    else: # Stochastic rule
        probsAndRules = string.split(";")
        probs = probsAndRules[0::2]
        probs = list(map(float, probs))
        rules = probsAndRules[1::2]
        listOfSuccessors = []
        for i in range(0,len(probs)):
            successor = []
            splitted = rules[i].split(" ")
            for mod in splitted:
                successor.append(stringToSymModWithExpr(mod.strip()))
            listOfSuccessors.append(successor)
        return(probs, listOfSuccessors)

def stringToAxiom(string):
    """Takes an axiom as a string and converts it into a list of modules."""
    sentence = []
    splitted = string.split(" ")
    for mod in splitted:
        sentence.append(stringToMod(mod.strip()))
    return(sentence)

def stringToRule(string):
    """ Takes a rule in string form as input and converts it to a rule object. """
    productionRule = re.split("[?:]+", string)
    rule_type, predecessor = stringToPredecessor(productionRule[0])
    if len(productionRule) == 2:
        probs, successor = stringToSuccessor(productionRule[1])
        return(Rule(rule_type, predecessor[0], predecessor[1], predecessor[2], "", successor, probs))
    else:
        probs, successor = stringToSuccessor(productionRule[2])
        return(Rule(rule_type, predecessor[0], predecessor[1], predecessor[2], productionRule[1], successor, probs))

########################################
#             FIND CONTEXT             #
########################################
def findLeftContext(tree, start, ignore):
    """ Returns the left context of a module at position 'start' in a 'tree'.
    
    The function ignores every substring of 'ignore' in the search for left context.
    """	
    nrOfClosingBrs = 0
    nrOfOpeningBrs = 0
    firstPass = True
    for currentIndex in range(start-1,-1,-1):
        if tree[currentIndex].symbol in ignore:
            continue
        elif tree[currentIndex].symbol == "[":
            if not firstPass:
                nrOfOpeningBrs = nrOfOpeningBrs + 1
        elif tree[currentIndex].symbol == "]":
            nrOfClosingBrs = nrOfClosingBrs + 1
        elif nrOfClosingBrs == nrOfOpeningBrs:
            return(tree[currentIndex])
        firstPass = False
    return(emptyModule())

def findRightContext(tree,start,ignore):
    """ Returns the right context of a module at position 'start' in a 'tree'.
    
    The function ignores every substring of 'ignore' in the search for right context.
    
    The current implementation is based on the paper: 'Mathematical Models for Cellular Interactions in Development
    II. Simple and Branching Filaments with Two-sided Inputs' by ARISTID LINDENMAYER.
    In the paper they suggest to look only for right context on the main branch the current module is a part of. 
    Therefore inputs from side branches are ignored. This results in always finding 1 right context and not multiple.
    """
    nrOfClosingBrs = 0
    nrOfOpeningBrs = 0
    firstPass = True
    if start+1 < len(tree):
        for currentIndex in range(start+1,len(tree)):
            if tree[currentIndex].symbol in ignore:
                continue
            elif tree[currentIndex].symbol == "]":
                if firstPass:
                    return(emptyModule())
                else:
                    nrOfClosingBrs = nrOfClosingBrs + 1
            elif tree[currentIndex].symbol == "[":
                nrOfOpeningBrs = nrOfClosingBrs + 1
            elif nrOfOpeningBrs == nrOfClosingBrs:
                return tree[currentIndex]
            firstPass = False
    else:
        return(emptyModule())



########################################
#          AUXILIARY FUNCTIONS         #
########################################
def printListOfMods(tree):
    """Print a list of modules (tree), mostly useful for debugging.

    INPUT: list of modules
    """
    for mod in tree:
        print(mod.symbol, mod.param)  

def printGeneration(tree):
    """Prints the modules of a tree one after the other on the same line.

    INPUT: list of modules
    """
    for mod in tree:
        if mod.param != []:
            print(str(mod.symbol) + str(mod.param).replace("[","(").replace("]",")"),end="")
        else:
            print(str(mod.symbol),end="")
    print("")

def emptyModule():
    """ Returns an empty module."""
    return(Module("",[]))


if __name__ == "__main__":
    print("For examples refer to: LSystems_examples.py")