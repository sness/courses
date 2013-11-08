#!/usr/bin/python

#
# Find the shortest path in a graph using Dijkstra's algorithm
#

import sys

def dijkstra(graph,start,end):
    dist = {}
    unvisited = {}
    
    for n in graph:
        if n != start:
            dist[n] = float('inf')
            unvisited[n] = n
        else:
            dist[n] = 0

    print dist
    print unvisited
            

def run():
    graph = {
        'A': {'B': 1, 'C': 1},
        'B': {'D': 1, 'E': 1}
        'C': {'E': 1, 'F': 1}
        }
    start = 'A'
    end = 'E'
    dijkstra(graph,start,end)
    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        print "Usage: dijkstras-algorithm.py"
        sys.exit(1)
        
    run()
