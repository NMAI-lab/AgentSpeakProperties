# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 16:15:23 2022

@author: Patrick
"""

class AgentAnalyzer:
    
    def __init__(self, path = ''):
        self.agentCode = self.loadAgent(path)
    
    def loadAgent(self, path = ''):
        print('Loading agent code')
        return 0

    def getCouplingCohesionMetrics(self):
        print('Get coupling and cohesion metrics')
    
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
        metrics = self.getCouplingCohesionMetrics()
        self.getNodeGraphs()
        complexity = self.getAgentCyclomaticComplexity()
        self.printReport(metrics, complexity)
        