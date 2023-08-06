class Chromosome:
    '''
    An abstract class that contains methods for a chromosome object
    used by selection algorithms.

    '''
    def __init__(self):
        self.fitness = 0
        self.mutation_probabilty = 0


    def crossover(self,chromosome):
        pass

    def compute_fitness(func):
        pass