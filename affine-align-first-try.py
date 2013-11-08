#!/usr/bin/python

#
# Do a global alignment of two strings using the Needleman-Wunsch
# algorithm.
#

import sys
import numpy as np
import operator

inf = float("inf")

def matchScore(a,b,matchCost,mismatchCost):
    """Return the score for aligning character a with b"""
    if a==b:
        return matchCost
    else:
        return mismatchCost

# pretty print    
def pp(d):
    outStr = ""
    for i in range(d.shape[0]):
        for j in range(d.shape[1]):
            outStr += "%.3f\t" % (d[i][j])
        outStr += "\n"
        
    print outStr
        

            
def doAffineAlign(x, y, matchCost, mismatchCost, openCost, extendCost):
    lx = len(x)+1
    ly = len(y)+1
    M = np.zeros((lx,ly))
    X = np.zeros((lx,ly))
    Y = np.zeros((lx,ly))

    for i in xrange(1, lx):
        M[i][0] = -inf
        X[i][0] = -inf
        Y[i][0] = openCost + i * extendCost

    for i in xrange(1, ly):
        M[0][i] = -inf
        X[0][i] = openCost + i * extendCost
        Y[0][i] = -inf

    for i in xrange(1, len(x)+1):
        for j in xrange(1, len(y)+1):

            M[i][j] = matchScore(x[i-1], y[j-1], matchCost, mismatchCost) + max(
                M[i-1][j-1],
                X[i-1][j-1],
                Y[i-1][j-1]
            )

            X[i][j] = max(
                    M[i][j-1] + openCost + extendCost,
                    X[i][j-1] + extendCost,
                    Y[i][j-1] + openCost + extendCost
            )

            Y[i][j] = max(
                    M[i-1][j], openCost + extendCost,
                    X[i-1][j] + openCost + extendCost,
                    Y[i-1][j] + extendCost
            )

    
    pp(X)
    pp(M)
    pp(Y)
    print "------------------------------"
    
    # The path can now travel
    # Start in table S
    # If S[i,j] = GA[i,j] or GB[i,j], jump to the corresponding table, without making a move.
    # Paths through GAmust move up
    # Paths through GBmust move left

    i = lx-1
    j = ly-1
    # print "i=%i\tj=%i" % (i, j)
    # print "X[i][j]=%f\tM[i][j]=%f\tY[i][j]=%f" % (X[i][j], M[i][j], Y[i][j])

    xStr = ""
    yStr = ""
    print x
    print y
    currArray = ""
    while i > 0 and j > 0:
        print "------------------------------"
        print "i=%i\tj=%i" % (i, j)
        
        arrays = {X[i][j] : "X", M[i][j] : "M", Y[i][j] : "Y"}
        print arrays
        maxArray = max(arrays.iteritems(), key=operator.itemgetter(0))[1]
        if currArray == "":
            currArray = maxArray
        print "maxArray=%s\tcurrArray=%s" % (maxArray, currArray)
        if maxArray == currArray:
            if maxArray == "X":
                xStr += "-"
                yStr += y[j-1]
            if maxArray == "M":
                xStr += x[i-1]
                yStr += y[j-1]
            if maxArray == "Y":
                xStr += x[i-1]
                yStr += "-"
            values = [X[i-1][j-1], M[i-1][j-1], Y[i-1][j-1]]
            vindex = values.index(max(values))
            if vindex == 0:
                j = j - 1
            if vindex == 1:
                i = i - 1
                j = j - 1
            if vindex == 2:
                i = i - 1

        currArray = maxArray
        
    print xStr[::-1]
    print yStr[::-1]

    
    

def run(seq1, seq2, matchCost, mismatchCost, openCost, extendCost):
    doAffineAlign(seq1, seq2, matchCost, mismatchCost, openCost, extendCost)
    
if __name__ == "__main__":
    if len(sys.argv) < 6:
        print "Usage: affine-align.py seq1 seq2 matchCost mismatchCost openCost extendCost"
        sys.exit(1)
        
    seq1 = sys.argv[1]
    seq2 = sys.argv[2]
    matchCost = float(sys.argv[3])
    mismatchCost = float(sys.argv[4])
    openCost = float(sys.argv[5])
    extendCost = float(sys.argv[6])
    
    run(seq1, seq2, matchCost, mismatchCost, openCost, extendCost)
