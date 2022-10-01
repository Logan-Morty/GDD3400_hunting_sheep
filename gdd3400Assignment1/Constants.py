FRAME_RATE = 60
WORLD_WIDTH = 1024
WORLD_HEIGHT = 768
BACKGROUND_COLOR = (100, 149, 237)

GATE_COUNT = 4
GATE_WIDTH = 100
GATES = [ [ [104, 552], [104, 664] ], \
	      [ [104, 216], [104, 104] ], \
		  [ [808, 616], [696, 616] ], \
		  [ [936, 152], [824, 152] ], \
		  #[ [456, 440], [456, 328] ]  ]		# vertical, green is on bottom (backwards c)
		  #[ [568, 328], [568, 440] ]  ]		# vertical, green is on top (c)
		  [ [456, 328], [568, 328] ]  ]	# horizontal, green on left (u)
		  #[ [568, 440], [456, 440] ]  ]	# horizontal, green on right (n)
		  
NBR_RANDOM_OBSTACLES = 40

DOG_HEIGHT = 32
DOG_WIDTH = 16
DOG_SPEED = 5
DOG_ANGULAR_SPEED = 1

SHEEP_COUNT = 1
SHEEP_HEIGHT = 32
SHEEP_WIDTH = 16
SHEEP_SPEED = 5
SHEEP_ANGULAR_SPEED = .2

# Flocking Behavior
SHEEP_NEIGHBOR_RADIUS = 50
SHEEP_BOUNDARY_RADIUS = 50
SHEEP_OBSTACLE_RADIUS = 50
SHEEP_ALIGNMENT_WEIGHT = 0.3
SHEEP_SEPARATION_WEIGHT = 0.325
SHEEP_COHESION_WEIGHT = 0.3
SHEEP_DOG_INFLUENCE_WEIGHT = 0.3
SHEEP_BOUNDARY_INFLUENCE_WEIGHT = 0.5
SHEEP_OBSTACLE_INFLUENCE_WEIGHT = 0.3

MIN_ATTACK_DIST = 100

DEBUGGING = True
DEBUG_LINE_WIDTH = 1
DEBUG_BOUNDING_RECTS = DEBUGGING
DEBUG_VELOCITY = DEBUGGING
DEBUG_NEIGHBORS = DEBUGGING
DEBUG_BOUNDARIES = DEBUGGING
DEBUG_DOG_INFLUENCE = DEBUGGING
DEBUG_OBSTACLES = DEBUGGING
DEBUG_GRID_LINES = True
DEBUG_NEIGHBOR_LINES = False

# Graph Constants
GRID_SIZE = 16
