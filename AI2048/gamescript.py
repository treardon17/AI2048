from GameInteraction import GameInteraction
from reinforcement import Agent

game = GameInteraction()
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
