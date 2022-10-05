from Constants import *
from pygame import *
from random import *
from Vector import *
from Agent import *
from Sheep import *
from Dog import *
from Graph import *
from Node import *
from GameState import *

class StateMachine:
	""" Machine that manages the set of states and their transitions """

	def __init__(self, startState):
		""" Initialize the state machine and its start state"""
		self.__currentState = startState
		self.__currentState.enter()

	def getCurrentState(self):
		""" Get the current state """
		return self.__currentState

	def update(self, gameState):
		""" Run the update on the current state and determine if we should transition """
		nextState = self.__currentState.update(gameState)

		# If the nextState that is returned by current state's update is not the same
		# state, then transition to that new state
		if nextState != None and type(nextState) != type(self.__currentState):
			self.transitionTo(nextState)

	def transitionTo(self, nextState):
		""" Transition to the next state """
		self.__currentState.exit()
		self.__currentState = nextState
		self.__currentState.enter()

	def draw(self, screen):
		""" Draw any debugging information associated with the states """
		self.__currentState.draw(screen)

class State:
	def enter(self):
		""" Enter this state, perform any setup required """
		print("Entering " + self.__class__.__name__)
		
	def exit(self):
		""" Exit this state, perform any shutdown or cleanup required """
		print("Exiting " + self.__class__.__name__)

	def update(self, gameState):
		""" Update this state, before leaving update, return the next state """
		print("Updating " + self.__class__.__name__)

	def draw(self, screen):
		""" Draw any debugging info required by this state """
		pass

			   
class FindSheepState(State):	
	def update(self, gameState):
		super().update(gameState)
		dog = gameState.getDog()

		if dog.getTargetSheep() is None:
			closest = 0
			herd = gameState.getHerd()
			for i in range(len(herd)):
				if (herd[i].center - dog.center).length() < (herd[closest].center - dog.center).length():
					closest = i
			dog.setTargetSheep(herd[closest])
		return ApproachSheep()

class ApproachSheep(State):
	def update(self, gameState):
		super().update(gameState)
		dog = gameState.getDog()

		if (dog.getTargetSheep().center - dog.center).length() > 200:
			if not dog.isFollowingPath:
				dog.calculatePathToNewTarget(dog.getTargetSheep().center)
			return ApproachSheep()
		return SteerSheep()

class SteerSheep(State):
	def update(self, gameState):
		super().update(gameState)
		dog = gameState.getDog()
		sheep = dog.getTargetSheep()

		if sheep in gameState.getHerd():
			if sheep.center.y < 200:
				return PushIntoPen()
			return PushUpward()
		dog.setTargetSheep(None)
		return Idle()

class PushIntoPen(State):
	def update(self, gameState):
		super().update(gameState)
		dog = gameState.getDog()
		sheep = dog.getTargetSheep()

		if not dog.isFollowingPath:
			if sheep.center.y > gameState.getPenBounds()[0][1]:
				return SteerSheep()
			dog.calculatePathToNewTarget(sheep.center + 
								Vector(sheep.center.x-WORLD_WIDTH/2,0).scale(0.1) + Vector(0, -30))		
		if sheep not in gameState.getHerd():	
			return Idle()
		return PushIntoPen()

class PushUpward(State):
	def enter(self):
		super().enter()
		self.numAlt = 2
		self.alt = 0

	def update(self, gameState):
		super().update(gameState)
		dog = gameState.getDog()
		sheep = dog.getTargetSheep()

		if not dog.isFollowingPath and sheep in gameState.getHerd():
			if sheep.center.y > 150:
				if self.alt < self.numAlt:
					dog.calculatePathToNewTarget(sheep.center + Vector(-50, 30))
					self.alt += 1
				elif self.alt < self.numAlt*2:
					dog.calculatePathToNewTarget(sheep.center + Vector(50, 30))
					self.alt += 1
				else:
					self.alt = 0
				return PushUpward()
			return SteerSheep()

class Idle(State):
	def update(self, gameState):
		super().update(gameState)

		if len(gameState.getHerd()) > 0:
			return FindSheepState()
		return Idle()