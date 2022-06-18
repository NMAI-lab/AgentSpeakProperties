# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 16:15:23 2022

@author: Patrick
"""

from os import listdir, getcwdb
from os.path import isfile, join

import ply.lex as lex

from AgentCode import AgentCode


class AgentAnalyzer:
    
    def __init__(self, path = ''):
        self.agentCode = AgentCode()
        self.loadAgent(path)
    
    def loadAgent(self, path = ''):
        print('Loading agent code')
        agentFiles = self.getAgentFilePaths(path)
        
        
        for filePath in agentFiles:
            with open(filePath, 'r') as file:
                self.agentCode.addCode(file.read())

        
    def getAgentFilePaths(self, path = ''):
        if len(path) <= 0:
            path = getcwdb()
           
        fileList = [f for f in listdir(path) if isfile(join(path, f))]
        agentFiles = []
        if not path.endswith('/'):
            path = path + '/'
        for file in fileList:
            if str(file).endswith('.asl'):
                agentFiles.append(path + file)
        print(agentFiles)

        if len(agentFiles) < 1:
            raise FileNotFoundError('No agent files found')
        
        return agentFiles

    def getCouplingCohesionParameters(self):
        (triggers, plansPerTrigger) = self.getPlansPerEvent()
        (contextTriggers, contextMetrics) = self.getContextMetrics()
        (subGoalTriggers, subGoals) = self.getSubGoalList()

        return ((triggers, plansPerTrigger), (contextTriggers, contextMetrics), (subGoalTriggers, subGoals))

    def getContextMetrics(self):
        plans = self.agentCode.plans
        triggers = []
        contextMetrics = []
        
        for plan in plans:
            trigger = plan.trigger
            contextMetric = plan.context.numExpressionsJoinedByConjunction()
            if not trigger in triggers:
                triggers.append(trigger)
                contextMetrics.append([contextMetric])
            else:
                i = triggers.index(trigger)
                contextMetrics[i].append(contextMetric)
        return (triggers, contextMetric)                
        

        

    def getSubGoalList(self):
        plans = self.agentCode.plans
        triggers = []
        subGoals = []
        for plan in plans:
            trigger = plan.trigger
            subGoals = plan.body.getSubGoals()
            
            if not trigger in triggers:
                triggers.append(trigger)
                subGoals.append(plan.body.getSubGoals())
            else:
                i = triggers.index(trigger)
                currentGoals = subGoals[i]
                
                for goal in subGoals:
                    if not goal in currentGoals:
                        currentGoals.append(goal)
        return (triggers, subGoals)
                
                    
            

        
    def getPlansPerEvent(self):
        plans = self.agentCode.plans
        triggerList = []
        useList = []
        for plan in plans:
            triggerFunctor = plan.trigger.functor
            if triggerFunctor in triggerList:
                i = triggerList.index(triggerFunctor)
                useList[i] = useList[i] + 1
            else:
                triggerList.append(triggerFunctor)
                useList.append(1)
        return(triggerList,useList)
            
    
    def getNodeGraphs(self):
        print('Get node graphs')
    
        print('Save node graphs')
    
    def getAgentCyclomaticComplexity(self):
        print('Get cyclomatic complexity metric')
        return 0
    

    
    def printReport(self, couplingCohesion, complexity):
        print('--- Agent analysis Report ---')
        print('Coupling and Cohesion: ' + str(couplingCohesion))
        print('Cyclomatic Complexity: ' + str(complexity))

    def analyze(self):
        metrics = self.getCouplingCohesionParameters()
        self.getNodeGraphs()
        complexity = self.getAgentCyclomaticComplexity()
        self.printReport(metrics, complexity)
        