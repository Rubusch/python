#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# Assignment05 for Intelligent Systems
#
# author: Lothar Rubusch
# email: l.rubusch@gmx.ch
#
#
# Question 1.
#
# Implement a binary Genetic Algorithm that uses fitness proportional selection,
# 1-point crossover, and bit-flip mutation to solve the problem in which the
# fitness is the number of 1s in the chromosome, i.e. the optimal solution is
# the chromosome where all genes are set to 1.
#
# A. (40 points) Run the algorithm 10 times for each of the four following
# versions of the problem:
# l = 5, 10, 20, 50, where l is the length of the chromosomes. Vary the
# population size and mutation rate to obtain good results (fast solution).
#
# B. (10 points) Plot the best fitness in each generation (averaged over the 10
# runs), for each of the four problems. There should be one graph with four
# curves, the x-axis being the generations, and the y-axis the average (best)
# fitness.


import random # randrange()


import sys # sys.exit()

def die( msg = "" ):
    print "FATAL",
    if 0 < len(str(msg)):
        print ": " + str(msg)
    sys.exit( -1 )


class Person(object):
    def __init__(self, chromosome=[], fitness=0, probability=0):
        self._chromosome=chromosome
        self._fitness=fitness
        self._probability=probability
    def chromosome(self): return self._chromosome
    def set_chromosome(self,chromosome): self._chromosome=chromosome
    def fitness(self): return self._fitness
    def set_fitness(self,fitness): self._fitness=fitness
    def probability(self): return self._probability
    def set_probability(self,probability): self._probability=probability


class Genetic(object):
    def __init__(self,population_size, chromosome_size, mutation_rate):
        self.population_size=population_size
        self.chromosome_size=chromosome_size
        self.mutation_rate=mutation_rate
        self.population=[]
        self.new_population=[]
        self._run=0
        self.optimal=0

    def run(self):
        # 1. initialize random popolation of candidate solutions
        # create random chromosome
        for idx in range(self.population_size):
            self.population += [Person()]
            self.new_population += [Person()]

#            for jdx in range(self.chromosome_size):
            self.population[idx].set_chromosome(self.get_chromosome())

# TODO check init with any NEW set of chromosomes
            self.new_population[idx].set_chromosome(self.get_chromosome())

        while self.optimal==0:
            self._run += 1

            # 2. evaluate solutions on problem and assign a fitnes score
            self.evaluate()

            # 3. select some solutions for mating
            self.select()

            # 4. recombine: create new solutions from selected ones by exchanging structure
            self.recombine()

            # 5. IF good solution not found: GOTO 2
            self.is_goto_two()
            

        ## // while
        return self._run

    def evaluate(self):
        for idx in range(self.population_size):
            self.population[idx].set_fitness(self.get_fitness(self.population[idx].chromosome()))

    def select(self):
        for idx in range(self.population_size):
            self.population[idx].set_probability(self.get_probability(self.population,self.population[idx].fitness()))

        pidx=0
        while pidx < self.population_size:
            self.new_population=[]
            rand=random.randrange(1, self.population_size) / 10
            tmp=0
            for idx in range(self.population_size):
                self.new_population=Person()
                tmp += self.population[idx].probability
                if rand < tmp:
                    new_person[pidx].set_chromosome(population[idx].chromosome())
# TODO is this needed: "from" ?              
#                    source[pidx]=idx   
                    pidx+=1
                    idx=100
                ## // if
            ## // for
        ## // while

        ## select some of genotypes
        idx_parent_a, idx_parent_b = self.get_parents(self.new_population)
        self.new_population=self.crossover(self.new_population, idx_parent_a, idx_parent_b)

    def recombine(self):
        for idx in range(self.population_size):
            for jdx in range(self.chromosome_size):
                rate = random.randrange(0,10000000)/10000000 * 1.0
                if rate < self.mutation_rate:
                    ## do a single mutation
                    
                    self.new_population[idx].chromosome[jdx] = (self.new_population[idx].chromosome[jdx] + 1) % 2
                    
#                    if self.new_population[idx].chromosome[jdx] == 0:   
#                        self.new_population[idx].chromosome[idx]=1
#                    else:
#                        self.new_population[idx].chromosome[idx]=0
#                    ## // if
                ## // if
            ## // for
        ## // for

    def is_goto_two(self):
        optimal=self.is_optimal(new_population)
        for idx in range(self.population_size):
            new_population[idx].set_fitness(self.get_fitness(new_population[idx].chromosome))

# TODO check where new_population is set up, in terms of fitness and probability
        print "generation: "+run+" - best fitness: "+self.get_best_fitness(self.new_population)
        self.population = [Person( chromosome=elem.chromosome, fitness=elem.fitness, probability=elem.probability) for elem in self.new_population]


            
    def get_chromosome(self): # elements of [0;2[
        return [random.randrange(0,2) for i in range(self.chromosome_size)]

    def get_best_fitness(self, population):
        return max([population[i].fitness() for i in range(self.population_size)])/self.chromosome_size

    def get_fitness(self, chromosome):
        return sum(chromosome)

    def get_probability(self, population, fitness):
        ## get total fitness
#        totalfitness=0
#        for idx in self.population_size:
#            totalfitness+=population[idx].fitness
        ## fraction of total fitness
#        return (1.0* fitness) / totalfitness
        return (1.0 * fitness) / sum([i.fitness for i in population])

    def get_parents(self, population):
        idx_parent_a=None
        idx_parent_b=idx_parent_a
        while idx_parent_a == idx_parent_b:
            idx_parent_a = population[random.randrange(0,self.population_size)]
            idx_parent_b = population[random.randrange(0,self.population_size)]
        return idx_parent_a, idx_parent_b

    def crossover(self, population, new_population, idx_parent_a, idx_parent_b):
        chromosome_parent_a=[ch for ch in population[idx_parent_a].chromosome]
        chromosome_parent_b=[ch for ch in population[idx_parent_b].chromosome]
        ## 1 point chrossover
        crossover_point=random.randrange(0,self.chromosome_size)

        for idx in range(crossover_point, self.chromosome_size):
            chromosome_parent_a[idx] = idx_parent_b.chromosome[idx]
            chromosome_parent_b[idx] = idx_parent_a.chromosome[idx]
            
#            person   # TODO person new
# TODO check this...
            
#            new_population[idx_parent_a] = [Person(chromosome=chromosome_parent_a)]
            new_population[idx_parent_a].chromosome=chromosome_parent_a
#            new_population[idx_parent_b] = [Person(chromosome=chromosome_parent_b)]
            new_population[idx_parent_b].chromosome=chromosome_parent_b

        return [i for i in population]

    def is_optimal(self,population):
        totalchromosome=0
        con=0   
        for idx_pop in range(self.population_size):
            for idx_chr in range(self.chromosome_size):
                totalchromosome+=population[idx_pop].chromosome[idx_chr]
            if self.chromosome_size == totalchromosome:
                con = 1    
# TODO check this...
        return con    



    
    def print_new_chromosome(self):
        print "Population : Chromosome"
        for idx_pop in self.population_size:
            for idx_chr in self.chromosome_size:
                print "%d\t%d"%(idx_pop, self._new_population[idx_pop].chromosome[idx_chr])




## MAIN
if __name__ == '__main__':
    population_size = 10
    chromosome_size = 5
    mutation_rate = 0.2

    die("XXX")    

    genetic = Genetic(population_size, chromosome_size, mutation_rate)

    print "optimal solution"
    print "generations: ",genetic.run()
    print "genes: "


    genetic.print_new_chromosome()


    print "READY."
