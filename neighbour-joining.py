#!/usr/bin/python

#
# Use the neighbour joining algorithm to build a tree
#

import sys
import numpy as np
import scipy as scipy
import itertools
from sys import maxint

def calculateQ(d):
    r = d.shape[0]
    q = np.zeros((r,r))
    for i in xrange(r):
        for j in xrange(r):
            if i == j:
                q[i][j] = 0
            else:
                sumI = 0
                sumJ = 0
                for k in xrange(r):
                    sumI += d[i][k]
                    sumJ += d[j][k]
                q[i][j] = (r-2) * d[i][j] - sumI - sumJ

    return q

def findLowestPair(q):
    r = q.shape[0]
    minVal = maxint
    for i in xrange(0,r):
        for j in xrange(i,r):
            if (q[i][j] < minVal):
                minVal = q[i][j]
                minIndex = (i,j)
    return minIndex


def doDistOfPairMembersToNewNode(i,j,d):
    r = d.shape[0]
    sumI = 0
    sumJ = 0
    for k in xrange(r):
        sumI += d[i][k]
        sumJ += d[j][k]

    dfu = (1. / (2. * (r - 2.))) * ((r - 2.) * d[i][j] + sumI - sumJ)
    dgu = (1. / (2. * (r - 2.))) * ((r - 2.) * d[i][j] - sumI + sumJ)

    return (dfu,dgu)

def calculateNewDistanceMatrix(f,g,d):
    print d
    r = d.shape[0]
    nd = np.zeros((r-1,r-1))

    # Copy over the old data to this matrix
    ii = jj = 1
    for i in xrange(0,r):
        if i == f or i == g:
            continue
        for j in xrange(0,r):
            if j == f or j == g:
                continue
            nd[ii][jj] = d[i][j]
            jj += 1
        ii += 1
        jj = 1
            
    # Calculate the first row and column
    ii = 1
    for i in range (0,r):
        if i == f or i == g:
            continue
        nd[0][ii] = (d[f][i] + d[g][i] - d[f][g]) / 2.
        nd[ii][0] = (d[f][i] + d[g][i] - d[f][g]) / 2.
        ii += 1

    return nd
    
def doNeighbourJoining(d):
    labels = ["A","B","C","D","E","F","G","H"]
    
    while d.shape[0] > 1:
        q = calculateQ(d)
        lowestPair = findLowestPair(q)
        print "Joining"
        print lowestPair[0]
        print lowestPair[1]
        # newlabel = "%s%s" % (labels[lowestPair[0]], labels[lowestPair[1]])
        # print "lowestPair[0]=%i\tlowestPair[1]=%i" % (lowestPair[0], lowestPair[1])
        # print labels
        # print newlabel
        # del labels[lowestPair[0]]
        # del labels[lowestPair[1]]
        # labels.insert(0,newlabel)

        i = lowestPair[0]
        j = lowestPair[1]
        
        pairDist = doDistOfPairMembersToNewNode(i,j,d)
        d = calculateNewDistanceMatrix(i,j,d)
        # print d

        
    
    
def run(distMatrix):
    doNeighbourJoining(distMatrix)
    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        print "Usage: neighbour-joining.py"
        sys.exit(1)

    distMatrix = np.array(
        [
            [  0,  30,  68,  57, 127,  27,  28,  33],
            [ 30,   0,  58,  47, 117,  11,  52,  57],
            [ 68,  58,   0,  35,  69,  55,  87,  92],
            [ 57,  47,  35,   0,  94,  44,  79,  84],
            [127, 117,  69,  94,   0, 114, 149, 154],
            [ 27,  11,  55,  44, 114,   0,  49,  54],
            [ 28,  52,  87,  79, 149,  49,   0,  13],
            [ 33,  57,  92,  84, 154,  54,  13,   0],
         ]
        )
    # distMatrix = np.array(
    #     [
    #         [  0,   7,  11,  14 ],
    #         [  7,   0,   6,   9 ],
    #         [ 11,   6,   0,   7 ],
    #         [ 14,   9,   7,   0 ]
    #      ]
    #     )
    # distMatrix = np.array(
    #     [
    #         [  0,   1,  2,  3, 4 ],
    #         [  5,   6,  7,  8,  9 ],
    #         [ 10 ,  11 , 12 , 13 , 14  ],
    #         [ 15 ,  16 ,17  , 18 , 19  ],
    #         [ 20 ,  21 , 22 , 23 , 24  ],

    #      ]
    #     )
        
    run(distMatrix)
