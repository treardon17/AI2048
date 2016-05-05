import random
import numpy as np
import copy, util
import pdb

class Expectimax:

    def __init__(self):
        self.score = 0
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

        for current_index in range(length):
            if line[current_index] != 0:
                result[last_index] = line[current_index]
                last_index += 1

        for key in range(length - 1):
            if result[key] == result[key + 1]:
                result[key] = result[key] * 2
                self.score += result[key]
                result.pop(key + 1)
                result.append(0)

        return result


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
                temp_grid.append(temp)
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
                temp_grid.append(temp)
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
                temp_grid.append(temp)
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
                temp_grid.append(temp)
            for row in range(4):
                for col in range(4):
                    newState[row][col] = temp_grid[row][4 -1 -col]

        return np.array(newState) #resulting grid from transition

    #gets the specified tile from state
    def get_tile(self, state, row, col):
        """
        Return the value of the tile at position [row][col]
        """
        return state[row][col]

    #gets the list of potential actions the computer can take
    def getLegalActions(self, state):
        legalActions = []
        currentGameState = copy.deepcopy(state)
        for action in self.actions:
            if not np.array_equiv(currentGameState, self.transition(state, action)):
                legalActions.append(action)
        return legalActions

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
    def getPossibleChildrenForState(self, state):
        children = []
        #get the legal actions for the current state
        legalActionsForState = self.getLegalActions(state)

        #get the possible states from the legal actions
        for action in legalActionsForState:
            children.append([self.transition(state, action), []])

        #probability % of getting a 2 (probability of getting a 4 is 10%)
        probabilityOfGetting2 = 90

        #get the free positions for each child
        for child in children:
            child[1] = self.getFreePositions(child[0])      #store the (x,y) coordinates
            randomPosition = random.choice(child[1])        #get a random (x,y) pair
            randomProb = random.randint(0,100)              #get a random number between 0 and 100

            #get the value for the new tile
            newTileValue = 0
            if randomProb <= probabilityOfGetting2:
                newTileValue = 2
            else:
                newTileValue = 4

            #assign the new tile value to the random position
            child[0][randomPosition[0]][randomPosition[1]] = newTileValue

        return children


    def getBest(self, state):
        util.notDefined("Expectimax.getBest()")


    # Copied from reinforcement. I'm pretty sure that this should work.
    def isTerminal(self, state):
        for action in self.actions:
            newState = self.transition(state, action)

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
