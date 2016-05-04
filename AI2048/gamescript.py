import sys, pdb

from reinforcement import Agent

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

agent = Agent()
currentGameState = game.getGameState()

while not agent.isTerminal(currentGameState):
    best = agent.getBest(currentGameState) #gets the best action and the maxVal
    maxVal = best[0]
    bestAction = best[1]

    agent.updateWeights(currentGameState, bestAction, maxVal)
    game.move(bestAction)
    agent.currScore = game.getScore()

    currentGameState = game.getGameState()

print currentGameState
