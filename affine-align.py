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
    outStr = "\t"
    for j in range(d.shape[1]):
        outStr += "j=%i\t" % j
    outStr += "\n"
  
    for i in range(d.shape[0]):
        outStr += "i=%i\t" % i
        for j in range(d.shape[1]):
          
            outStr += "%+.3f\t" % (d[i][j])
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

    for j in xrange(1, ly):
        M[0][j] = -inf
        X[0][j] = openCost + j * extendCost
        Y[0][j] = -inf

    for i in xrange(1, lx):
        for j in xrange(1, ly):

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
                    M[i-1][j] + openCost + extendCost,
                    X[i-1][j] + openCost + extendCost,
                    Y[i-1][j] + extendCost
            )

    i = lx - 1
    j = ly - 1
    #    
    # Find matrix to start in
    #
    arrays = [M,X,Y]
    values = [M[i][j],Y[i][j],X[i][j]]
    currArray = values.index(max(values))

    xStr = ""
    yStr = ""
    
    # Iterate until we are at the 0,0 element
    while i + j > 0:
        # M array
        if currArray == 0:
            values = [M[i-1][j-1],Y[i-1][j-1],X[i-1][j-1]]
            maxArray = values.index(max(values))
            xStr += x[i-1]
            yStr += y[j-1]

            i = i - 1
            j = j - 1
            

        # Y array
        if currArray == 1:
            values = [M[i-1][j],Y[i-1][j],X[i-1][j]]
            maxArray = values.index(max(values))
            xStr += x[i-1]
            yStr += "-"
                
            i = i - 1

        # X array
        if currArray == 2:
            values = [M[i][j-1],Y[i][j-1],X[i][j-1]]
            maxArray = values.index(max(values))
            xStr += "-"
            yStr += y[j-1]
            j = j - 1

        currArray = maxArray

    return (xStr[::-1],yStr[::-1])
    

def testAlgorithm(seq1, seq2, align1, align2, matchCost, mismatchCost, openCost, extendCost):
    print "Asserting that %s aligned with %s should give %s and %s as alignments" % (seq1, seq2, align1, align2)
    test1,test2 = doAffineAlign(seq1, seq2, matchCost, mismatchCost, openCost, extendCost)
    assert test1 == align1
    assert test2 == align2
    print "Passed"
    print
    

def run(seq1, seq2, matchCost, mismatchCost, openCost, extendCost):
    print "Running tests"
    testAlgorithm("AAA", "AAA", "AAA", "AAA", +1, -1, -3, 0.1)
    testAlgorithm("ATA", "AAA", "ATA", "AAA", +1, -1, -3, 0.1)
    testAlgorithm("ATTTTT", "A", "ATTTTT", "A-----", +1, -1, -3, 0.1)
    testAlgorithm("A", "ATTTTT", "A-----", "ATTTTT", +1, -1, -3, 0.1)
    testAlgorithm("ACCCCG", "AG", "ACCCCG", "A----G", +1, -1, -3, 0.1)
    testAlgorithm("GTA", "GCCCCCCCCA", "G-------TA", "GCCCCCCCCA", +1, -1, -3, 0.1)
    testAlgorithm("GTTTTCCCCCTTTA", "GCCCCA", "GTTTTCCCCCTTTA", "G------CCCC--A", +1, -1, -3, 0.1)
    print "--------------------------------------------------------------------------------"

    # Do the alignment
    print "Running Alignment"
    a,b = doAffineAlign(seq1, seq2, matchCost, mismatchCost, openCost, extendCost)
    print a
    print b
    
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
