# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 09:44:04 2022

@author: Patrick
"""

from Plan import Plan
from Rule import Rule

class AgentCode:
    
    
    def __init__(self):
        self.code = ''
        self.plans = []
        self.rules = []
    
    def addCode(self, code):
        code = self.removeCommentBlocks(code)
        code = self.removeLineComments(code)
        code = self.removeIncludes(code)
        self.setPlans(code)
        self.setRules(code)
        self.code += '\n' + code
        
    def removeCommentBlocks(self, code):
        commentStartSplit = code.split('/*')
        cleanCode = commentStartSplit[0]    # Add anything before the first comment block
        
        for block in commentStartSplit:
            commentEndSplit = block.split('*/')
            if len(commentEndSplit) > 1:
                cleanCode += commentEndSplit[1]
            
        return cleanCode
        
    def removeLineComments(self, code):
        lines = code.split('\n')
        commentFreeCode = ''
        for line in lines:
            if not '//' in line:
                commentFreeCode = commentFreeCode + '\n' + line
            else:
                # Comment found, ignore everything after it
                cleanLine = line.split('//')[0]
                commentFreeCode = commentFreeCode + '\n' + cleanLine
        
        return commentFreeCode
    
    def removeDebugMessages(self,code):
        lines = code.split('\n')
        debugFreeCode = ''
        
        for line in lines:
            if '.broadcast' in line:
                if line.endswith('.'):
                    debugFreeCode = debugFreeCode + '.'
            else:
                debugFreeCode = debugFreeCode + '\n' + line
       
        return debugFreeCode
    
    
        
  
    def removeIncludes(self,code):
        cleanCode = ''
        lines = code.split('\n')
        for line in lines:
            if not '{ include' in line:
                cleanCode += '\n' + line
        return cleanCode
        
  
    def setPlans(self, code):
        lines = code.split('\n')
        
        inPlan = False
        for line in lines:
            if line.startswith('+'):
                inPlan = True
                planLine = ''
            
            if inPlan and len(line) > 0:
                planLine += line
                
                if line.replace(' ','').endswith('.'):
                    inPlan = False
                    self.plans.append(Plan(planLine))
    
    def setRules(self, code):
        lines = code.split('\n')
        
        inRule = False
        i = 0
        for line in lines:
            if ':-' in line:
                inRule = True
                if line.split(':-')[0].isspace():
                    ruleLine = lines[i-1]
                else:
                    ruleLine = ''                    
                    
            
            if inRule and len(line) > 0:
                ruleLine += line
                
                if line.replace(' ','').endswith('.'):
                    inRule = False
                    self.rules.append(Rule(ruleLine))
            i += 1
        
