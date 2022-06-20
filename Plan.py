# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 14:56:46 2022

@author: Patrick
"""

class Plan:
    
    def __init__(self,raw):
        raw = raw.replace(' ','')
        raw = raw.replace('\t','')
        raw = raw.replace('\n','')
        
        self.setTrigger(raw)
        self.setContext(raw)
        self.setBody(raw)
        
        
    def setTrigger(self,raw):
        if ':' in raw:
            self.trigger = Trigger(raw.split(':') [0])
        elif '<-' in raw:
            self.trigger = Trigger(raw.split('<-') [0])
        else:
            self.trigger = Trigger(raw.split('.') [0])
        
    def setContext(self,raw):
        if ':' in raw:
            rawContext = raw.split(':')[1]
            if '<-' in rawContext:
                rawContext = rawContext.split('<-')[0]
        else:
            rawContext = ''
        self.context = Context(rawContext)
            

    def setBody(self,raw):
        if '<-' in raw:
            self.body = Body(raw.split('<-') [1])
        else:
            self.body = Body('')
            

class Trigger:
    def __init__(self,raw):
        self.functor = raw.split('+')[1]
        bracketSplit = self.functor.split('(')
        
        self.functor = bracketSplit[0]
        
        self.parameterList = []
        if len(bracketSplit) > 1:
            parameters = raw.split('(')[1]
            parameters = parameters.split(')')[0]
            self.parameterList = parameters.split(',')
            
class Context:
    def __init__(self,raw):
        self.parameters = raw
        
    def numExpressionsJoinedByConjunction(self):
        if len(self.parameters) > 0:
            if '&' in self.parameters:
                return len(self.parameters.split('&'))
            else:
                return 1
        else:
            return -1    
        
class Body:
    def __init__(self,raw):
        self.steps = []
        
        raw = raw.replace(';}','};')
        
        if len(raw) == 0:
            steps = ''
        elif ';' in raw:
            steps = raw.split(';')
        else:
            steps = [raw]
        
        # Drop last period
        if len(steps) > 0:
            lastStep = steps[len(steps)-1]
            lastStep = lastStep[:-1]
            steps[len(steps)-1] = lastStep

            for step in steps:
                if not('.broadcast' in step) and len(step) > 0:
                    self.steps.append(step)
        else:
            self.steps = ['']
        
            
        

    def getSubGoals(self):
        subGoals = []
        for step in self.steps:
            if '!' in step or '?' in step:
                subGoal = step.split('(')[0]
                if not subGoal in subGoals:
                    subGoals.append(step)
        return subGoals   