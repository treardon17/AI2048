import reinforcement
import numpy as np
import random, os, util

class Gameboard:
    def __init__(self):
        self.board = np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
        random.seed(None)
        self.possibleRandomVals = [2,4]
        self.score = 0
        self.newTile = 0


    def randomNewTile(self):
        numEmptyCells = 16 - np.count_nonzero(self.board)

        posRand = random.randint(1,numEmptyCells)

        count = 0
        for x in range(0, 4):
            for y in range(0, 4):
                if self.board[x][y] == 0:
                    count += 1
                if count == posRand:
                    self.newTile = self.possibleRandomVals[random.randint(0,len(self.possibleRandomVals) -1)]
                    self.board[x][y] = self.newTile


    def printBoard(self):
        os.system("cls")
        for x in self.board:
            for y in x:
                print '{0:3}'.format(y),
            print
        print "-------------------"
        print "[+] Score:", self.score
        print "[+] NewTile:", self.newTile

    def updateScore(self, newPoints):
        self.score += newPoints

    def getGameState(self):
        self.randomNewTile()
        return self.board

    def move(self, action):
        # The merging doesn't work correctly. It merges multiple things at a time.
        # [4,0,4,8] => [0,0,0,16]
        score = 0
        mergeCount = 0
        newState = [[], [], [], []]
        index = 0
        state = self.board
        if action == "left" or action == "up":
            index = 3
        if action == "up" or action == "down":
            state = self.board.T

        i = 0
        for x in state:
            if index == 3:
                for y in x:
                    if y != 0:
                        if y in newState[i]:
                            newState[i][newState[i].index(y)] = 2 * y
                            score += 2 * y
                            mergeCount += 1
                        else:
                            newState[i].insert(index, y)
            else:
                for y in reversed(x):
                    if y != 0:
                        if y in newState[i]:
                            newState[i].reverse()
                            newState[i][newState[i].index(y)] = 2 * y
                            newState[i].reverse()
                            score += 2 * y
                            mergeCount += 1
                        else:
                            newState[i].insert(index, y)
            i += 1

        for x in newState:
            while len(x) < 4:
                x.insert(index, 0)

        if action == 'up' or action == 'down':
            self.board = np.array(newState).T
            self.score += score
        else:
            self.board = np.array(newState)
            self.score += score

    def getScore(self):
        return self.score