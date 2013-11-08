#!/usr/bin/python

#
# Do a global alignment of two strings using the Needleman-Wunsch
# algorithm and then find the path that has the fewest events in it.
#

import sys

# Penalties
MATCH = 1
MISMATCH = -1
GAP = -2

# Make the two dimensional array
def createEmptyMatrix(a,b):
    m = []
    for i in range(0,len(a)+1):
        n = []
        for j in range(0,len(b)+1):
            n.append({'i':i,
                      'j':j,
                      'score':None,
                      'parents':[],
                      'dist': float('inf'),
                      'visited': False
                      })
        m.append(n)
    return m

def matchScore(a,b):
    if a == b:
        return MATCH
    else:
        return MISMATCH

def doGlobalAlign(a, b):
    score = createEmptyMatrix(a,b)

    # Initialize the first row of the matrix
    for i in range(0,len(score)):
        score[i][0]['score'] = i * GAP

    for i in range(0,len(score[0])):
        score[0][i]['score'] = i * GAP

    # Fill in the rest of the matrix from these
    for i in range(1,len(score)):
        for j in range(1,len(score[i])):
            this = score[i][j]
            up = score[i-1][j]
            left = score[i][j-1]
            diag = score[i-1][j-1]

            upScore = up['score'] + GAP
            leftScore = left['score'] + GAP
            diagScore = diag['score'] + matchScore(a[i-1],b[j-1])
            
            this['score'] = upScore
            this['parents'] = [{'i' : up['i'], 'j' : up['j']}]
            
            if (diagScore == upScore):
                this['parents'].append({'i' : diag['i'], 'j' : diag['j']})

            if (diagScore > upScore):
                this['score'] = diagScore
                this['parents'] = [{'i' : diag['i'], 'j' : diag['j']}]

            if (leftScore == diagScore):
                this['parents'].append({'i' : left['i'], 'j' : left['j']})
                
            if (leftScore > diagScore):
                this['score'] = leftScore
                this['parents'] = [{'i' : left['i'], 'j' : left['j']}]

    print score

def run(a, b):
    doGlobalAlign(a, b)
    
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: needleman-wunsch.py sequence_a sequence_b"
        sys.exit(1)
        
    a = sys.argv[1]
    b = sys.argv[2]
    
    run(a,b)
