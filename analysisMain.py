# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 16:15:23 2022

@author: Patrick
"""

from AgentAnalyzer import AgentAnalyzer

def analyze():
    aib = ['C:/Users/Patrick/Documents/GitHub/AirSimNavigatingCar/asl/AgentInABox/steeringController.asl',
                  'C:/Users/Patrick/Documents/GitHub/AirSimNavigatingCar/asl/AgentInABox/carController.asl',
                  'C:/Users/Patrick/Documents/GitHub/AirSimNavigatingCar/asl/AgentInABox/a_star.asl',
                  'C:/Users/Patrick/Documents/GitHub/AirSimNavigatingCar/asl/AgentInABox/driveTowardController.asl',
                  'C:/Users/Patrick/Documents/GitHub/AirSimNavigatingCar/asl/AgentInABox/map.asl',
                  'C:/Users/Patrick/Documents/GitHub/AirSimNavigatingCar/asl/AgentInABox/obstacleAvoidStopper.asl',
                  'C:/Users/Patrick/Documents/GitHub/AirSimNavigatingCar/asl/AgentInABox/positioningRules.asl',
                  'C:/Users/Patrick/Documents/GitHub/AirSimNavigatingCar/asl/AgentInABox/speedController.asl']
    agentType = 'idiomatic'
    connectionBias = ['Prioritization']
    analyzer = AgentAnalyzer(aib, agentType, connectionBias)
    analyzer.analyze()
    
    

if __name__ == '__main__':
    analyze()
    
    