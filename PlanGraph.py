# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 21:33:35 2022

@author: Patrick
"""

import graphviz



class PlanGraph:
    def __init__(self, trigger, plans, ruleConclusions):

        self.FIRST_NODE_ID = 0
        self.EXIT_NODE_ID = -1        
        
        self.trigger = trigger
        self.plans = [plan for plan in plans if plan.trigger.functor == trigger]
        self.connectedComponents = ruleConclusions
        
        self.buildGraph()
      
        
    # TODO DEBUG THIS METHOD!!!!!
    def buildGraph(self):
        dot = graphviz.Digraph(comment = self.trigger)
        
        nodeID = self.FIRST_NODE_ID
        dot.node(str(nodeID), self.trigger)
        dot.node(str(self.EXIT_NODE_ID),'Plan Exit')
        
        for plan in self.plans:
            newPlan = True
            if len(plan.body.steps) > 0:
                for step in plan.body.steps:
                    nodeID += 1
                    
                    if self.trigger in step:
                        dot.edge(str(nodeID - 1), str(self.FIRST_NODE_ID), constraint = 'false')
                        
                    else:
                        dot.node(str(nodeID), step)
                        if newPlan:
                            dot.edge(str(self.FIRST_NODE_ID), str(nodeID))
                        else:
                            dot.edge(str(nodeID - 1), str(nodeID), constraint = 'false')
            
                    dot.edge(str(nodeID), str(self.EXIT_NODE_ID))
                    
            else: # Empty plan body case
                dot.edge(str(self.FIRST_NODE_ID), str(self.EXIT_NODE_ID))
            newPlan = False
                
        # Handle belief triggered plan - where it is possible to go straight to the plan exit if not applicable
        if not '!' in self.trigger and not '?' in self.trigger:
            dot.edge(str(self.FIRST_NODE_ID), str(self.EXIT_NODE_ID))
        
        self.graph = dot

        print(dot.source)

        dot.render('doctest-output/round-table.gv', view=True)