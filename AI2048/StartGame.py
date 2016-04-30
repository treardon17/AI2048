from splinter import Browser
import os
import re
import pdb

browser = Browser('chrome')
currentFolderPath = os.path.dirname(os.path.abspath(__file__))
browser.visit("file:///"+currentFolderPath+"/2048-master/index.html")

"""browser.execute_script("KeyboardInputManager.moveUp()")
browser.execute_script("KeyboardInputManager.moveLeft()")
browser.execute_script("KeyboardInputManager.moveRight()")
browser.execute_script("KeyboardInputManager.moveDown()")

"""


gameState = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]] #empty gameState

def updateGameState():
    tileContainer = browser.find_by_css(".tile-container")
    allTiles = tileContainer.find_by_css(".tile")
    sortedTiles = {}

    classString = ".tile-position-"
    legalPositions = {}
    for col in xrange(1,5):
        for row in xrange(1,5):
            positionString = classString + str(col) + "-" + str(row)
            legalPositions[str(col)+"-"+str(row)] = positionString

    #fill the sortedTiles map with all the tiles at their legal position (col-row)
    for tile in allTiles:
        for pos, classPos in legalPositions.items():
            currentTilesInPos = tileContainer.find_by_css(classPos)
            if len(currentTilesInPos) == 1:
                valueOfPos = currentTilesInPos[0].find_by_css(".tile-inner")[0].value.encode("utf8")
                valueOfPos = int(valueOfPos)
                sortedTiles[pos] = valueOfPos
            elif len(currentTilesInPos) == 3:
                valueOfPos = currentTilesInPos.find_by_css(".tile-merged")[0].find_by_css(".tile-inner")[0].value.encode("utf8")
                valueOfPos = int(valueOfPos)
                sortedTiles[pos] = valueOfPos

    for row in range(1,len(gameState)):
        for col in range(1, len(gameState[row])):
            tileLocation = str(col)+"-"+str(row)
            if tileLocation in sortedTiles:
                gameState[col][row] = sortedTiles[tileLocation] 
