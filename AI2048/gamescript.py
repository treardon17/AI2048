import sys, pdb,os

#from reinforcement import Reinforcement
#from Expectimax import Expectimax
from ExpectimaxJoseph import Expectimax

if "--no-graphics" in sys.argv:
    #from gameBoard import Gameboard
    #game = Gameboard()
    from gameGit import TwentyFortyEight
    game = TwentyFortyEight(4,4)
    noG = True
else:
    from GameInteraction import GameInteraction
    game = GameInteraction()
    noG = False

#agent = Reinforcement()
agent = Expectimax()
currentGameState = game.getGameState()

while not agent.isTerminal(currentGameState):
    #if noG:
        #game.printBoard()
        #pdb.set_trace()


    #best = agent.getBest(currentGameState) #gets the best action and the maxVal
    bestAction = agent.getBest(currentGameState) #gets the best action and the maxVal
    #maxVal = best[0]
    #bestAction = best[1]

    if bestAction == None:
        print "All done!!"
        break

    #agent.updateWeights(currentGameState, bestAction, maxVal)
    game.move(bestAction)
    #agent.score = game.getScore()

    if noG:
        game.printBoard()
        print "[+] Best Action:", bestAction
        #pdb.set_trace()
    currentGameState = game.getGameState()
