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
  'NUMBER',
  'PLUS',
  'MINUS',
  'TIMES',
  'DIVIDE',
  'LPAREN',
  'RPAREN',
)
 
def MyLexer():
    # Regular expression rules for simple tokens
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
    t_DIVIDE  = r'/'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
 
    # A regular expression rule with some action code
    def t_NUMBER(t):
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