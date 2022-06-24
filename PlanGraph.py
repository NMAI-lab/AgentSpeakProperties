# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 21:33:35 2022

@author: Patrick
"""

import graphviz



class PlanGraph:
    def __init__(self, trigger, plans, ruleConclusions, name):

        self.name = name        
        self.numNodes = 0
        self.numEdges = 0        

        self.FIRST_NODE_ID = 0
        self.EXIT_NODE_ID = -1        
        
        self.trigger = trigger
        self.plans = []
        for plan in plans:
            if trigger in plan.trigger.functor:
                self.plans.append(plan)
        
        
        self.rulesAvailable = ruleConclusions
        self.buildGraph()
      
        #self.printGraph()
        self.saveGraph()
    
    
    def getGoalsUsed(self):
        goalsUsed = set([])
        for plan in self.plans:
            subGoals = plan.body.getSubGoals()
            for subGoal in subGoals:
                goalsUsed.add(subGoal.split('(')[0])
        goalsUsed.discard(self.trigger)
        return goalsUsed

    def getBeliefsMaintained(self):
        beliefsMaintained = set([])
        for plan in self.plans:
            for step in plan.body.steps:
                if '+' in step or '-' in step:
                    if not '!' in step and not '?' in step:
                        belief = step.split('(')[0]
                        belief = belief.replace('+','')
                        belief = belief.replace('-','')
                        beliefsMaintained.add(belief)
        return beliefsMaintained
    
    def getRulesUsed(self):
        rulesUsed = set([])
        for rule in self.rulesAvailable:
            for plan in self.plans:
                if rule.functor in plan.context.parameters:
                    rulesUsed.add(rule.functor)
        return rulesUsed
    
    def addNode(self, nodeID, name):
        self.graph.node(str(nodeID), name)
        self.numNodes += 1

    def addEdge(self, a, b):
        self.graph.edge(str(a), str(b))
        self.numEdges += 1
        
    def getNumNodes(self):
        return self.numNodes
    
    def getNumEdges(self):
        return self.numEdges
    
    # Need to count the edges, nodes, and connected components as I build the graph
    
    def buildGraph(self):
        self.graph = graphviz.Digraph(comment = self.trigger)
        self.nodeID = self.FIRST_NODE_ID
        self.addNode(self.nodeID, self.trigger)
        self.addNode(self.EXIT_NODE_ID,'Plan Exit')
        if (not '!' in self.trigger) and (not '?' in self.trigger):
            self.addEdge(self.FIRST_NODE_ID, self.EXIT_NODE_ID)
               
        for plan in self.plans:
            self.addPlanToGraph(plan)

            

    def addPlanToGraph(self, plan):
        firstStep = True
        needExit = True
               
        if len(plan.body.steps) > 0:
            for step in plan.body.steps:                
                if len(step) > 0:
                    self.nodeID += 1
                    if self.trigger in step:
                        self.nodeID -= 1
                        if firstStep:
                            self.addEdge(self.FIRST_NODE_ID, self.FIRST_NODE_ID)
                        else:
                            self.addEdge(self.nodeID, self.FIRST_NODE_ID)
                        needExit = False
                        
                    else:
                        self.addNode(self.nodeID, step)
                    
                        if firstStep:
                            self.addEdge(self.FIRST_NODE_ID, self.nodeID)
                            firstStep = False
                        else:
                            self.addEdge(self.nodeID - 1, self.nodeID)
            
            if needExit:
                self.addEdge(self.nodeID, self.EXIT_NODE_ID)
                    
        else: # Empty plan body case
            self.addEdge(self.FIRST_NODE_ID, self.EXIT_NODE_ID)


    def printGraph(self):
        print(self.graph.source)
        
    def saveGraph(self,view=False):
        self.graph.render('output/' + str(self.name) + '_' + str(self.trigger) + '.gv', view=view)