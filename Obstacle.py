class Obstacle(object):
	def __init__(self, x,y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height


	def contains(self, pos):
		return pos[0] < self.x + self.width and pos[0] > self.x and pos[1] < self.y + self.height and pos[1] > self.y
		