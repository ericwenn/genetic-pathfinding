import string
import random
import math

class DNA(object):
	def __init__(self, start_pos, target_pos, flowfield_dim, obstacles):
		self.start_pos = start_pos
		self.pos = start_pos
		self.velocity = (0,0)
		self.target_pos = target_pos
		self.flowfield_dim = flowfield_dim
		self.step = 0
		self.obstacles = obstacles
		self.hit_obstacle = 0
		self.finished = 0
		self.time_to_completion = 0
		self.time_alive = 0

		self.best_distance = float("inf")

		self.dna = []
		for i in range(flowfield_dim):
			self.dna.append([])







	def generate_dna(self):
		for y in range(self.flowfield_dim):
			for x in range(self.flowfield_dim):
				self.dna[x].append( self.random_vector() )


	def random_vector(self):
		x = random.random() * 2 - 1
		y = random.random() * 2 - 1

		vec_abs = math.sqrt( math.pow(x,2) + math.pow(y,2))

		x = x / vec_abs
		y = y / vec_abs



		return (x,y)




	def calc_fitness(self, target_pos, total_distance):



		factor = 1
		if( self.finished == 1):
			self.best_distance = 1
			factor = 2
			
		self.fitness = math.pow(factor/float(self.best_distance * self.time_to_completion),4)


		if( self.hit_obstacle == 1):
			self.fitness =  0


	def get_fitness(self):
		return self.fitness

	def crossover(self, partner):

		child = DNA(self.start_pos, self.target_pos, self.flowfield_dim, self.obstacles)

		for x in range(self.flowfield_dim):
			for y in range(self.flowfield_dim):

				if (random.random() < 0.5):
					child.dna[x].append(self.dna[x][y])
				else:
					child.dna[x].append(partner.dna[x][y])

		return child


	def mutate(self, mutation_prob):
		for x in range(self.flowfield_dim):
			for y in range(self.flowfield_dim):
				if( random.random() < mutation_prob ):
					self.dna[x][y] = self.random_vector()

	def clone( self ):
		child = DNA(self.start_pos, self.target_pos, self.flowfield_dim, self.obstacles)
		child.dna = self.dna
		return child



	def _step(self):
		flowfield_x = int(self.pos[0] / 20)
		flowfield_y = int(self.pos[1] / 20)


		if( flowfield_x < 0 or flowfield_x > self.flowfield_dim - 1 or flowfield_y < 0 or flowfield_y > self.flowfield_dim - 1 ):
			shouldMove = False
		else:
			self.velocity = self.dna[flowfield_x][flowfield_y]
			shouldMove = True

		oldPos = self.pos

		if(self.finished == 0 and self.hit_obstacle == 0 and shouldMove):
			self.pos = ( int(self.pos[0] + self.velocity[0]*5), int(self.pos[1] + self.velocity[1]*5) )
			distance = math.sqrt( math.pow(self.target_pos[0] - self.pos[0],2) + math.pow(self.target_pos[1] - self.pos[1], 2))
			if distance < self.best_distance:
				self.best_distance = distance

			self.time_alive += 1
			self.time_to_completion += 1

			for o in range(len(self.obstacles)):
				if(self.obstacles[o].contains(self.pos)):
					self.hit_obstacle = 1

			if( math.fabs(self.pos[0] - self.target_pos[0]) < 3 and math.fabs(self.pos[1] - self.target_pos[1]) < 3):
				self.time_to_completion = self.step
				self.finished = 1

		if( self.hit_obstacle == 1 or not shouldMove):
			self.time_to_completion += 1

		self.step += 1



	def _pos(self):
		return self.pos


