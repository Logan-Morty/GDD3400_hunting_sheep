import Constants
import Node
import pygame
import Vector

from pygame import *
from Vector import *
from Node import *
from enum import Enum

class SearchType(Enum):
	BREADTH = 0
	DJIKSTRA = 1
	A_STAR = 2
	BEST_FIRST = 3

class Graph():
	def __init__(self):
		""" Initialize the Graph """
		self.nodes = []			# Set of nodes
		self.obstacles = []		# Set of obstacles - used for collision detection

		# Initialize the size of the graph based on the world size
		self.gridWidth = int(Constants.WORLD_WIDTH / Constants.GRID_SIZE)
		self.gridHeight = int(Constants.WORLD_HEIGHT / Constants.GRID_SIZE)

		# Create grid of nodes
		for i in range(self.gridHeight):
			row = []
			for j in range(self.gridWidth):
				node = Node(i, j, Vector(Constants.GRID_SIZE * j, Constants.GRID_SIZE * i), Vector(Constants.GRID_SIZE, Constants.GRID_SIZE))
				row.append(node)
			self.nodes.append(row)

		## Connect to Neighbors
		for i in range(self.gridHeight):
			for j in range(self.gridWidth):
				# Add the top row of neighbors
				if i - 1 >= 0:
					# Add the upper left
					if j - 1 >= 0:		
						self.nodes[i][j].neighbors += [self.nodes[i - 1][j - 1]]
					# Add the upper center
					self.nodes[i][j].neighbors += [self.nodes[i - 1][j]]
					# Add the upper right
					if j + 1 < self.gridWidth:
						self.nodes[i][j].neighbors += [self.nodes[i - 1][j + 1]]

				# Add the center row of neighbors
				# Add the left center
				if j - 1 >= 0:
					self.nodes[i][j].neighbors += [self.nodes[i][j - 1]]
				# Add the right center
				if j + 1 < self.gridWidth:
					self.nodes[i][j].neighbors += [self.nodes[i][j + 1]]
				
				# Add the bottom row of neighbors
				if i + 1 < self.gridHeight:
					# Add the lower left
					if j - 1 >= 0:
						self.nodes[i][j].neighbors += [self.nodes[i + 1][j - 1]]
					# Add the lower center
					self.nodes[i][j].neighbors += [self.nodes[i + 1][j]]
					# Add the lower right
					if j + 1 < self.gridWidth:
						self.nodes[i][j].neighbors += [self.nodes[i + 1][j + 1]]

	def getNodeFromPoint(self, point):
		""" Get the node in the graph that corresponds to a point in the world """
		point.x = max(0, min(point.x, Constants.WORLD_WIDTH - 1))
		point.y = max(0, min(point.y, Constants.WORLD_HEIGHT - 1))

		# Return the node that corresponds to this point
		return self.nodes[int(point.y/Constants.GRID_SIZE)][int(point.x/Constants.GRID_SIZE)]

	def placeObstacle(self, point, color):
		""" Place an obstacle on the graph """
		node = self.getNodeFromPoint(point)

		# If the node is not already an obstacle, make it one
		if node.isWalkable:
			# Indicate that this node cannot be traversed
			node.isWalkable = False		

			# Set a specific color for this obstacle
			node.color = color
			for neighbor in node.neighbors:
				neighbor.neighbors.remove(node)
			node.neighbors = []
			self.obstacles += [node]

	def reset(self):
		""" Reset all the nodes for another search """
		for i in range(self.gridHeight):
			for j in range(self.gridWidth):
				self.nodes[i][j].reset()

	def buildPath(self, endNode):
		""" Go backwards through the graph reconstructing the path """
		path = []
		node = endNode
		while node is not 0:
			node.isPath = True
			path = [node] + path
			node = node.backNode

		# If there are nodes in the path, reset the colors of start/end
		if len(path) > 0:
			path[0].isPath = False
			path[0].isStart = True
			path[-1].isPath = False
			path[-1].isEnd = True
		return path

	def findPath_Breadth(self, start, end):
		""" Breadth Search """
		#print("BREADTH-FIRST")
		self.reset()

		toVisit = []
		startNode = self.getNodeFromPoint(start)
		startNode.isVisited = True
		toVisit.append(startNode)
		endNode = self.getNodeFromPoint(end)


		while toVisit:
			currentNode = toVisit.pop(0)
			currentNode.isExplored = True
		
			for neighbor in currentNode.neighbors:
				if neighbor is endNode:
					neighbor.backNode = currentNode
					return self.buildPath(neighbor)
					
				if not neighbor.isVisited:
					neighbor.backNode = currentNode
					toVisit.append(neighbor)
					neighbor.isVisited = True

		# Return empty path indicating no path was found
		return []

	def findPath_Djikstra(self, start, end):
		""" Djikstra's Search """
		#print("DJIKSTRA")
		self.reset()

		toVisit = []
		startNode = self.getNodeFromPoint(start)
		startNode.isVisited = True
		startNode.costFromStart = 0
		startNode.costToEnd = 0
		startNode.cost = startNode.costFromStart + startNode.costToEnd
		toVisit.append(startNode)
		endNode = self.getNodeFromPoint(end)


		while toVisit:
			currentNode = toVisit.pop(0)
			currentNode.isExplored = True

			if currentNode is endNode:
				return self.buildPath(currentNode)
			
			for neighbor in currentNode.neighbors:
				currCost = ((currentNode.center.x - neighbor.center.x)**2 + 
						 (currentNode.center.y - neighbor.center.y)**2)**0.5
				if not neighbor.isVisited:
					neighbor.isVisited = True
					neighbor.costFromStart = currCost + currentNode.costFromStart
					neighbor.costToEnd = 0
					neighbor.cost = neighbor.costFromStart + neighbor.costToEnd
					neighbor.backNode = currentNode
					toVisit.append(neighbor)
					toVisit = sorted(toVisit, key=lambda x: x.cost)
				elif currCost + currentNode.cost < neighbor.cost:
					neighbor.cost = currCost + currentNode.cost
					neighbor.backNode = currentNode

		# Return empty path indicating no path was found
		return []

	def findPath_AStar(self, start, end):
		""" A Star Search """
		#print("A_STAR")
		self.reset()

		toVisit = []
		startNode = self.getNodeFromPoint(start)
		startNode.isVisited = True
		startNode.costFromStart = 0
		startNode.costToEnd = 0
		startNode.cost = startNode.costFromStart + startNode.costToEnd
		toVisit.append(startNode)
		endNode = self.getNodeFromPoint(end)

		while toVisit:
			currentNode = toVisit.pop(0)
			currentNode.isExplored = True

			if currentNode is endNode:
				return self.buildPath(currentNode)
			
			for neighbor in currentNode.neighbors:
				costCalc = lambda x, y: ((x - neighbor.center.x)**2 + (y - neighbor.center.y)**2)**0.5
				currCost = costCalc(currentNode.center.x, currentNode.center.y)
				if not neighbor.isVisited:
					neighbor.isVisited = True
					neighbor.costFromStart = currCost + currentNode.costFromStart
					neighbor.costToEnd = neighbor.costToEnd = costCalc(endNode.center.x, endNode.center.y)
					neighbor.cost = neighbor.costFromStart + neighbor.costToEnd
					neighbor.backNode = currentNode
					toVisit.append(neighbor)
					toVisit = sorted(toVisit, key=lambda x: x.cost)
				elif currCost + currentNode.cost < neighbor.costFromStart:
					neighbor.costFromStart = currCost + currentNode.cost
					neighbor.cost = neighbor.costFromStart + neighbor.costToEnd
					print("cost to end", neighbor.costToEnd)
					neighbor.backNode = currentNode

		# TODO: Implement A Star Search
		
		# Return empty path indicating no path was found
		return []

	def findPath_BestFirst(self, start, end):
		""" Best First Search """
		#print("BEST_FIRST")
		self.reset()

		toVisit = []
		startNode = self.getNodeFromPoint(start)
		startNode.isVisited = True
		startNode.costFromStart = 0
		startNode.costToEnd = 0
		startNode.cost = startNode.costFromStart + startNode.costToEnd
		toVisit.append(startNode)
		endNode = self.getNodeFromPoint(end)

		while toVisit:
			currentNode = toVisit.pop(0)
			currentNode.isExplored = True

			if currentNode is endNode:
				return self.buildPath(currentNode)
			
			for neighbor in currentNode.neighbors:
				if not neighbor.isVisited:
					neighbor.isVisited = True
					neighbor.costFromStart = 0
					neighbor.costToEnd = ((endNode.center.x - neighbor.center.x)**2 + 
						 (endNode.center.y - neighbor.center.y)**2)**0.5
					neighbor.cost = neighbor.costFromStart + neighbor.costToEnd
					neighbor.backNode = currentNode
					toVisit.append(neighbor)
					toVisit = sorted(toVisit, key=lambda x: x.cost)
		# Return empty path indicating no path was found
		return []

	def draw(self, screen):
		""" Draw the graph """
		for i in range(self.gridHeight):
			for j in range(self.gridWidth):
				self.nodes[i][j].draw(screen)