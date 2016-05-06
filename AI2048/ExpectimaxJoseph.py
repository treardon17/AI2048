import random
import numpy as np
import copy, util
import pdb

class Expectimax:

    def __init__(self):
        #self.score = 0
        self.depth = 6
        self.UP = 1
        self.DOWN = 2
        self.LEFT = 3
        self.RIGHT = 4
        self.actions = ["up","down","left","right"]
        self.OFFSETS = {'up': (1, 0), 'down': (-1, 0), 'left': (0, 1), 'right': (0, -1)}

    # I don't think we need this. This contains self._grid, and that is not in this class
    def __str__(self):
        """
        Return a string representation of the grid
        """
        return str(self._grid)

    def merge(self, line):
        """
        Function that merges a single row or column in 2048
        """
        length = len(line)
        result = [0] * length
        last_index = 0
        score = 0

        for current_index in range(length):
            if line[current_index] != 0:
                result[last_index] = line[current_index]
                last_index += 1

        for key in range(length - 1):
            if result[key] == result[key + 1]:
                result[key] = result[key] * 2
                score += result[key]
                result.pop(key + 1)
                result.append(0)

        return (result, score)


    def transition(self, state, action):
        score = 0
        mergeCount = 0
        offset = self.OFFSETS[action]
        temp_grid = []
        newState =[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

        # Up
        if action == 'up':
            for row in range(4):
                start = 0
                temp_list = []
                for this_col in range(4):
                    temp_list.append(state[start][row])
                    start += offset[0]
                temp = self.merge(temp_list)
                score += temp[1]
                temp_grid.append(temp[0])
            for row in range(4):
                for col in range(4):
                    newState[row][col] = temp_grid[col][row]

        # Down
        elif action == 'down':
            for row in range(4):
                start = 4 -1
                temp_list = []
                for this_col in range(4):
                    temp_list.append(state[start][row])
                    start += offset[0]
                temp = self.merge(temp_list)
                score += temp[1]
                temp_grid.append(temp[0])
            for row in range(4):
                for col in range(4):
                    newState[row][col] = temp_grid[col][4 -1 -row]

        # Left
        elif action == 'left':
            for col in range(4):
                start = 0
                temp_list = []
                for this_row in range(4):
                    temp_list.append(state[col][start])
                    start += offset[1]
                temp = self.merge(temp_list)
                score += temp[1]
                temp_grid.append(temp[0])
            for row in range(4):
                for col in range(4):
                    newState[row][col] = temp_grid[row][col]

        # Right
        elif action == 'right':
            for col in range(4):
                start = 4 -1
                temp_list = []
                for this_row in range(4):
                    temp_list.append(state[col][start])
                    start += offset[1]
                temp = self.merge(temp_list)
                score += temp[1]
                temp_grid.append(temp[0])
            for row in range(4):
                for col in range(4):
                    newState[row][col] = temp_grid[row][4 -1 -col]

        return (np.array(newState), score) #resulting grid from transition

    #gets the specified tile from state
    def get_tile(self, state, row, col):
        """
        Return the value of the tile at position [row][col]
        """
        return state[row][col]

    #gets the list of potential actions the computer can take
    def getLegalActions(self, state):
        """legalActions = []
        currentGameState = copy.deepcopy(state)
        for action in self.actions:
            if not np.array_equiv(currentGameState, self.transition(state, action)[0]):
                legalActions.append(action)
        return legalActions"""
        return self.actions

    #gets the free positions on the gameState
    #returns tuple of zero-based (x,y) coordinates
    def getFreePositions(self, state):
        freePositions = []
        for x in range(0,4):
            for y in range(0,4):
                if state[x][y] == 0:
                    freePositions.append((x,y))
        return freePositions

    #returns a list of gameState children for a given
    #state and all the legal actions at that state
    def posNewTile(self, state):
        newState = copy.deepcopy(state)

        freePos = self.getFreePositions(newState)      #store the (x,y) coordinates

        if len(freePos) != 0:
            randomPosition = random.choice(freePos)        #get a random (x,y) pair
            randomProb = random.randint(0,100) #get a random number between 0 and 100

            #get the value for the new tile
            newTileValue = 0
            if randomProb <= 90:
                newTileValue = 2
            else:
                newTileValue = 4

            #assign the new tile value to the random position
            newState[randomPosition[0]][randomPosition[1]] = newTileValue

            return newState
        else:
            return state



    #def getBest(self, state):
    #    util.notDefined("Expectimax.getBest()")


    def getBest(self, state):
        def value(depth, state):
            if self.isTerminal(state) or depth == self.depth*2:
                return (0, None)

            # if the next state is the AI turn
            if depth % 2 == 0:
                return maxVal(depth, state)
            # else the next state will be determined by a random addition
            else:
                return expVal(depth, state)


        def maxVal(depth, state):
            mVal = float("-inf")
            bestAction = None

            for action in self.getLegalActions(state):
                child = self.transition(state, action)   # (newState, stateScore)
                childScore = value((depth + 1), child[0])[0]
                if childScore > mVal:
                    mVal = child[1]
                    bestAction = action

            return (mVal, bestAction)

        def expVal(depth, state):
            """v = 0
            p = 1/float(len(self.getLegalActions(state)))  # see multiAgents.py code for more explaination
            bestAction = ""

            for action in self.getLegalActions(state):
                child = self.transition(state, action)
                childScore = value((depth + 1), child[0])[0]

                v+= p*childScore"""
            p = 1/float(len(self.getLegalActions(state)))
            newState = self.posNewTile(state)
            childScore = value((depth +1), newState)[0]
            v = p*childScore


            return (childScore, None, newState)

        return value(0, state)[1]   # This will be the best action returned from maxVal or expVal


    # Copied from reinforcement. I'm pretty sure that this should work.
    # need to optimize the program so we need to get rid of the self.transition() call
    def isTerminal(self, state):
        for action in self.actions:
            newState = self.transition(state, action) # don't like this. This probably slows it down a lot

            if np.array_equiv(newState, state):
                # if (newState != state).all():
                print "[+] Action:", action
                self.printState(newState)
                return True
        return False

    """def isTerminal(self, state):
        # Think we can copy paste this from the other one.
        util.notDefined("Expetimax.isTerminal()")"""


"""state = [[2,2,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
expectimax = Expectimax()
print state
print expectimax.getPossibleChildrenForState(state)"""





#endOfFile
