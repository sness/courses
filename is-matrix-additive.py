#!/usr/bin/python

#
# Do a global alignment of two strings using the Needleman-Wunsch
# algorithm.
#

import sys
import numpy as np
import itertools

def checkPermutations(ii,jj,kk,ll,d):
    a = [ii,jj,kk,ll]
    print a
    for n in list(itertools.permutations(a)):
        i = n[0]
        j = n[1]
        k = n[2]
        l = n[3]
        print "%f <= %f = %f" % (
            d[i][l] + d[j][k], d[i][j] + d[i][j], d[i][k] + d[j][l])
        if (d[i][j] + d[k][l] == d[i][k] + d[j][l]) and (d[i][k] + d[j][l] >= d[i][l] + d[j][k]):
            print "Additive"
            return
    print "Not additive"
    
def doCheckDistMatrixAdditive(d):
    for i in xrange(0,d.shape[0]):
        for j in xrange(i+1,d.shape[0]):
            for k in xrange(j+1,d.shape[0]):
                for l in xrange(k+1,d.shape[0]):
                    checkPermutations(i,j,k,l,d)
                
    
def run(distMatrix):
    doCheckDistMatrixAdditive(distMatrix)
    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        print "Usage: is-matrix-additive.py"
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
        
    run(distMatrix)
