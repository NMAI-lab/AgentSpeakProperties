# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 16:15:23 2022

@author: Patrick
"""

from AgentAnalyzer import AgentAnalyzer

def analyze():
    path = 'C:/Users/Patrick/Documents/GitHub/AirSimNavigatingCar/asl/AgentInABox'
    analyzer = AgentAnalyzer(path)
    analyzer.analyze()

if __name__ == '__main__':
    analyze()
    
    