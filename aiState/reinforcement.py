import util, pdb
import numpy as np
import copy


#state = [[1,0,0,1],[1,0,0,0],[1,0,1,0],[1,0,1,0]]  #state[row][col]
#state = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])
state = np.array([[1,0,0,1],[1,0,0,0],[1,0,1,0],[1,0,1,0]])
actions = ['up', 'down', 'left', 'right']

def printState(state):
    for x in state:
        for y in x:
            print '{0:3}'.format(y),
        print
    print "-------------------"

def transition(state, action):
    newState = [[],[],[],[]]
    index = 0
    if action == "left" or action == "up":
        index = 3
    if action == "up" or action == "down":
        state = state.T


    i = 0
    for x in state:
        if index == 3:
            for y in x:
                if y != 0:
                    if y in newState[i]:
                        newState[i][newState[i].index(y)] = 2*y
                    else:
                        newState[i].insert(index, y)
        else:
            for y in reversed(x):
                if y != 0:
                    if y in newState[i]:
                        newState[i].reverse()
                        newState[i][newState[i].index(y)] = 2 * y
                        newState[i].reverse()
                    else:
                        newState[i].insert(index, y)
        i += 1


    for x in newState:
        while len(x) < 4:
            x.insert(index, 0)


    if action == 'up' or action == 'down':
        return np.array(newState).T
    else:
        return np.array(newState)

def isTerminal(state):
    for action in actions:
        newState = transition(state, action)
        if (newState != state).all():
            print "[+] Action:", action
            printState(transition(state, action))
            return True
    return False

printState(state)
state = transition(state, 'down')
printState(state)
state = transition(state, 'right')
printState(state)
state = transition(state, 'left')
printState(state)
state = transition(state, 'up')
printState(state)
state = transition(state, 'down')
printState(state)
state = transition(state, 'right')
printState(state)

if not isTerminal(state):
    print "Terminal State"
else:
    print "Not the Terminal State"