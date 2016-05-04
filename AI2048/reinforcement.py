import util, pdb
import numpy as np
import copy


class Agent:
    def __init__(self):
        self.weights = util.Counter()
        self.weights["mergeCount"] = 0
        self.weights["largestPos"] = 0
        self.weights["free"] = 0

        self.OFFSETS = {'up': (1, 0), 'down': (-1, 0), 'left': (0, 1), 'right': (0, -1)}

        self.state = np.array([[1,0,0,1],[1,0,0,0],[1,0,1,0],[1,0,1,0]])
        self.actions = ['up', 'down', 'left', 'right']
        self.currScore = 0

        self.gamma = 0.8
        self.alpha = 0.2



    def printState(self, state):
        for x in state:
            for y in x:
                print '{0:3}'.format(y),
            print
        print "-------------------"



    def transition(self, state, action):
        # will return right even though it can't go right.
        # need to implement a legal actions list
        score = 0
        mergeCount = 0
        offset = self.OFFSETS[action]
        temp_grid = []
            
        # Up
        if action == 'up':
            for row in range(4):
                start = 0
                temp_list = []
                for this_col in range(4):
                    temp_list.append(state[start][row])
                    start += offset[0]
                temp_list, temp_score, temp_mCount = self.merge(temp_list)
                score += temp_score
                mergeCount += temp_mCount
                temp_grid.append(temp_list)
            """for row in range(4):
                for col in range(4):
                    self._grid[row][col] = temp_grid[col][row]"""
        
        # Down
        elif action == 'down':
            for row in range(4):
                start = 4 -1
                temp_list = []
                for this_col in range(4):
                    temp_list.append(state[start][row])
                    start += offset[0]
                temp_list, temp_score, temp_mCount = self.merge(temp_list)
                score += temp_score
                mergeCount += temp_mCount
                temp_grid.append(temp_list)
            """for row in range(4):
                for col in range(4):
                    self._grid[row][col] = temp_grid[col][4 -1 -row]"""
        
        # Left
        elif action == 'left':
            for col in range(4):
                start = 0
                temp_list = []
                for this_row in range(4):
                    temp_list.append(state[col][start])
                    start += offset[1]
                temp_list, temp_score, temp_mCount = self.merge(temp_list)
                score += temp_score
                mergeCount += temp_mCount
                temp_grid.append(temp_list)
            """for row in range(4):
                for col in range(4):
                    self._grid[row][col] = temp_grid[row][col]"""

        # Right                    
        elif action == 'right':
            for col in range(4):
                start = 4 -1
                temp_list = []
                for this_row in range(4):
                    temp_list.append(state[col][start])
                    start += offset[1]
                temp_list, temp_score, temp_mCount = self.merge(temp_list)
                score += temp_score
                mergeCount += temp_mCount
                temp_grid.append(temp_list)
            """for row in range(4):
                for col in range(4):
                    self._grid[row][col] = temp_grid[row][4 -1 -col]"""
        
        """total_num = 1
        for value in self._grid:
            for val_el in value:
                total_num *= val_el
                if total_num == 0:
                    self._is_occupied = False
                    break
                else:
                    self._is_occupied = True"""

        return (np.array(temp_grid),score, mergeCount)



    def merge(self, line):
        """
        Function that merges a single row or column in 2048
        """
        length = len(line)
        result = [0] * length
        last_index = 0
        score = 0
        mergeCount = 0

        for current_index in range(length):
            if line[current_index] != 0:
                result[last_index] = line[current_index]
                last_index += 1

        for key in range(length - 1):
            if result[key] is result[key + 1]:
                result[key] = result[key] * 2
                score += result[key]
                mergeCount += 1
                result.pop(key + 1)
                result.append(0)
        return (result, score, mergeCount)


    def isTerminal(self, state):
        for action in self.actions:
            newState = self.transition(state, action)

            if np.array_equiv(newState, state):
            #if (newState != state).all():
                print "[+] Action:", action
                self.printState(self.transition(state, action))
                return True
        return False



    def getBest(self, state):
        bestAction = None
        maxVal = 0
        for action in self.getLegalActions(state):
            tempVal = self.transition(state, action)  #tempVal is a tuple (nextState, score, mergedCount)
            if tempVal[1] >= maxVal:
                maxVal = tempVal[1]
                bestAction = action

        if bestAction is None:
            return (0,"Exit")
        else:
            return (maxVal, bestAction)



    def getFeatures(self, state):
        feats = util.Counter()
        oneDpos = np.argmax(state)

        pos = (oneDpos/4, oneDpos%4)   #(row, col)

        if pos == (3,3):
            feats["largestPos"] = 50
        elif pos[0] == 3:
            feats["largestPos"] = 25
        else:
            feats["largestPos"] = 5

        feats["free"] = 16 - np.count_nonzero(state)
        sumMergeCount = 0
        #sumScore = 0
        for action in self.getLegalActions(state):
            things = self.transition(state, action)
            sumMergeCount += things[2]
            #sumScore += things[1]

        feats["mergeCount"] = sumMergeCount
        #feats["score"] = sumScore
        return feats


    def getQValue(self, state):
        return self.weights.__mul__(self.getFeatures(state))



    def updateWeights(self, state, action, reward):
        features = self.getFeatures(state)
        #the score is the reward

        difference = (reward + self.gamma*self.getBest(state)[0]) - self.getQValue(state)

        for f in features.keys():
            self.weights[f] = self.weights[f] + (self.alpha*difference*features[f])



    def getLegalActions(self, state):
        legalActions = []
        for action in self.actions:
            if not np.array_equiv(self.transition(state, action)[0], state):
                legalActions.append(action)

        return legalActions