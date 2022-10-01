import pygame
import Vector
import Agent

from Vector import Vector
from Agent import *
from enum import Enum
from pygame import *

class SearchType(Enum):
	BREADTH = 1
	DJIKSTRA = 2
	BEST = 3
	A_STAR = 4

class Player(Agent):

	def __init__(self, image, position, size, color, speed, angularSpeed):
		super().__init__(image, position, size, color, speed, angularSpeed)
		self.searchType = SearchType.A_STAR
		self.gateNumber = 0
		self.isFollowingPath = False
		self.path = []

	def calculateHerdPosition(self, herd):
		position = Vector(0, 0)
		for sheep in herd:
			position += sheep.center

		return position.scale(1 / len(herd))

	def update(self, bounds, graph, herd, gates):
		if pygame.key.get_pressed()[K_f]:
			self.searchType = SearchType.BREADTH
		elif pygame.key.get_pressed()[K_d]:
			self.searchType = SearchType.DJIKSTRA
		elif pygame.key.get_pressed()[K_s]:
			self.searchType = SearchType.BEST
		elif pygame.key.get_pressed()[K_a]:
			self.searchType = SearchType.A_STAR

		# If we are not following the path, find the sheep
		if not self.isFollowingPath:
			# Find the sheep and head toward the sheep
			herdPosition = self.calculateHerdPosition(herd)

			if self.searchType == SearchType.BREADTH:
				self.path = graph.findPath_Breadth(self.center, herdPosition)
			elif self.searchType == SearchType.DJIKSTRA:
				self.path = graph.findPath_Djikstra(self.center, herdPosition)
			elif self.searchType == SearchType.BEST:
				self.path = graph.findPath_BestFirst(self.center, herdPosition)
			elif self.searchType == SearchType.A_STAR:
				self.path = graph.findPath_AStar(self.center, herdPosition)

			if len(self.path) > 0:
				self.isFollowingPath = True
				self.target = self.path.pop(0).center
				self.speed = self.maxSpeed

		# If we are following the path
		else:
			vectorToTarget = self.target - self.center
			# if we've arrived at the first location in the path
			if (vectorToTarget).length() <= Constants.GRID_SIZE * .5:
				# Go to next position in path, if there is one
				if len(self.path) > 0:
					self.target = self.path.pop(0).center
				# Stop following the path if it is empty
				else:
					self.isFollowingPath = False
					self.speed = 0
			else:
				self.setVelocity(vectorToTarget)

		## If we need a new goal
		#if not self.isFollowingPath:
		#	# Find the herd position
		#	herdPosition = self.calculateHerdPosition(herd)

		#	# Find a position on the opposite side of the gate to which to drive the sheep
		#	gateVector = (Vector(gates[self.gateNumber][0][0], gates[self.gateNumber][0][1]) \
		#			     - Vector(gates[self.gateNumber][1][0], gates[self.gateNumber][1][1])).normalize()
		#	gateMidPoint = (Vector(gates[self.gateNumber][0][0], gates[self.gateNumber][0][1]) 
		#					+ Vector(gates[self.gateNumber][1][0], gates[self.gateNumber][1][1])).scale(.5)
		#	gateGoalPoint = gateMidPoint + Vector(-gateVector.y, gateVector.x).scale(Constants.Grid_Size * 3)

		#	# Find the vector between the sheep and the gate
		#	gateToSheep = (herdPosition - gateMidPoint).normalize()

		#	# Determine if we need to go to the next gate


		#	# Aim to get the sheep 2 units BEYOND the gate
		#	self.targetGatePoint = gateMidPoint + gateToSheep.Scale(Constants.GRID_SIZE * 2)

		#	# if the herd is through the gate, pick the next gate
		#	if (len(herdPosition) < 3):

		#	newDogPosition = herdPosition + gateToSheep.scale(Constants.MIN_ATTACK_DIST) - Vector(Constants.GRID_SIZE, Constants.GRID_SIZE)

		#	if self.searchType == SearchType.BREADTH:
		#		self.path = graph.findPath_Breadth(self.position, newDogPosition)
		#	elif self.searchType == SearchType.DJIKSTRA:
		#		self.path = graph.findPath_Djikstra(self.position, newDogPosition)
		#	elif self.searchType == SearchType.BEST:
		#		self.path = graph.findPath_BestFirst(self.position, newDogPosition)
		#	elif self.searchType == SearchType.A_STAR:
		#		self.path = graph.findPath_AStar(self.position, newDogPosition)

		#	if len(self.path) > 0:
		#		self.isFollowingPath = True
		#		self.target = self.path.pop(0).center



		super().update(bounds, graph, [self] + [herd])