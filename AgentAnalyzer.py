# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 16:15:23 2022

@author: Patrick
"""

from os import listdir, getcwdb
from os.path import isfile, join

from AgentCode import AgentCode
from PlanGraph import PlanGraph

from tabulate import tabulate


class AgentAnalyzer:
    
    def __init__(self, files = [''], name = '', connectionBias = []):
        self.agentCode = AgentCode()
        self.loadAgent(files)
        self.name = name
        self.connectionBias = connectionBias
    
    def loadAgent(self, files = ['']):
        #agentFiles = self.getAgentFilePaths(files)
        
        
        for filePath in files:
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

        if len(agentFiles) < 1:
            raise FileNotFoundError('No agent files found')
        
        return agentFiles

    def getCouplingCohesionParameters(self):
        (triggers, plansPerTrigger) = self.getPlansPerEvent()
        (contextTriggers, contextMetrics) = self.getContextMetrics()
        (subGoalTriggers, subGoals) = self.getSubGoalList()

        return ((triggers, plansPerTrigger), (contextTriggers, contextMetrics), (subGoalTriggers, subGoals))

    
    # TODO: dig into this method
    def getContextMetrics(self):
        plans = self.agentCode.plans
        triggers = []
        contextMetrics = []
        
        for plan in plans:
            trigger = plan.trigger.functor
            contextMetric = plan.context.numExpressionsJoinedByConjunction()
            if not trigger in triggers:
                triggers.append(trigger)
                contextMetrics.append([contextMetric])
            else:
                i = triggers.index(trigger)
                contextMetrics[i].append(contextMetric)
        return (triggers, contextMetrics)                

        

    def getSubGoalList(self):
        plans = self.agentCode.plans
        triggers = []
        subGoals = []
        for plan in plans:
            trigger = plan.trigger.functor
            subGoals.append(plan.body.getSubGoals())
            
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
        plans = self.agentCode.plans
        triggers = set([plan.trigger.functor for plan in plans])
        ruleConclusions = [rule.conclusion for rule in self.agentCode.rules]
        planGraphs = [PlanGraph(trigger, plans, ruleConclusions, self.name) for trigger in triggers]
        return planGraphs
    
    def calculateCyclomaticComplexity(self, numNodes, numEdges, numConnectedComonenets):
        return numEdges - numNodes + (2 * numConnectedComonenets)
    
    def getAgentCyclomaticComplexity(self, planGraphs):
        triggers = []
        numEdges = []
        numNodes = []
        rulesUsed = []
        beliefsMaintained = []
        goalsUsed = []
        cyclomaticComplexity = []
        connectionBias = []
        connectedComponentsList = []
        for graph in planGraphs:
            triggers.append(graph.trigger)
            numEdges.append(graph.getNumEdges())
            numNodes.append(graph.getNumNodes())
            rulesUsed.append(graph.getRulesUsed())
            beliefsMaintained.append(graph.getBeliefsMaintained())
            goalsUsed.append(graph.getGoalsUsed())
            connectionBias.append(self.connectionBias)
            connectedComponents = len(graph.getGoalsUsed()) + len(graph.getBeliefsMaintained()) + len(graph.getRulesUsed()) + len(self.connectionBias)            
            connectedComponentsList.append(connectedComponents)
            cyclomaticComplexity.append(self.calculateCyclomaticComplexity(graph.getNumNodes(), graph.getNumEdges(), connectedComponents))
        return (triggers, numEdges, numNodes, rulesUsed, beliefsMaintained, goalsUsed, connectionBias, connectedComponentsList, cyclomaticComplexity)
    

    # TODO: Print a pretty report
    def printCouplingCohesionReport(self, couplingCohesion):
        ((triggers, plansPerTrigger), (_, contextMetrics), (_, subGoals)) = couplingCohesion
        rows = []
        while len(triggers) > 0:
            rows.append([triggers.pop(), plansPerTrigger.pop(), contextMetrics.pop(), subGoals.pop()])
        print('Coupling and Cohesion Report')
        headers = ['Triggers', 'PlansPerTrigger', 'contextMetrics', 'subGoals']
        print(tabulate(rows, headers = headers))
        self.saveReport(rows, headers, str(self.name) + '_CouplingCohesionReport')

    # TODO: Print a pretty report
    def printCyclomaticComplexityReport(self, complexity):
         (triggers, numEdges, numNodes, rulesUsed, beliefsMaintained, goalsUsed, connectionBias, connectedComponents, cyclomaticComplexity) = complexity
         rows = []
         while len(triggers) > 0:
             rows.append([triggers.pop(), numEdges.pop(), numNodes.pop(), 
                          rulesUsed.pop(), beliefsMaintained.pop(), 
                          goalsUsed.pop(), connectionBias.pop(), 
                          connectedComponents.pop(), cyclomaticComplexity.pop()]) 
         headers = ['triggers', 'numEdges', 'numNodes', 'rulesUsed', 
                   'beliefsMaintained', 'goalsUsed', 'connectionBias',
                                      'connectedComponents',
                                      'cyclomaticComplexity']
         print('Cyclomatic Complexity Report')
         print(tabulate(rows, headers = headers))
         self.saveReport(rows, headers, str(self.name) + '_CyclomaticComplexity')

    def printReport(self, couplingCohesion, complexity):
        print('--- Agent analysis Report: ' + self.name + ' version ---')
        self.printCouplingCohesionReport(couplingCohesion)
        self.printCyclomaticComplexityReport(complexity)
        
        
    def saveReport(self, rows, headdings, fileName):
        import csv
        with open('output/' + fileName + '.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', 
                                    quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(headdings)
            for row in rows:
                spamwriter.writerow(row)



    def analyze(self):
        metrics = self.getCouplingCohesionParameters()
        graphs = self.getNodeGraphs()
        complexity = self.getAgentCyclomaticComplexity(graphs)
        self.printReport(metrics, complexity)
        