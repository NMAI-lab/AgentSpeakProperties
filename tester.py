# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 14:36:56 2022

@author: Patrick
"""

from AgentAnalyzer import AgentAnalyzer
import shutil


def loadCsv(fileName):
    import csv
    data = []
    with open(fileName) as csvfile:
        fileData = csv.reader(csvfile)
        for element in fileData:
            data.append(element)
    return data


def compareCsv(a, b):
    aData = loadCsv(a)
    bData = loadCsv(b)
    errorCount = 0
    for row in aData:
        if not row in bData:
            print('ERROR: ' + str(row) + ' in ' + a + 'not found in ' + b)
            errorCount += 1
    
    for row in bData:
        if not row in aData:
            print('ERROR: ' + str(row) + ' in ' + b + 'not found in ' + a)
            errorCount += 1
    
    if errorCount > 0:
        print('CSV check FAILED: error count: ' + str(errorCount))
    else:
        print('CSV check PASSED: error count: ' + str(errorCount))
    
    return errorCount
    
    
def loadGv(fileName):
    with open(fileName) as f:
        lines = f.readlines()
    firstLine = lines[0]
    graphElements = []
    if not 'digraph {' in lines[1].strip() and not '}' in lines[-1].strip():
        print('ERROR: File not properly formatted -> ' + fileName)
    else:
        graphElements = lines[2:-2]
    return (firstLine, graphElements)


def compareGv(a, b):
    aFirstLine, aData = loadGv(a)
    bFirstLine, bData = loadGv(b)
    errorCount = 0
    
    for row in aData:
        if not row in bData:
            print('ERROR: ' + row + ' in ' + a + 'not found in ' + b)
            errorCount += 1
    
    for row in bData:
        if not row in aData:
            print('ERROR: ' + row + ' in ' + b + 'not found in ' + a)
            errorCount += 1
    
    if errorCount > 0:
        print('GV check FAILED: error count: ' + str(errorCount))
    else:
        print('GV check PASSED: error count: ' + str(errorCount))
    
    return errorCount
        
    
    
    
def runTestCase(inputFiles, agentType, connectionBias, expectedOutputFiles, actualOutputFiles):
    analyzer = AgentAnalyzer(inputFiles, agentType, connectionBias)
    analyzer.analyze()
    errorCount = 0
    for a, b in zip(expectedOutputFiles, actualOutputFiles):
        if 'csv' in a and 'csv' in b:
            errorCount += compareCsv(a, b)
        else:
            errorCount += compareGv(a, b)
    print('Test ' + agentType + ' completed with ' + str(errorCount) + ' errors.')
    return errorCount


def test():
    try:
        shutil.rmtree('output')
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))   
     
    errorCount = 0   
     
    inputFiles = ['testCases/case1Input/steeringController.asl',
                  'testCases/case1Input/carController.asl',
                  'testCases/case1Input/a_star.asl',
                  'testCases/case1Input/driveTowardController.asl',
                  'testCases/case1Input/map.asl',
                  'testCases/case1Input/obstacleAvoidStopper.asl',
                  'testCases/case1Input/positioningRules.asl',
                  'testCases/case1Input/speedController.asl']
    agentType = 'case1'
    connectionBias = ['Prioritization']
    expectedOutputFiles = ['testCases/expectedOutput/case1_!controlSpeed.gv', 
                           'testCases/expectedOutput/case1_!controlSteering.gv',
                           'testCases/expectedOutput/case1_!mission.gv',
                           'testCases/expectedOutput/case1_!navigate.gv',
                           'testCases/expectedOutput/case1_!waypoint.gv',
                           'testCases/expectedOutput/case1_CouplingCohesionReport.csv',
                           'testCases/expectedOutput/case1_CyclomaticComplexity.csv',
                           'testCases/expectedOutput/case1_obstacle.gv']
    actualOutputFiles = ['output/case1_!controlSpeed.gv', 
                         'output/case1_!controlSteering.gv',
                         'output/case1_!mission.gv',
                         'output/case1_!navigate.gv',
                         'output/case1_!waypoint.gv',
                         'output/case1_CouplingCohesionReport.csv',
                         'output/case1_CyclomaticComplexity.csv',
                         'output/case1_obstacle.gv']
    errorCount += runTestCase(inputFiles, agentType, connectionBias, 
                             expectedOutputFiles, actualOutputFiles)
        
        
    inputFiles = ['testCases/case2Input/carController.asl',
                  'testCases/case2Input/driveTowardController.asl',
                  'testCases/case2Input/map.asl',
                  'testCases/case2Input/positioningRules.asl',
                  'testCases/case2Input/speedController.asl',
                  'testCases/case2Input/steeringController.asl']
    agentType = 'case2'
    connectionBias = []
    expectedOutputFiles = ['testCases/expectedOutput/case2_!controlSpeed.gv',
                           'testCases/expectedOutput/case2_!controlSteering.gv',
                           'testCases/expectedOutput/case2_!mission.gv',
                           'testCases/expectedOutput/case2_!waypoint.gv',
                           'testCases/expectedOutput/case2_CouplingCohesionReport.csv',
                           'testCases/expectedOutput/case2_CyclomaticComplexity.csv']
    actualOutputFiles = ['output/case2_!controlSpeed.gv',
                         'output/case2_!controlSteering.gv',
                         'output/case2_!mission.gv',
                         'output/case2_!waypoint.gv',
                         'output/case2_CouplingCohesionReport.csv',
                         'output/case2_CyclomaticComplexity.csv']
    errorCount += runTestCase(inputFiles, agentType, connectionBias, 
                             expectedOutputFiles, actualOutputFiles)
        
        
    inputFiles = ['testCases/case3Input/carController.asl',
                  'testCases/case3Input/driveTowardController.asl',
                  'testCases/case3Input/map.asl',
                  'testCases/case3Input/positioningRules.asl',
                  'testCases/case3Input/steeringController.asl']
    agentType = 'case3'
    connectionBias = []
    expectedOutputFiles = ['testCases/expectedOutput/case3_!busy.gv',
                           'testCases/expectedOutput/case3_!mission.gv',
                           'testCases/expectedOutput/case3_CouplingCohesionReport.csv',
                           'testCases/expectedOutput/case3_CyclomaticComplexity.csv',
                           'testCases/expectedOutput/case3_navigate.gv',
                           'testCases/expectedOutput/case3_obstacle.gv']
    actualOutputFiles = ['output/case3_!busy.gv',
                         'output/case3_!mission.gv',
                         'output/case3_CouplingCohesionReport.csv',
                         'output/case3_CyclomaticComplexity.csv',
                         'output/case3_navigate.gv',
                         'output/case3_obstacle.gv']
    errorCount += runTestCase(inputFiles, agentType, connectionBias, 
                             expectedOutputFiles, actualOutputFiles)
    
    print('--- Test completed with ' + str(errorCount) + ' errors. ---')
    

if __name__ == '__main__':
    test()
    