# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 12:03:37 2022

@author: Patrick
"""

import ply.yacc as yacc
import ply.lex as lex
 
# Get the token map from the lexer.  This is required.
#from calclex import tokens

rawInput = '+trigger(TriggerValue) : context(ContextValue) <- action(3).'

 
# List of token names.   This is always required
tokens = (
  'integer',
  'plus',
  'minus',
  'times',
  'divide',
  #'exp',
  #'div',
  #'mod',
  'parenLeft',
  'parenRight',
  'bracketLeft',
  'bracketRight',
  'exclamation',
  'question',
  'colon',
  'period',
  'arrow',
  'implication',
  'text',
  'capital'
)
 
def MyLexer():
    # Regular expression rules for simple tokens
    t_plus = r'\+'
    t_minus = r'-'
    t_times = r'\*'
    t_divide = r'\/'
    #t_exp = r'\**'
    #t_div = r'\div',
    #t_mod = r'\mod',
    t_parenLeft = r'\('
    t_parenRight = r'\)'
    t_bracketLeft = r'\['
    t_bracketRight = r'\]'
    t_exclamation = r'\!'
    t_question = r'\?'
    t_colon = r'\:'
    t_period= r'\.'
    t_arrow = r'\<-'
    t_implication = r'\:-'
    t_text = r'[a-zA-Z]+'
    t_capital = r'[A-Z]'



    def t_integer(t):
        r'\d+'
        t.value = int(t.value)    
        return t

    # Define a rule so we can track line numbers
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)
 
    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'
 
    # Error handling rule
    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)
 
    # Build the lexer from my environment and return it    
    return lex.lex()


lexer = MyLexer()
#lexer.input(rawInput)
#for tok in iter(lex.token, None):
#    print(repr(tok.type), repr(tok.value))
    
    
#class Plan(object):
#    def __init__(self, symbol, count):
#        self.symbol = symbol
#        self.count = count
#   def __repr__(self):
#        return "Plan(%r, %r)" % (self.symbol, self.count)

#def p_term_div(p):
#    'term : term divide factor'
#    p[0] = p[1] / p[3]
    
#def p_factor_num(p):
#    'factor : number'
#    p[0] = p[1]
    
#def p_term_factor(p):
#     'term : factor'
#     p[0] = p[1]
     
class Goal(object):
    def __init__(self, otherGoal):
        self.goalName = otherGoal.goalName
        self.goalType = otherGoal.goalType
    
    def __init__(self, goalType, goalName):
        self.goalType = goalType 
        self.goalName = goalName
    def __repr__(self):
        return "Goal: (%r %r)" % (self.goalType, self.goalName)

class Rule(object):
    def __init__(self, conclusion, condition):
        self.conclusion = conclusion 
        self.condition = condition
    def __repr__(self):
        return "Rule: %r implied by %r" % (self.conclusion, self.condition)
    
class Plan(object):
    def __init__(self, goal, context, body):
        self.goal = goal
        self.context = context
        self.body = body
    def __repr__(self):
        return "Plan \n %r \n Plan Context: %r \n Plan Body: %r \n" % (self.goal, self.context, self.body)

class Predicate(object):
    def __init__(self, functor, parameters):
        self.functor = functor
        self.parameters = parameters
    def __repr__(self):
        return "Predicate: %r (%r)" % (self.functor, self.parameters)
    
#class (object):
#    def __init__(self, conclusion, condition):
#        self.conclusion = conclusion 
#        self.condition = condition
#    def __repr__(self):
#        return "Rule: %r implied by %r" % (self.conclusion, self.condition)


def p_term_text(p):
    'term : text'
    p[0] = str(p[1])
    

def p_goal(p):
    '''goal  : exclamation text
             | question text'''
    p[0] = Goal(str(p[1]), str(p[2]))

def t_predicate(p):
    'term : text parenLeft text parenRight'
    p[0] = Predicate(p[1],p[3])
    
    
def p_rule(p):
    'term : text implication text period'
    p[0] = Rule(p[1],p[3])
    

def p_plan(p):
    '''
    term : goal colon text arrow text period
    '''
    
    p[0] = Plan(p[1], p[3], p[5])
    

def p_arithmExpressionTerm(p):
    'term : arithmExpression'
    p[0] = str(p[1])
 
    
 
# TODO: Think about what I really need: I need to identify:
#   achievement goal functors
#   Terms in logical expressions
#   number of concerns
#   number of connected components
#   number of steps in a plan body
# I DON't NEED THE WHOLE EBNF FOR THAT
    
 
# TODO: Think about how to represent this behind the scenes - if there are variables I can't run the math so I have to store it as such

#def p_arithmExpression(p):
#    '''arithmExpression : arithmTerm plus arithmTerm
#                        | arithmTerm minus arithmTerm
#                        | arithmTerm times arithmTerm
#                        | arithmTerm divide arithmTerm
#                        | arithmTerm exp arithmTerm
#                        | arithmTerm div arithmTerm
#                        | arithmTerm mod arithmTerm'''
#                        
#    if p[2] == '+':
#        p[0] = p[1] + p[3]
#    elif p[2] == '-':
#        p[0] = p[1] - p[3]

def p_arithmExpressionParen(p):
    '''arithmExpression : parenLeft arithmExpression parenRight
                        | arithmTerm'''
    if len(p) > 2:
        p[0] = str(p[2])
    else:
        p[0] = str(p[1])

#def p_termArithmTerm(p):
#    'term : arithmTerm'
#    p[0] = str(p[1])
    
def p_arithmTerm(p):
    '''arithmTerm   : variable
                    | number
                    | minus arithmTerm'''
                    #| parenLeft arithmExpression parenRight'''

    
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = 0 - float(p[2])
    else:
        p[0] = p[2]
    
    #if isinstance(p[1], int):
    #    p[0] = int(p[1])
    #else:
    #    p[0] = str(p[1])


def p_term_variable(p):
    'variable : capital'
    p[0] = str(p[1])
    

def p_term_varaibleLong(p):
    'variable : capital text'
    p[0] = str(p[1]) + str[p[2]]
        

def p_number(p):
    '''number   : integer period integer
                | integer'''
    if len(p) > 2:
        fractional = float(p[3])
        while abs(fractional) >= 1.0:
            fractional = fractional / 10.0
        p[0] = float(p[1]) + fractional
    else:
        p[0] = int(p[1])
        

    
def p_error(p):
    raise TypeError("unknown text at %r" % (p.value,))
    
    
    
#def p_word_letterLower(p):
#    'word : t_letterLower'
#    p[0] = str(p[1])
         
#def p_binary_operators(p):
#    '''expression : expression '+' term
#                  | expression '-' term
#       term       : term '*' factor
#                  | term '/' factor'''
#    if p[2] == '+':
#        p[0] = p[1] + p[3]
#    elif p[2] == '-':
#        p[0] = p[1] - p[3]
#    elif p[2] == '*':
#        p[0] = p[1] * p[3]
#    elif p[2] == '/':
#        p[0] = p[1] / p[3]
        
    
    
yacc.yacc()
#print(yacc.parse("!ab"))
#print(yacc.parse('!ab : meow <- cat.'))
#print(yacc.parse('conc :- cond.'))
print(yacc.parse('functor(parameter)'))
#print(yacc.parse("V"))
#print(yacc.parse("Variable"))
#print(yacc.parse("-4.126485431"))
#print(yacc.parse("4.126485431"))

#print(yacc.parse("-(-4.126485431)"))
#print(yacc.parse("5 + 10"))

