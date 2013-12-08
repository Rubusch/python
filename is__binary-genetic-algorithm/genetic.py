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



class Person(object):
    def __init__(self, chromosome=0.1, chromosome=0, prob=0):
        self._chromosome=chromosome
        self._fitness=fitness
        self._prob=prob
    def chromosome(self): return self._chromosome
    def set_chromosome(self,chromosome): self._chromosome=chromosome
    def fitness(self): return self._fitness
    def set_fitness(self,fitness): self._fitness=fitness
    def prob(self): return self._prob
    def set_prob(self,prob): self._prob=prob


class Genetic(object):
    def __init__(self,population_size, chromosome_size, mutation_rate):
        self.population_size=population_size
        self.chromosome_size=chromosome_size
        self.mutation_rate=mutation_rate
        self.persons=[]
        self.new_persons=[]
        self._run=0
        self.optimal=0

    def run(self):
        # 1. initialize random popolation of candidate solutions
        # create random chromosome
        for idx in range(self.population_size):
            persons += [Person()]
            for jdx in range(self.chromosome_size):
                persons[idx].set_chromosome(self.get_chromosome())    

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
            self.persons[idx].set_fitness(self.get_fitness(self.persons[idx].chromosome()))

    def select(self):
        for idx in range(self.population_size):
            self.persons[idx].set_prob(self.get_prob(self.persons,self.persons[idx].fitness()))

        pidx=0
        while pidx < self.population_size:
            self.new_persons=[]
            rand=random.randrange(1,self.population_size-1)/10
            tmp=0
            for idx in range(self.population_size):
                self.new_persons=Person()
                tmp += self.persons[idx].prob
                if rand < tmp:
                    new_person[pidx].set_chromosome(persons[idx].chromosome())
# TODO              
                    source[pidx]=idx   
                    pidx+=1
                    idx=100
                ## // if
            ## // for
        ## // while
        mother, father=self.get_parents(self.new_persons)
        self.new_persons=self.crossover(self.new_persons,mother,father)

    def recombine(self):
        for idx in range(self.population_size):
            for jdx in range(self.chromosome_size):
                rand = random.randrange(0,10000000)/10000000 * 1.0
                if rand < self.mutation_rate:
# TODO              
                    if self.new_persons[idx].chromosome[jdx] == 0:   
                        self.new_persons[idx].chromosome[idx]=1
                    else:
                        self.new_persons[idx].chromosome[idx]=0
                    ## // if
                ## // if
            ## // for
        ## // for

    def is_goto_two(self):
        optimal=self.is_optimal(new_persons)
        for idx in range(self.population_size):
            new_persons[idx].set_fitness(self.get_fitness(new_persons[idx].chromosome))
            print "Generation: "+run+"Best fitness: "+self.get_best_fitness(self.new_persons)    
            self.persons = self.new_persons


            
    def get_chromosome(self): # elements of [1;8[
        return [random.randrange(1,8) for i in range(self.chromosome_size)]

    def get_best_fitness(self, persons):
        return max([persons[i].fitness() for i in range(self.population_size)])/self.chromosome_size

    def get_prob(self, persons, fitness):
        ## get total fitness
        totalfitness=0
        for idx in self.population_size:
            totalfitness+=persons[idx].fitness
        ## fraction of total fitness
        return (1.0* fitness) / totalfitness

    def get_parents(self, persons):
        mother=None
        father=mother
        while mother == father:
            mother = persons[random.randrange(0,self.population_size)]
            father = persons[random.randrange(0,self.population_size)]
        return mother, father

    def crossover(self, persons, mother, father):
        new_maternal_chromosome=[i for i in mother.chromosome]
        new_paternal_chromosome=[i for i in father.chromosome]
        crossover_point=random.randrange(0,self.chromosome_size)
        for idx in range(crossover_point,self.chromosome_size):
            new_maternal_chromosome[idx] = father.chromosome[idx]
            new_paternal_chromosome[idx] = mother.chromosome[idx]
            
#            person   # TODO person new
        pass

    def is_optimal(self):
        
        pass



    
    def print_new_chromosome(self):
        print "Population : Chromosome"
        for idx_pop in self.population_size:
            for idx_chr in self.chromosome_size:
                print "%d\t%d"%(idx_pop, self._new_persons[idx_pop].chromosome[idx_chr])




## MAIN
if __name__ == '__main__':
    population_size = 10
    chromosome_size = 5
    mutation_rate = 0.2

    genetic = Genetic(population_size, chromosome_size, mutation_rate)

    print "optimal solution"
    print "generations: ",genetic.run()
    print "genes: "


    genetic.print_new_chromosome()


    print "READY."
