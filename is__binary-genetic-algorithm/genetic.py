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
    def __init__(self, chromosome=[], fitness=0, probability=0.0):
        self._chromosome=chromosome
        self._fitness=fitness
        self._probability=probability
    def chromosome(self): return self._chromosome
    def set_chromosome(self,chromosome): self._chromosome=chromosome
    def fitness(self): return self._fitness
    def set_fitness(self,fitness): self._fitness=fitness
    def probability(self): return self._probability
    def set_probability(self, probability): self._probability=probability
    def set_chromatide(self, idx, chromatide): self._chromosome[idx] = chromatide


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
        self.population = [Person(chromosome=self.generate_chromosome()) for p in range(self.population_size)]

#        for idx in range(self.population_size):
#            self.population += [Person()]
#            self.new_population += [Person()]
#            self.population[idx].set_chromosome(self.generate_chromosome())

# TODO rm
#            self.new_population[idx].set_chromosome(self.generate_chromosome())   

        while self.optimal==0:
            self._run += 1

            # 2. evaluate solutions on problem and assign a fitnes score
            self.evaluate()

            self.DB_population()     
            print ""                 

            # 3. select some solutions for mating
            self.selection()

            # 4. recombine: create new solutions from selected ones by exchanging structure
            self.recombination()

            self.DB_population()     
            die("FAHRKARTENKONTROLLE")                                         


            # 5. IF good solution not found: GOTO 2
            self.optimal = self.is_done()


            
#            print "XXX total fitness %d"%sum([i.fitness() for i in self.population])    
            self.DB_population()    
#            print ""  
            if self._run == 150: die("150. generation XXX")    
            
        print "EXIT"

        ## // while
        return self._run

    def evaluate(self):
        for idx in range(self.population_size):
            self.population[idx].set_fitness(self.get_fitness(self.population[idx].chromosome()))

    def selection(self):
# TODO check proportional selection

        ## calculate a genotypes probability of being selected in proportion to its fitness
        for idx in range(self.population_size):
            self.population[idx].set_probability(self.compute_probability(self.population, self.population[idx].fitness()))

        ## prepare new_population
        idx=0
        while idx < self.population_size:
            # for each position in new_population choose a "likely" individual
            probability = 0.0
            for jdx in range(self.population_size):
                ## get random criteria
                rnd_probability = (1.0*random.randrange(1, self.population_size)) / 10
                ## go through all population items and see by probability if one gots selected,
                ## only increment the counter if we have an item for new_population
                ## if not, go through all again
                probability = self.population[jdx].probability()
                if rnd_probability < probability:
                    ## we found an item
                    self.new_population += [Person(chromosome=self.population[jdx].chromosome())]
                    idx+=1
                    break


                                        
##        idx_parent_a, idx_parent_b

            

        # new_pop_idx=0
        # while new_pop_idx < self.population_size:
        #     rnd_probability = (1.0*random.randrange(1, self.population_size)) / 10
        #     probability = 0.0
        #     for pop_idx in range(self.population_size):
        #         self.new_population[pop_idx] = Person()
        #         probability += self.population[pop_idx].probability()
        #         if rnd_probability < probability:
        #             self.new_population[new_pop_idx].set_chromosome(self.population[pop_idx].chromosome()) 
        #             new_pop_idx += 1
        #             break



                    


            
#         new_pop_idx=0
# #        prob=0.0  
#         while new_pop_idx < self.population_size:
# #            self.new_population=[]
#             random_probability=(1.0*random.randrange(1, self.population_size)) / 10

#             prob=0.0  
#             for pop_idx in range(self.population_size):
# #                print( "new_pop_idx '%d', pop_idx '%d' - prob '%f'"%(new_pop_idx,pop_idx,prob))     

# #                self.new_population[new_pop_idx] = Person()   
#                 self.new_population[pop_idx] = Person()   
#                 prob += self.population[pop_idx].probability()

# #                print("prob '%d'"%prob)     
# #                print "random_probability: %f, prob: %f"%(random_probability,prob)    
#                 if random_probability < prob:
# #                    chromo=self.population[pop_idx].chromosome()  
# #                    self.new_population[new_pop_idx].set_chromosome(chromo)  
#                     self.new_population[new_pop_idx].set_chromosome(self.population[pop_idx].chromosome())
#                     new_pop_idx+=1
# #                    print("break - len(new_population) = '%d'"%len(self.new_population))              
#                     break

# # TODO how should this algorithm work??     
# # FIXME     
# #                    pop_idx=100
#                 ## // if
#             ## // for
#         ## // while
            




        ## then select some number of genotypes for mating according to probabilities
# TODO check, get_parents selects randomly, ando not "according to probabilities"     
#        idx_parent_a, idx_parent_b = self.get_parents()  
                
#        self.new_population=self.crossover(self.population, self.new_population, idx_parent_a, idx_parent_b)
                

    def recombination(self):
        ## mating
        self.new_population = self.crossover(self.new_population)

            
        for idx in range(self.population_size):
            for jdx in range(self.chromosome_size):
                rate = random.randrange(0,10000000)/10000000 * 1.0
                if rate < self.mutation_rate:
                    ## do a single mutation
                    self.new_population[idx].set_chromatide(jdx, (self.new_population[idx].chromosome()[jdx] + 1) % 2)
                ## // if
            ## // for
        ## // for

    def is_done(self):
        print "generation: %d - best fitness: %d"%(self._run, self.get_best_fitness(self.new_population))   
        if 0 != self.is_optimal(self.new_population):
            return 1

        for idx in range(self.population_size):
            self.new_population[idx].set_fitness(self.get_fitness(self.new_population[idx].chromosome()))

# TODO check where new_population is set up, in terms of fitness and probability
        self.population = [Person( chromosome=elem.chromosome(), fitness=elem.fitness(), probability=elem.probability()) for elem in self.new_population]
        return 0

    def generate_chromosome(self): # elements of [0;2[
        return [random.randrange(0,2) for i in range(self.chromosome_size)]

    def get_best_fitness(self, population):
        return max([population[i].fitness() for i in range(self.population_size)])/self.chromosome_size

    def get_fitness(self, chromosome):
        return sum(chromosome)

    def compute_probability(self, population, fitness):
        return (1.0 * fitness) / sum([i.fitness() for i in population])

    def get_parents(self):
# TODO this picks just any kind of parents - do we need to keep certain criteria for selection?
        idx_parent_a=None
        idx_parent_b=idx_parent_a
        while idx_parent_a == idx_parent_b:
            idx_parent_a = random.randrange(0, self.population_size)
            idx_parent_b = random.randrange(0, self.population_size)
        return idx_parent_a, idx_parent_b

    def crossover(self, population):
        for idx_person in range(1,self.population_size,2):
            chromosome_a=[]; chromosome_b=[]
            ## 1 point chrossover
            crossover_point=random.randrange(0,self.chromosome_size)
            print "XXX crossover_point %d",crossover_point  
            print population[idx_person-1].chromosome()  
            print population[idx_person].chromosome()  

            for idx_chromosome in range(self.chromosome_size):
                print "%d ",(idx_person-1 if idx_chromosome < crossover_point else idx_person)   
                chromosome_a += [population[idx_person-1 if idx_chromosome < crossover_point else idx_person].chromosome()[idx_chromosome]]
                print "%d ",(idx_person if idx_chromosome < crossover_point else idx_person-1)   
                chromosome_b += [population[idx_person if idx_chromosome < crossover_point else idx_person-1].chromosome()[idx_chromosome]]

            print population[idx_person-1].chromosome()  
            print population[idx_person].chromosome()  
            print ""    
            ## init by generated chromosome
            population[idx_person-1].set_chromosome(chromosome_a)
            population[idx_person].set_chromosome(chromosome_b)

            die("XXX")   
        return population


        # chromosome_parent_a=[ch for ch in population[idx_parent_a].chromosome()]
        # chromosome_parent_b=[ch for ch in population[idx_parent_b].chromosome()]
        # ## 1 point chrossover
        # crossover_point=random.randrange(0,self.chromosome_size)
        # for idx in range(crossover_point, self.chromosome_size):
        #     chromosome_parent_a[idx] = population[idx_parent_b].chromosome()[idx]
        #     chromosome_parent_b[idx] = population[idx_parent_a].chromosome()[idx]
            
#            person   # TODO person new
# TODO check this...
            
#            new_population[idx_parent_a].chromosome=chromosome_parent_a
#            new_population[idx_parent_b].chromosome=chromosome_parent_b
#        return [i for i in population]

    def is_optimal(self, population):
        for pop in population:
#            print "chromsome_size %d"%self.chromosome_size    
#            print "sum %d"%sum(pop.chromosome())    
#            print ""    
            if self.chromosome_size == sum(pop.chromosome()):
                return 1
        return 0

        
#         totalchromosome=0
#         con=0   
#         for idx_pop in range(self.population_size):
#             for idx_chr in range(self.chromosome_size):
#                 totalchromosome += population[idx_pop].chromosome()[idx_chr]
#             print "totalchromosome_size"
#             if self.chromosome_size == totalchromosome:
#                 con = 1    
# # TODO check this...
#         return con    


    ## debug, print the chromosomes of all population
    def DB_population(self):
        print "self.population"
        for idx in range(self.population_size):
            print "%d. individuum, fitness: '%d', probability: '%f', chromosome: "%(idx, self.population[idx].fitness(), self.population[idx].probability()),
            print '%s'%' '.join(map(str,self.population[idx].chromosome()))
        print "self.new_population"
        for idx in range(len(self.new_population)):
            print "%d. individuum, fitness: '%d', probability: '%f', chromosome: "%(idx, self.new_population[idx].fitness(), self.new_population[idx].probability()),
            print '%s'%' '.join(map(str,self.new_population[idx].chromosome()))
            


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

    genetic = Genetic(population_size, chromosome_size, mutation_rate)
    genetic.run()

    die("STOP")    

    print "optimal solution"
    print "generations: ",genetic.run()
    print "genes: "


    genetic.print_new_chromosome()


#    population_size = 10
#    chromosome_size = 10
#    mutation_rate = 0.02
# TODO


#    population_size = 10
#    chromosome_size = 20
#    mutation_rate = 0.02
# TODO


#    population_size = 10
#    chromosome_size = 50
#    mutation_rate = 0.02
# TODO


    print "READY."
