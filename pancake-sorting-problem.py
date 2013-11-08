#!/usr/bin/python

#
# Find the shortest route between input and output given the pancake
# sorting problem.
#

import sys

data = {}
strLen = 0
queue = {}
queueLevel = 0
startStr = ""
endStr = ""

def doFlip(inStr,loc):
    outStr = inStr[loc::-1] + inStr[loc+1::]
    data[inStr][outStr] = 1;
    
def doAllFlips(inStr):
    for i in range(1,strLen):
        doFlip(inStr,i)
    for item in data[inStr]:
        if item not in data:
            data[item] = {}
            doAllFlips(item)

def doBreadthFirstSearch(startStr, endStr):
    # Convert data to adjacency list format graph
    graph = {}
    for k in data:
        a = []
        for item in data[k]:
            a.append(item)
        graph[k] = a

    print bfs(graph, startStr, endStr)

# Breadth first search
# adapted from http://bit.ly/12CpMe7
def bfs(g, s, e):
    a = []
    a.append([s])
    while a:
        p = a.pop(0)
        n = p[-1]
        if n == e:
            return p
        for adj in g.get(n, []):
            np = list(p)
            np.append(adj)
            a.append(np)

def run(startStr, endStr):
    data[startStr] = {}
    doAllFlips(startStr)
    doBreadthFirstSearch(startStr, endStr)
    
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: pancake-sorting-problem.py startStr endStr"
        sys.exit(1)
        
    startStr = sys.argv[1]
    endStr = sys.argv[2]
    
    if len(startStr) != len(endStr):
        print "String lengths do not match (%i) (%i)" % (len(startStr),len(endStr))
        sys.exit(1)

    strLen = len(startStr)
                   
    run(startStr, endStr)
