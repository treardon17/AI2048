import util
import numpy as np
import copy


#state = [[1,0,0,1],[1,0,0,0],[1,0,1,0],[1,0,1,0]]  #state[row][col]
state = np.array([[1,0,0,1],[1,0,0,0],[1,0,1,0],[1,0,1,0]])

def printState(state):
    for x in state:
        for y in x:
            print y,
        print

def transition(state, action):
    newState = [[],[],[],[]]
    index = 0
    if action == "left" or action == "up":
        index = 3
    if action == "up" or action == "down":
        state = state.T

    i = 0
    for x in state:
        for y in x:
            if y != 0:
                newState[i].insert(index, y)
        i += 1
    for x in newState:
        while len(x) < 4:
            x.insert(index, 0)


    if action == 'up' or action == 'down':
        return np.array(newState).T
    else:
        return np.array(newState)

printState(state)
print "-------------------"
state = transition(state, 'up')
printState(state)
print "-------------------"
state = transition(state, 'down')
printState(state)
print "-------------------"
state = transition(state, 'left')
printState(state)
print "-------------------"
state = transition(state, 'right')
printState(state)