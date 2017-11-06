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
	newGhostStates = successorGameState.getGhostStates()
	newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
	score=successorGameState.getScore()
	foodArray=newFood.asList()

	#Taking reciprocal since closer the food higher should be the score returned

	for i in foodArray:
		foodDist = util.manhattanDistance(i,newPos)
		if (foodDist)!=0:
        		score=score+(1.0/foodDist)
	
	#Taking reciprocal since the score returned with respect to ghost is negative, closer the ghost higher should be the score 		in negative		 
	
	for ghost in newGhostStates:
		ghostpos=ghost.getPosition()
		ghostDist = util.manhattanDistance(ghostpos,newPos)
		if (abs(newPos[0]-ghostpos[0])+abs(newPos[1]-ghostpos[1]))>1:	
			score=score+(1.0/ghostDist)
		
	
	return score

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
	self.value_avg = 99999

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
    
	# New function defined to recursively traverse the minimax tree 
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
			 
			if agentNumber == 0: #pacman
				maxvalues.append((self.getAction1(successorGameState,depth1-1,num_of_agents), action))			
				maximum = max(maxvalues) 
				self.value_max = maximum[0]
				self.action1=maximum[1]	#storing the current action for the max value			
				
			else:	#ghosts
				minvalues.append((self.getAction1(successorGameState,depth1-1,num_of_agents), action))			
				minimum = min(minvalues)
				self.value_min = minimum[0]
			
		if agentNumber == 0:
			return self.value_max
		else:
			return self.value_min
	
	else:
		return self.evaluationFunction(gameState) #leaf nodes return the evaluated score

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
	#passing the initial values of alpha and beta as infinity.
	value,action = self.alpha_value(gameState,float('-inf'),float('inf'),0,self.depth) 
	return action
	
    #for pacman	
    def alpha_value(self,state,alpha,beta,agentNumber,depth):
	if state.isWin() or state.isLose():
		return self.evaluationFunction(state),'none'
		
	v = float('-inf')
	actions = state.getLegalActions(agentNumber)
	bestAction = actions[0]
		
	for action in actions:
		previous_v = v		
		successorGameState = state.generateSuccessor(agentNumber,action)
		#for leaf nodes or if the game finishes
		if depth == 0 or successorGameState.isWin() or successorGameState.isLose(): 
			v = max(v,self.evaluationFunction(successorGameState))
		else:
			v = max(v,self.beta_value(successorGameState,alpha,beta,agentNumber+1,depth))
		if v > beta:	#checking the pruning condition 
			return v,action
		alpha = max(alpha,v) 
		if v != previous_v:
			bestAction = action #to store the best action
	return v,bestAction

    #for ghosts
    def beta_value(self,state,alpha,beta,agentNumber,depth):
	if state.isWin() or state.isLose():
		return self.evaluationFunction(state),'none'
	
	v = float('inf')
	actions = state.getLegalActions(agentNumber)
	flag = False
	for action in actions:
		
		successorGameState = state.generateSuccessor(agentNumber,action)
		if depth == 0 or successorGameState.isWin() or successorGameState.isLose():
	
			v = min(v,self.evaluationFunction(successorGameState))
		elif agentNumber == (state.getNumAgents() - 1): 
			if flag == False: #flag is used to avoid decreasing depth for the same level more than once
				depth = depth -1
				flag=True
			if depth == 0: #if the last level is reached
				v = min(v,self.evaluationFunction(successorGameState))
			else:
				v = min(v,self.alpha_value(successorGameState,alpha,beta,0,depth)[0])
			
		else:	
			v = min(v,self.beta_value(successorGameState,alpha,beta,agentNumber+1,depth))
		if v < alpha: #checking the pruning condition
			return v
		beta = min(beta,v)

	return v	
		
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
	num_of_agents = gameState.getNumAgents()
	depth1 = self.depth * num_of_agents	

	self.getAction1(gameState,depth1,num_of_agents)
	return self.action1		
	util.raiseNotDefined()

    def getAction1(self,gameState,depth1,num_of_agents):
	maxvalues = list()
	chancevalues = list()
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
				chancevalues.append((self.getAction1(successorGameState,depth1-1,num_of_agents), action))			
				avg = 0.0
				for i in chancevalues:
					avg += chancevalues[chancevalues.index(i)][0]
				avg /= len(chancevalues) #returning the average of the ghost moves instead of 
				self.value_avg = avg
			
		if agentNumber == 0:
			return self.value_max
		else:
			return self.value_avg
	
	else:
		return self.evaluationFunction(gameState) #leaf nodes return the evaluated score

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

