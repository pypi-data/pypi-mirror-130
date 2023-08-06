import random as random
import hashlib
import logging

class RouletteWheel:
	def __init__(self,population):
		self.population = population
		self.sum = self.create_wheel()

	def create_wheel(self):
		return self.sum_fitness(self.population)

	def sum_fitness(self):
		sum = 0
		for x in range(0,len(self.population)):
			sum = sum + self.population[x].fitness
		return sum


	def get_parents(self,population):
		logging.info("Selecting parent one :\n")
		parent_one = self.select_individual(population)
		logging.info("\nSelecting parent two: \n")
		parent_two = self.select_mate(population,parent_one)
		return parent_one,parent_two


	def select_individual(self,population):
		R = 0
		R = R + random.uniform(0,self.sum)
		logging.info("Threshold : " + str(R))
		weight = 0
		for x in range(0,len(population)):
			weight = weight + population[x].fitness
			if(weight >= R):
				return population[x]
		return -1

	def select_mate(self,population,partner):
		R = 0
		R = R + random.uniform(0,self.sum)
		weight = 0
		for x in range(0,len(population)):
			weight = weight + population[x].fitness
			if(weight >= R):
				if(population[x] == partner):
					return self.select_mate(population,partner)
				else:
					return population[x]
		return -1