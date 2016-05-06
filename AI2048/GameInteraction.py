from splinter import Browser
import numpy as np
import time
import os
import re
import pdb

class GameInteraction:

    def __init__(self):
        self.browser = Browser('chrome')
        currentFolderPath = os.path.dirname(os.path.abspath(__file__))
        self.browser.visit("file:///"+currentFolderPath+"/2048-master/index.html")

    def getGameState(self):
        gameState = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]  # empty gameState

        tileContainer = self.browser.find_by_css(".tile-container")
        allTiles = tileContainer.find_by_css(".tile")
        sortedTiles = {}

        classString = ".tile-position-"
        legalPositions = {}
        for col in xrange(1,5):
            for row in xrange(1,5):
                positionString = classString + str(col) + "-" + str(row)
                legalPositions[str(col)+"-"+str(row)] = positionString
                sortedTiles[str(col)+"-"+str(row)] = 0


        #fill the sortedTiles map with all the tiles at their legal position (col-row)
        for pos, classPos in legalPositions.items():
            #time.sleep(0.3) #let the web browser catch up
            currentTilesInPos = tileContainer.find_by_css(classPos)
            if len(currentTilesInPos) == 1:
                valueOfPos = currentTilesInPos[0].find_by_css(".tile-inner")[0].value.encode("utf8")
                try:
                    valueOfPos = int(valueOfPos)
                    sortedTiles[pos] = valueOfPos
                except:
                    pdb.set_trace()
                    print "[-]: valueOfPos (1 tile):",valueOfPos
            elif len(currentTilesInPos) == 3:
                #valueOfPos = currentTilesInPos.find_by_css(".tile-merged")[0].find_by_css(".tile-inner")[0].value.encode("utf8")
                mergedTiles = tileContainer.find_by_css(classPos+".tile-merged")
                innerTile = mergedTiles[0].find_by_css(".tile-inner")[0].value.encode("utf8")
                try:
                    valueOfPos = int(innerTile)
                    sortedTiles[pos] = valueOfPos
                except:
                    pdb.set_trace()
                    print "[-] mergedTiles:", mergedTiles
                    print "[-] innerTile:", innerTile
                    print "[-] valueOfPos (merged):",valueOfPos
            else:
                sortedTiles[pos] = 0

        try:
            for row in range(0,len(gameState)):
                for col in range(0, len(gameState[row])):
                    tileLocation = str(col+1)+"-"+str(row+1)
                    gameState[row][col] = sortedTiles[tileLocation]
        except:
            pdb.set_trace()

        return np.array(gameState)

    def getScore(self):
        score = self.browser.find_by_css(".score-container").value
        print "[+] score:",score
        splitScore = score.split("+")
        return int(splitScore[0])

    def move(self, action):
        if action == "up":
            self.browser.execute_script("KeyboardInputManager.moveUp()")
        elif action == "down":
            self.browser.execute_script("KeyboardInputManager.moveDown()")
        elif action == "left":
            self.browser.execute_script("KeyboardInputManager.moveLeft()")
        elif action == "right":
            self.browser.execute_script("KeyboardInputManager.moveRight()")
        else:
            print "[!] invalid action:", action
