import sys,pygame
from Population import Population
from Obstacle import Obstacle
import math
pygame.init()

size = width, height = 500,500

screen = pygame.display.set_mode(size)
surface = pygame.Surface(size)


population_size = 200
mutation_probability = 0.05
goal_position = (250,250)
start_position = (0,250)
flowfield_dim = 100
elite_size = 5

obstacles = []

obstacles.append(Obstacle(50, 200, 20, 100))
obstacles.append( Obstacle( 150, 100, 20, 140))
obstacles.append( Obstacle(150, 260, 20, 150))

population = Population(population_size, mutation_probability, elite_size, goal_position, start_position, flowfield_dim, obstacles)



while(1):
	population_list = population.get_population_list()

	for x in range(500):
		screen.fill((255,255,255))
		pygame.draw.circle(screen, (0,255,0), goal_position, 5, 0)
		pygame.draw.circle(screen, (255,0,0), goal_position, 20, 1)
		pygame.draw.circle(screen, (255,0,0), goal_position, 40, 1)
		pygame.draw.circle(screen, (255,0,0), goal_position, 60, 1)
		pygame.draw.circle(screen, (255,0,0), goal_position, 80, 1)
		pygame.draw.circle(screen, (255,0,0), goal_position, 100, 1)
		pygame.draw.circle(screen, (255,0,0), goal_position, 120, 1)
		pygame.draw.circle(screen, (255,0,0), goal_position, 140, 1)
		pygame.draw.circle(screen, (255,0,0), goal_position, 160, 1)
		pygame.draw.circle(screen, (255,0,0), goal_position, 180, 1)
		pygame.draw.circle(screen, (255,0,0), goal_position, 200, 1)


		for o in range(len(obstacles)):
			pygame.draw.rect(screen, (255,0,0), (obstacles[o].x, obstacles[o].y, obstacles[o].width, obstacles[o].height),0)

		for r in range(len(population_list)):
			population_list[r]._step()
			pygame.draw.circle(screen, (0,0,0), population_list[r]._pos(), 2, 0)
			

		pygame.display.flip()

	population.calcFitness()
	best_fit = population.get_best_fit()
	print ""
	print "Generation {}".format(population.generations)
	print "Best fit: Position [{}] TTC: [{}] Hit obstacle: [{}] Done: [{}] Fitness: [{}]".format(best_fit._pos(), best_fit.time_to_completion, best_fit.hit_obstacle, best_fit.finished, best_fit.get_fitness())

	sum_x = 0
	sum_y = 0
	sum_ttc = 0
	sum_hit = 0
	sum_done = 0
	sum_fitness = 0
	for i in range(population_size):
		sum_x += population_list[i]._pos()[0]
		sum_y += population_list[i]._pos()[1]
		sum_ttc += population_list[i].time_to_completion
		sum_hit += population_list[i].hit_obstacle
		sum_done += population_list[i].finished
		sum_fitness = population_list[i].fitness

	avg_x = float(sum_x) / population_size
	avg_y = float(sum_y) / population_size
	avg_ttc = float(sum_ttc) / population_size
	avg_hit = float(sum_hit) / population_size
	avg_done = float(sum_done) / population_size
	avg_fitness = float(sum_fitness) / population_size

	print "Best fit: Position [{}] TTC: [{}] Hit obstacle: [{}] Done: [{}] Fitness: [{}]".format((avg_x, avg_y), avg_ttc, avg_hit, avg_done, avg_fitness)

	population.natural_selection()

	fit_list = population.get_fit_list()
	screen.fill((255,255,255))



	for f_X in range(flowfield_dim):
		for f_Y in range(flowfield_dim):
			pygame.draw.line(screen, (0,0,0), (f_X*5, f_Y*5), (f_X*5 + int(best_fit.dna[f_X][f_Y][0]*5), f_Y*5 + int(best_fit.dna[f_X][f_Y][1]*5)))

	best_fit_clone = best_fit.clone()

	for x in range(500):
		pygame.draw.circle(screen, (0,255,0), goal_position, 5, 0)
		pygame.draw.circle(screen, (255,0,0), goal_position, 20, 1)
		pygame.draw.circle(screen, (255,0,0), goal_position, 40, 1)
		pygame.draw.circle(screen, (255,0,0), goal_position, 60, 1)
		pygame.draw.circle(screen, (255,0,0), goal_position, 80, 1)
		pygame.draw.circle(screen, (255,0,0), goal_position, 100, 1)
		pygame.draw.circle(screen, (255,0,0), goal_position, 120, 1)
		pygame.draw.circle(screen, (255,0,0), goal_position, 140, 1)
		pygame.draw.circle(screen, (255,0,0), goal_position, 160, 1)
		pygame.draw.circle(screen, (255,0,0), goal_position, 180, 1)
		pygame.draw.circle(screen, (255,0,0), goal_position, 200, 1)


		for o in range(len(obstacles)):
			pygame.draw.rect(screen, (255,0,0), (obstacles[o].x, obstacles[o].y, obstacles[o].width, obstacles[o].height),0)

		best_fit_clone._step()
		pygame.draw.circle(screen, (0,0,0), best_fit_clone._pos(), 2, 0)
			

		pygame.display.flip()



	for fit in fit_list:
		norm_fit = float(fit[1]) / 100
		color = ( 255 - (norm_fit*255), 0 + norm_fit*255, 0)
#		pygame.draw.circle(screen, color, fit[0]._pos(), 2, 0)

	pygame.display.flip()


	population.generate()









def fitness_fn(x,y, target_x, target_y):
	distance = math.sqrt(math.pow(target_x - x, 2) + math.pow(target_y - y, 2))
	finished = False
	if( distance == 0):
		distance = 1
		finished = True
			
	fitness = math.sqrt( x/(distance))

	return fitness

pos_fit = []

for x in range(0,500, 5):
	for y in range(0, 245, 5):
		pos_fit.append( (x, y, fitness_fn(x,y,250, 250)))

max_fitness = 0
for pf in pos_fit:
	if( pf[2] > max_fitness):
		max_fitness = pf[2]

print "Max fitness: {}".format(max_fitness)
for i in range(len(pos_fit)):
	norm_fitness = pos_fit[i][2] / max_fitness
	#print "Normal fitness {}".format(norm_fitness)
	pos_fit[i] = (pos_fit[i][0], pos_fit[i][1], norm_fitness)

while(1):
	screen.fill((255,255,255))
	for pf in pos_fit:
		color = ( int(255 - (pf[2]*255)), int(0 + pf[2]*255), 0)
		pygame.draw.rect(screen, color, (pf[0], pf[1], 5, 5), 0)
	pygame.display.flip()

