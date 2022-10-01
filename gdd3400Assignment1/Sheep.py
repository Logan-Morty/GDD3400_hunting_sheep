import pygame
import Vector
import Agent
import Constants

from Vector import Vector
from Agent import *

class Sheep(Agent):
	"""description of class"""

	def computeNeighborhood(self, herd):
		self.neighborCnt = 0
		self.neighbors = []
		self.boundaries = []

		for sheep in herd:
			if sheep is not self:
				if (self.center - sheep.position).length() < Constants.SHEEP_NEIGHBOR_RADIUS:
					self.neighborCnt += 1
					self.neighbors += [sheep]
					
	def computeAlignment(self, herd):
		alignment = Vector(0, 0)

		for sheep in self.neighbors:
			alignment += sheep.velocity

		# if there were no neighbors
		if (self.neighborCnt == 0):
			return alignment
		else:
			return alignment.scale(1 / self.neighborCnt)

	def computeCohesion(self, herd):
		cohesion = Vector(0, 0)

		for sheep in self.neighbors:
			cohesion += sheep.position

		if self.neighborCnt > 0:
			cohesion = cohesion.scale(1 / self.neighborCnt) - self.center

		# if there were no neighbors
		return cohesion

	def computeSeparation(self, herd):
		separation = Vector(0, 0)

		for sheep in self.neighbors:
			separation += self.center - sheep.position

		# if there were no neighbors
		if (self.neighborCnt == 0):
			return separation
		else:
			return separation.scale(1 / self.neighborCnt)

	def computeDogInfluence(self, dog):
		vectToDog = self.center - dog.center
		self.target = dog
		if vectToDog.length() < Constants.MIN_ATTACK_DIST:
			self.drawDogInfluence = True
			return vectToDog
		else:
			self.drawDogInfluence = False
		return Vector(0, 0)

	def computeBoundaryInfluence(self, bounds):
		boundsInfluence = Vector(0, 0)
		self.boundaries = []

		if self.center.x < Constants.SHEEP_BOUNDARY_RADIUS:
			boundsInfluence -= Vector(0 - self.center.x, 0)
			self.boundaries += [Vector(0, self.center.y)]
		elif self.center.x > bounds.x - Constants.SHEEP_BOUNDARY_RADIUS:
			boundsInfluence -= Vector(bounds.x - self.center.x, 0)
			self.boundaries += [Vector(bounds.x, self.center.y)]

		if self.center.y < Constants.SHEEP_BOUNDARY_RADIUS:
			boundsInfluence -= Vector(0, 0 - self.center.y)
			self.boundaries += [Vector(self.center.x, 0)]
		elif self.center.y > bounds.y - Constants.SHEEP_BOUNDARY_RADIUS:
			boundsInfluence -= Vector(0, bounds.y - self.center.y)
			self.boundaries += [Vector(self.center.x, bounds.y)]

		return boundsInfluence

	def computeObstacleInfluence(self, obstacles):
		obstacleInfluence = Vector(0, 0)
		obstacleCount = 0
		self.obstacles = []
		self.obstacleForces = []

		for obstacle in obstacles:
			vectToObstacle =  self.center - obstacle.center
			if vectToObstacle.length() < Constants.SHEEP_OBSTACLE_RADIUS:
				self.obstacles += [obstacle]
				self.obstacleForces += [vectToObstacle]
				obstacleInfluence += vectToObstacle.normalize().scale(1 / vectToObstacle.length())
		return obstacleInfluence			

	def update(self, bounds, graph, dog, herd, gates):
		self.computeNeighborhood(herd)

		alignment = self.computeAlignment(herd).normalize()
		separation = self.computeSeparation(herd).normalize()
		cohesion = self.computeCohesion(herd).normalize()
		dogInfluence = self.computeDogInfluence(dog).normalize()
		boundsInfluence = self.computeBoundaryInfluence(bounds).normalize()
		obstacleInfluence = self.computeObstacleInfluence(graph.obstacles).normalize()

		direction = alignment.scale(Constants.SHEEP_ALIGNMENT_WEIGHT) \
					+ separation.scale(Constants.SHEEP_SEPARATION_WEIGHT) \
					+ cohesion.scale(Constants.SHEEP_COHESION_WEIGHT) \
					+ dogInfluence.scale(Constants.SHEEP_DOG_INFLUENCE_WEIGHT) \
					+ boundsInfluence.scale(Constants.SHEEP_BOUNDARY_INFLUENCE_WEIGHT) \
					+ obstacleInfluence.scale(Constants.SHEEP_OBSTACLE_INFLUENCE_WEIGHT)

		# If velocity is zero, keep the old velocity but set the speed to zero
		if abs(direction.x) < 0.000001 and abs(direction.y) < 0.000001:
			self.speed = 0
		else:
			self.setVelocity(direction)
			self.speed = self.maxSpeed
		super().update(bounds, graph, [dog] + [herd])


	def draw(self, screen):
		super().draw(screen)

		if self.drawDogInfluence and Constants.DEBUG_DOG_INFLUENCE:
			pygame.draw.line(screen, (255, 0, 0), (self.center.x, self.center.y), 
				(self.target.center.x, self.target.center.y), Constants.DEBUG_LINE_WIDTH)

		if Constants.DEBUG_NEIGHBORS:
			for sheep in self.neighbors:
				pygame.draw.line(screen, (0, 0, 255), (self.center.x, self.center.y), 
								 (sheep.center.x, sheep.center.y), Constants.DEBUG_LINE_WIDTH)
		
		if Constants.DEBUG_BOUNDARIES:
			for boundary in self.boundaries:
				pygame.draw.line(screen, (255, 0, 255), (self.center.x, self.center.y), 
								 (boundary.x, boundary.y), Constants.DEBUG_LINE_WIDTH)

		if Constants.DEBUG_OBSTACLES:
			for obstacle in self.obstacles:
				pygame.draw.line(screen, (0, 255, 255), (self.center.x, self.center.y),
								 (obstacle.center.x, obstacle.center.y), Constants.DEBUG_LINE_WIDTH)
