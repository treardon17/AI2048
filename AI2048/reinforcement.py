import util, pdb, random
import numpy as np
import copy


class Reinforcement:
    def __init__(self):
        self.weights = util.Counter()
        self.weights["mergeCount"] = 0
        self.weights["largestPos"] = 0
        self.weights["free"] = 0

        self.OFFSETS = {'up': (1, 0), 'down': (-1, 0), 'left': (0, 1), 'right': (0, -1)}

        self.state = np.array([[1,0,0,1],[1,0,0,0],[1,0,1,0],[1,0,1,0]])
        self.actions = ['up', 'down', 'left', 'right']
        self.currScore = 0
        self.mCount = 0

        self.gamma = 0.8
        self.alpha = 0.2
        self.epsilon = 0.05



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
                temp_list, temp_score, temp_mCount = temp[0], temp[1], temp[2]
                score += temp_score
                mergeCount += temp_mCount
                temp_grid.append(temp_list)
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
                temp_list, temp_score, temp_mCount = temp[0], temp[1], temp[2]
                score += temp_score
                mergeCount += temp_mCount
                temp_grid.append(temp_list)
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
                temp_list, temp_score, temp_mCount = temp[0], temp[1], temp[2]
                score += temp_score
                mergeCount += temp_mCount
                temp_grid.append(temp_list)
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
                temp_list, temp_score, temp_mCount = temp[0], temp[1], temp[2]
                score += temp_score
                mergeCount += temp_mCount
                temp_grid.append(temp_list)
            for row in range(4):
                for col in range(4):
                    newState[row][col] = temp_grid[row][4 -1 -col]
        
        """total_num = 1
        for value in self._grid:
            for val_el in value:
                total_num *= val_el
                if total_num == 0:
                    self._is_occupied = False
                    break
                else:
                    self._is_occupied = True"""

        return (np.array(newState),score, mergeCount)



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
            if result[key] == result[key + 1]:
                result[key] = result[key] * 2
                score += result[key]
                if result[key] != 0:
                    mergeCount += 1
                result.pop(key + 1)
                result.append(0)
        return (result, score, mergeCount)


    def isTerminal(self, state):
        numFree = self.getFreePositions(state)
        if len(numFree) > 0:
            return False
        else:
            for x in range(3):
                for y in range(3):
                    if state[x][y] == state[x+1][y]:
                        return False
                    if state[x][y] == state[x-1][y]:
                        return False
                    if state[x][y] == state[x][y+1]:
                        return False
                    if state[x][y] == state[x][y-1]:
                        return False
        return True


    # This is probabbly incorrect
    """def getBest(self, state):
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
            return (maxVal, bestAction)"""

    def getBest(self, state):
        legalActions = self.getLegalActions(state)
        action = None

        if len(legalActions) == 0:
            return action
        if util.flipCoin(self.epsilon):
            return random.choice(legalActions)
        else:
            best = self.computeActionFromQValues(state)
            try:
                float(best[0])
            except:
                print "Stop it!"
            return best


    def computeActionFromQValues(self,state):
        actions = self.getLegalActions(state)
        if len(actions) == 0:
            return None
        else:
            bestAction = None
            max_val = 0
            for action in actions:
                tempVisit = self.getQValue(state, action)
                try:
                    if tempVisit >= max_val:
                        bestAction = action
                        max_val = tempVisit
                except:
                    print "Stop it!"

            return (max_val, bestAction)



    def getFeatures(self, transState):    # (state, score, mergeCount)
        feats = util.Counter()
        oneDpos = np.argmax(transState[0])

        pos = (oneDpos/4, oneDpos%4)   #(row, col)

        if pos == (3,3):
            feats["largestPos"] = 50.0
        elif pos[0] == 3:
            feats["largestPos"] = 25.0
        else:
            feats["largestPos"] = 5.0

        feats["free"] = float(16 - np.count_nonzero(transState[0]))
        #sumMergeCount = 0
        #sumScore = 0
        #for action in self.getLegalActions(transState[0]):
        #    things = self.transition(transState[0], action)
        #    sumMergeCount += things[2]
            #sumScore += things[1]

        try:
            u = float(transState[1])
        except:
            print "Stop it!"

        feats["score"] = transState[1]

        float_thing = transState[2]
        feats["mergeCount"] = float(float_thing)
        #feats["score"] = sumScore
        return feats


    def getQValue(self, state, action):
        newState = self.transition(state, action)
        self.mCount = newState[2]
        try:
            float(newState[1])
        except:
            print "Stop it!"
        feats = self.getFeatures(newState)
        dot = self.weights.__mul__(feats)
        return dot



    def updateWeights(self, state, action, reward):
        try:
            float(reward)
        except:
            print "Stop it!"

        features = self.getFeatures((state,reward, self.mCount))
        #the score is the reward

        try:
            maxVal = float(self.getBest(state)[0])
            QVal = float(self.getQValue(state, action))
        except:
            maxVal = 0
            QVal = 0
            print "Stop it!"

        difference = (reward + self.gamma*maxVal) - QVal

        for f in features.keys():
            self.weights[f] = self.weights[f] + (self.alpha*difference*features[f])



    def getLegalActions(self, state):
        legalActions = []
        for action in self.actions:
            newState = self.transition(state, action)[0]
            if not np.array_equiv(newState, state):
                legalActions.append(action)

        return legalActions