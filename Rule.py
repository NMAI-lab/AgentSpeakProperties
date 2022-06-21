# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 16:14:14 2022

@author: Patrick
"""

class Rule:
    def __init__(self,raw):
        raw = raw.replace(' ','')
        raw = raw.replace('\t','')
        raw = raw.replace('\n','')
        self.conclusion = Conclusion(raw.split(':-')[0])
        self.condition = raw.split(':-')[1]
        self.condition = self.condition[:-1]
        
class Conclusion:
    def __init__(self,raw):
        bracketSplit = raw.split('(')
        
        self.functor = bracketSplit[0]
        
        self.parameterList = []
        if len(bracketSplit) > 1:
            parameters = raw.split('(')[1]
            parameters = parameters.split(')')[0]
            self.parameterList = parameters.split(',')