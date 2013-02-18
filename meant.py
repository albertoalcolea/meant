#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import commands
import re
import os.path
import math
import time



def checkAppExists(cmd):
    status = False
    l = re.findall(r'(\S+)(\s+.+)?', cmd)

    try: 
        exe = l[0][0]
    except:
        return False 
        
    wout = commands.getstatusoutput('which ' + exe)
    exists = os.path.isfile(exe)
        
    return (wout[0] == 0 or exists)


def extractTime(cmd):
    while (True):  # If the app returns error, run it again
        tinit = time.time()
        out = commands.getstatusoutput(cmd)
        t = time.time() - tinit
        if out[0] == 0:
            break
  
    return t


def calculateMean(cmd, numRepeats):
    print "Starting  the calculation of the mean time..."
  
    ltimes = []
  
    for n in range(0, numRepeats):
        sys.stdout.write("  Test [" + str(n+1) + "]")
        sys.stdout.flush()
        t = extractTime(cmd)
        print ":\t%4.3f s" % (t)
        ltimes.append(t)
        
    return ltimes


def showResults(ltimes, graph=False, graphST=False, graphName="graph.png"):
    nSamples = len(ltimes)
    mean = sum([x for x in ltimes]) / nSamples
    variance = sum([(x-mean)**2 for x in ltimes]) / len(ltimes)
    sDeviation = math.sqrt(variance)
	
    print "Mean time for ", nSamples, "executions:", mean, "s"
    print "Standard deviation for", nSamples, "executions:", sDeviation, "s"
    if graph:
        draw(ltimes, mean, sDeviation, graphST, graphName)


def draw(ltimes, mean, sDeviation, graphST, graphName):
    import matplotlib.pyplot as plt
 
    plt.figure()
    
    # x-axis = num of tests
    x = range(1, len(ltimes)+1)
    
    # In the line of the mean put all y = mean
    y_mean = [mean for i in range(len(ltimes))]
 
    #plot the two lines
    plt.plot(x, ltimes, 'bo')
    plt.plot(x, y_mean, 'r')
    
    if graphST:
        y_plusST = [mean+sDeviation for i in range(len(ltimes))]
        y_minusST = [mean-sDeviation for i in range(len(ltimes))]
        plt.plot(x, y_plusST, 'k')
        plt.plot(x, y_minusST, 'k')
        
        legend = '\mu=' +  str(round(mean, 3)) + ',\ \sigma=' + str(round(sDeviation, 3))
    else:
        legend = '\mu=' +  str(round(mean, 3))
    
    plt.text(1.5, mean+.005, r'$' + legend + '$', bbox={'facecolor':'red', 'alpha':0.8, 'pad':5})
    plt.axis([1, len(ltimes), min(ltimes)-0.05, max(ltimes)+0.05])
    plt.grid(True)

    plt.savefig(graphName)


def meant(argv):
    
    cmd = ""
    graph = False
    graphST = False
    graphName = ""
    repeats = 20
	
  
    # Read the arguments
    i = 0
    while (i < len(argv)-1): 
        if (argv[i] == "-n"): # Repeats
            try:
                repeats = int(argv[i + 1])
                if (repeats < 1):
                    raise Exception("Invalid repeat number")
                i += 1
            except:
                print >>sys.stderr, "Invalid parameters"
                exit(1)

        elif (argv[i] == "-g"): # Graph
            graph = True
            
        elif (argv[i] == "-gst"): # Graph with standard deviation
            graph = True
            graphST = True
            
        elif (argv[i] == "-gname"):
            try:
                graphName = argv[i + 1]
                if os.path.isfile(graphName):
                    raise Exception("Invalid filename for graph")
                i += 1
            except:
                print >>sys.stderr, "Invalid parameters"
                exit(1)

        else:
            print >>sys.stderr, "Unknown parameter:", argv[i]
            exit(1)
            
        i += 1
    
    # CMD
    try:
        if not checkAppExists(argv[i]):
            raise Exception("Invalid app to measure")
        cmd = argv[i]
    except:
        print >>sys.stderr, "The app to measure doesn't exists"
        exit(1)
        
    # Default name for the graph file    
    if graph and graphName == "":
        graphName = "graph_" + str(int(time.time())) + ".png"
    
    # Launch the app and calculate execution time    
    ltimes = calculateMean(cmd, repeats)
    showResults(ltimes, graph, graphST, graphName)
  

# MAIN
if __name__ == '__main__':
    argc = len(sys.argv)  # Num of args

    if argc < 2:
        print >>sys.stderr, "USAGE:", sys.argv[0], "[-n repeats] [-u regex] [-g|-gst] [-gname filename] 'app to measure'"
        exit(1)
        
    meant(sys.argv[1:])
