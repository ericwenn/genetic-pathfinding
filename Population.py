from DNA import DNA
import random
import math

class Population(object):
	def __init__(self, pop_size, variation, elite_size, target_pos, start_pos, flowfield_dim, obstacles):
		
		self.pop_size = pop_size
		self.variation = variation
		self.elite_size = elite_size
		self.target = target_pos
		self.start_pos = start_pos
		self.flowfield_dim = flowfield_dim
		self.obstacles = obstacles
		self.population = []
		self.mating_pool = []
		self.generations = 0


		self.elites = []

		self.total_distance = math.sqrt( math.pow(target_pos[0] - start_pos[0], 2) + math.pow(target_pos[1] - start_pos[1], 2))

		for i in range(pop_size):
			self.population.append(DNA(start_pos, target_pos, flowfield_dim, obstacles))
			self.population[i].generate_dna()



		
	
	def calcFitness(self):
		for i in range(self.pop_size):
			self.population[i].calc_fitness(self.target, self.total_distance)



	def natural_selection(self):
		self.mating_pool = []
		self.fit_list = []
		self.elites = sorted(self.population, key=lambda dna: -dna.fitness)
		max_fitness = self.elites[0].get_fitness()




		for i in range(self.pop_size):
			times_to_add = 100 * self.population[i].get_fitness()  / max_fitness
			self.fit_list.append((self.population[i], int(times_to_add)))
			for ii in range(int(times_to_add)):
				#print "DNA [{}] [{}] added to mating pool".format(self.population[i].to_string(), self.population[i].get_fitness())
				self.mating_pool.append(self.population[i])

		print "Mating pool is {} specimens".format(len(self.mating_pool))




		

	def print_population(self):
		print "Population:"
		for i in range(self.pop_size):
			self.print_dna_and_fitness(self.population[i].to_string(), self.population[i].get_fitness())

	def print_mating_pool(self):
		print "Mating Pool:"
		for i in range(len(self.mating_pool)):
			self.print_dna_and_fitness( self.mating_pool[i].to_string(), self.mating_pool[i].get_fitness())

	def print_dna_and_fitness(self, dna, fitness):
		print "[{}], fitness = [{}]".format(dna, fitness)


	def generate(self):
		for i in range(self.pop_size):
			if( i < self.elite_size):

				self.population[i] = self.elites[i].clone()
			else:
				a = random.randint(0, len(self.mating_pool) - 1)
				b = random.randint(0, len(self.mating_pool) - 1)
				partnerA = self.mating_pool[a]
				partnerB = self.mating_pool[b]

				child = partnerA.crossover(partnerB)
				child.mutate(self.variation)
				self.population[i] = child

		self.generations += 1


	def get_best_fit(self):
		best_fitness = 0
		best_fit = None
		for i in range(self.pop_size):
			if( self.population[i].get_fitness() > best_fitness ):
				best_fitness = self.population[i].get_fitness()
				best_fit = self.population[i]



		return best_fit

	def get_fit_list(self):
		return self.fit_list

	def get_population_list(self):
		return self.population


