# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 16:15:23 2022

@author: Patrick
"""

from os import listdir, getcwdb
from os.path import isfile, join

import ply.lex as lex


class AgentAnalyzer:
    
    def __init__(self, path = ''):
        self.agentCode = []
        self.loadAgent(path)
    
    def loadAgent(self, path = ''):
        print('Loading agent code')
        agentFiles = self.getAgentFilePaths(path)
        
        
        for filePath in agentFiles:
            with open(filePath, 'r') as file:
                self.agentCode.append(file.read())
        print(self.agentCode)
        
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

    def getCouplingCohesionMetrics(self):
        print('Get coupling and cohesion metrics')
        triggerList = self.getTriggerList()
    
    def getNodeGraphs(self):
        print('Get node graphs')
    
        print('Save node graphs')
    
    def getAgentCyclomaticComplexity(self):
        print('Get cyclomatic complexity metric')
        return 0
    
    def getTriggerList(self):
        triggers = []
        for codeBlock in self.agentCode:
            for line in codeBlock:
                if '+' in line:
                    triggers.append(line)
                    print(line)
        return triggers
    
    def printReport(self, couplingCohesion, complexity):
        print('--- Agent analysis Report ---')
        print('Coupling and Cohesion: ' + str(couplingCohesion))
        print('Cyclomatic Complexity: ' + str(complexity))

    def analyze(self):
        metrics = self.getCouplingCohesionMetrics()
        self.getNodeGraphs()
        complexity = self.getAgentCyclomaticComplexity()
        self.printReport(metrics, complexity)
        