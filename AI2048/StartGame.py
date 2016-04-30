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
    for pos, classPos in legalPositions.items():
        currentTilesInPos = tileContainer.find_by_css(classPos)
        if len(currentTilesInPos) == 1:
            valueOfPos = currentTilesInPos[0].find_by_css(".tile-inner")[0].value.encode("utf8")
            try:
                valueOfPos = int(valueOfPos)
                sortedTiles[pos] = valueOfPos
            except:
                print "[-]: valueOfPos:",valueOfPos
            print "pos: ",pos
        elif len(currentTilesInPos) == 3:
            valueOfPos = currentTilesInPos.find_by_css(".tile-merged")[0].find_by_css(".tile-inner")[0].value.encode("utf8")
            try:
                valueOfPos = int(valueOfPos)
                sortedTiles[pos] = valueOfPos
            except:
                print "[-]: valueOfPos:",valueOfPos
        else:
            sortedTiles[pos] = 0


    for row in range(0,len(gameState)):
        for col in range(0, len(gameState[row])):
            tileLocation = str(col+1)+"-"+str(row+1)
            gameState[row][col] = sortedTiles[tileLocation]
            print "tileLocation: ",tileLocation



updateGameState()

for row in gameState:
    print row
