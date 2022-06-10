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
  'number',
  'plus',
  'minus',
  'times',
  'divide',
  'parenLeft',
  'parenRight',
  'bracketLeft',
  'bracketRight',
  'exclamation',
  'colon',
  'period',
  'arrow',
  'implication',
  'text',
)
 
def MyLexer():
    # Regular expression rules for simple tokens
    t_plus = r'\+'
    t_minus = r'-'
    t_times = r'\*'
    t_divide = r'\/'
    t_parenLeft = r'\('
    t_parenRight = r'\)'
    t_bracketLeft = r'\['
    t_bracketRight = r'\]'
    t_exclamation = r'\!'
    t_colon = r'\:'
    t_period= r'\.'
    t_arrow = r'\<-'
    t_implication = r'\:-'
    t_text = r'[a-zA-Z]+'


    # A regular expression rule with some action code
    def t_number(t):
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
    

def p_term_text(p):
    'term : text'
    p[0] = str(p[1])
    
def p_term_achievementGoal(p):
    'term : exclamation text'
    p[0] = Goal(str(p[1]), str(p[2]))
    
def p_term_rule(p):
    'term : text implication text period'
    p[0] = Rule(p[1],p[3])
        
    
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
goalTest = yacc.parse("!ab")
print(goalTest)
ruleTest = yacc.parse("conc :- cond.")
print(ruleTest)

