# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
	newPos = successorGameState.getPacmanPosition()
	currentpos= currentGameState.getPacmanPosition()
	newFood = successorGameState.getFood()
	distances=list()
	foodDistances = list()
	count = 0
	for food in newFood:
		for i in range(len(food)):
			if food[i]==True:
	 			distances.append((i,count)) #all food coordinates
		count = count+1

	for i in distances:
		foodDistances.append(abs(newPos[0]-i[0])+abs(newPos[1]-i[1])) #distances from the current position to the food coordinates
	if len(foodDistances)>0:
		minFoodDistance=min(foodDistances) #minimum food distance
	else:	
		minFoodDistance=foodDistances   
	
	newGhostStates = successorGameState.getGhostStates()
	newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
	ghostpos = currentGameState.getGhostPosition(1)

 		        		
	tempPosition = currentpos
	minDist=999
	totalDist=0

	while len(distances) > 0:
    		for i in distances:
    			if (abs(tempPosition[0]-i[0])  + abs(tempPosition[1] - i[1])) < minDist:
				minDist = abs(tempPosition[0]-i[0])  + abs(tempPosition[1] - i[1])
				value = i
				indx = distances.index(value)
		tempPosition = value
	    	totalDist=totalDist+minDist
	    	distances.remove(tempPosition)
		minDist = 99999


	#	print newGhostStates
	#for ghost in newGhostStates:
		#ghostpos=ghost.getPosition()	
	
	ghostDistance = (abs(currentpos[0]-ghostpos[0])+abs(currentpos[1]-ghostpos[1]))
	
	score=0

	"*** YOUR CODE HERE ***"
	if action==Directions.STOP:
		score+= -10	

	if (currentGameState.getNumFood() > successorGameState.getNumFood()):
		score += 100
	if totalDist>0:
		score += (1/(totalDist))*100
		if ghostDistance == 0:
			score += -100
	
        else:
		score += 100
		
	return successorGameState.getScore()+score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
	self.action1 = Directions.STOP
	self.value_max = -99999
	self.value_min = 99999

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
	
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
	num_of_agents = gameState.getNumAgents()
	depth1 = self.depth * num_of_agents	

	self.getAction1(gameState,depth1,num_of_agents)
	return self.action1		
	util.raiseNotDefined()

    def getAction1(self,gameState,depth1,num_of_agents):
	maxvalues = list()
	minvalues = list()
	if gameState.isWin() or gameState.isLose():
		return self.evaluationFunction(gameState)
			
	if depth1 > 0:
		if depth1%num_of_agents ==0:
			agentNumber = 0
				
		else: 
			agentNumber = num_of_agents-(depth1%num_of_agents)
		
		actions = gameState.getLegalActions(agentNumber)
		for action in actions:
			successorGameState = gameState.generateSuccessor(agentNumber,action)
			 
			if agentNumber == 0:
				maxvalues.append((self.getAction1(successorGameState,depth1-1,num_of_agents), action))			
				maximum = max(maxvalues)
				self.value_max = maximum[0]
				self.action1=maximum[1]				
				
			else:	
				minvalues.append((self.getAction1(successorGameState,depth1-1,num_of_agents), action))			
				minimum = min(minvalues)
				self.value_min = minimum[0]
			
		if agentNumber == 0:
			return self.value_max
		else:
			return self.value_min
	
	else:
		return self.evaluationFunction(gameState)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
	num_of_agents = gameState.getNumAgents()
	depth1 = self.depth * num_of_agents	
	alpha = -99999
	beta = 99999
	self.getAction1(gameState,depth1,num_of_agents,alpha,beta)
	return self.action1		
	util.raiseNotDefined()

    def getAction1(self,gameState,depth1,num_of_agents,alpha,beta):
	alpha_values = list()
	beta_values = list()
	alpha_values.append((-99999,None))
	beta_values.append((99999,None))
	if gameState.isWin() or gameState.isLose():
		return self.evaluationFunction(gameState)
			
	if depth1 > 0:
		if depth1%num_of_agents ==0:
			agentNumber = 0
				
		else: 
			agentNumber = num_of_agents-(depth1%num_of_agents)
		
		actions = gameState.getLegalActions(agentNumber)

		for action in actions:
			 
			if agentNumber == 0:
				if alpha <= beta:
					
					successorGameState = gameState.generateSuccessor(agentNumber,action)
				
					alpha_values.append((self.getAction1(successorGameState,depth1-1,num_of_agents,alpha,beta), action))			
					alpha_max = max(alpha_values)
					alpha = alpha_max[0]
					self.action1=alpha_max[1]
				else:
					break
									
				
			else:	
				if alpha <= beta:
					
					successorGameState = gameState.generateSuccessor(agentNumber,action)
			
					beta_values.append((self.getAction1(successorGameState,depth1-1,num_of_agents,alpha,beta), action))			
					beta_min = min(beta_values)
					beta = beta_min[0]
				else:
					break
					
	
		if agentNumber == 0:
			return alpha
		else:
			return beta
	
	else:
		return self.evaluationFunction(gameState)

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

