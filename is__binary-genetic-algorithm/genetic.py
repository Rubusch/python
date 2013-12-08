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


POPULATION_SIZE = 10
CHROMOSOME_SIZE = 5
MUTATION_RATE = 0.2

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

# TODO person new




class Genetic(object):
    def __init__(self):
        self.presons=[]
        self.new_persons=[]
        self.run=0
        self.optimal=0

        # 1. initialize random popolation of candidate solutions
        # create random chromosome
        for idx in range(POPULATION_SIZE):
            persons += [Person()]
            for jdx in range(CHROMOSOME_SIZE):
                persons[idx].set_chromosome(self.get_chromosome())    

        while self.optimal==0:
            self.run += 1

        # 2. evaluate solutions on problem and assign a fitnes score
        self.evaluate()

        # 3. select some solutions for mating
        self.select()

        # 4. recombine: create new solutions from selected ones by exchanging structure
        self.recombine()



        

    def evaluate(self):
        for idx in range(POPULATION_SIZE):
            self.persons[idx].set_fitness(self.get_fitness(self.persons[idx].chromosome()))

    def select(self):
        for idx in range(POPULATION_SIZE):
            self.persons[idx].set_prob(self.get_prob(self.persons,self.persons[idx].fitness()))

        pidx=0
        while pidx < POPULATION_SIZE:
            self.new_persons=[]
            rand=random.randrange(1,POPULATION_SIZE-1)/10
            tmp=0
#            idx=0
            for idx in range(POPULATION_SIZE):
                self.new_persons=Person()
                tmp += self.persons[idx].prob
                if rand < tmp:
                    new_person[pidx].set_chromosome(persons[idx].chromosome())
                    source[pidx]=idx   
                    pidx+=1
                    idx=100
                ## if
            ## for
        ## while
        parents=self.get_parents(self.new_persons)
        self.new_persons=self.crossover(self.new_persons,parents)




    def recombine(self):
        for idx in range(POPULATION_SIZE):
            for jdx in range(CHROMOSOME_SIZE):
                rand = random.randrange(0,10000000)/10000000 * 1.0
                if rand < MUTATION_RATE:
                    if self.new_persons[idx].chromosome[jdx] == 0:   
                        self.new_persons[idx].chromosome[idx]=1
                    else:
                        self.new_persons[idx].chromosome[idx]=0
                    ## if
                ## if
            ## for
        ## for

        optimal=self.is_optimal(new_persons)
        for idx in range(POPULATION_SIZE):
            new_persons[idx].set_fitness(self.get_fitness(new_persons[idx].chromosome))

            print "Generation: "+run+"Best fitness: "+self.get_best_fitness(self.new_persons)    

            self.persons = self.new_persons


    def goto_two(self):
        # 5. IF good solution not found: GOTO 2
        
        pass


    def get_chromosome(self):
        
        pass



                      


echo "<br>Optimal solution!<br>";
echo "Generation: $run <br>";
echo "Genes: <br>";

echo "<table border=1>
        <tr><th colspan = '4'>Population</th></tr>
        <tr><td>Person </td><td>Chromosome</td></tr>";
    for ($i=0; $i<POPULATION_SIZE; $i++) {
        echo "<tr>";
        echo "<td>$i</td>";
        echo "<td>";
        for ($j=0; $j<CHROMOSOME_SIZE; $j++)
            echo $person_new[$i][chromosome][$j];
        echo "</td>";
        echo "</tr>";
    }
    echo "</table>";

// create a random chomosomes
function get_chromosome(){
    
    for ($i=0; $i<CHROMOSOME_SIZE; $i++) {
        $rand = rand(0,1);
        $chomo[$i] = $rand;  
    }
    
    return $chomo;
}

function get_best_fitness ($p) {
    
    for ($i=0; $i<POPULATION_SIZE; $i++) {
        $fitness[$i] = $p[$i][fitness];
    }
    
    $best_fitness = max($fitness)/CHROMOSOME_SIZE;
    
    return $best_fitness;
    
}

// calculate a fitness value for each person
function get_fitness($chromo) {
    
    $sum=0;
    
    for ($i=0; $i<CHROMOSOME_SIZE; $i++)
        $sum = $sum + $chromo[$i];
     
    return $sum;
   
}

function get_sum_fitness($p) {
    
    $sum=0;
    
    for ($i=0; $i<POPULATION_SIZE; $i++)
        $sum = $sum + $p[$i][fitness];
    
    return $sum;
    
}

// calculate a fitness probability for each person
function get_prob($person, $fitness) {

    $prob = $fitness/get_sum_fitness($person);
    
    return round($prob,4);

}

// select randomly two parents
function get_parents($person_new) {
    
    $parent[A] = rand(0,POPULATION_SIZE-1);
    $parent[B] = rand(0,POPULATION_SIZE-1);
    
    // make sure that the same person will not be selected
    while ($parent[A]==$parent[B]) {
        $parent = get_parents($person_new);
    }
    
    return $parent;
    
}

function crossover($person_new, $parents) {
    
    $tmp = array();
    
    $crossover_point = rand(0,CHROMOSOME_SIZE-1);
    for ($i=$crossover_point; $i<CHROMOSOME_SIZE; $i++) {
        $tmp[$parents[A]][chromosome][$i] = $person_new[$parents[B]][chromosome][$i]; 
        $tmp[$parents[B]][chromosome][$i] = $person_new[$parents[A]][chromosome][$i];
        
        $person_new[$parents[A]][chromosome][$i] = $tmp[$parents[A]][chromosome][$i];
        $person_new[$parents[B]][chromosome][$i] = $tmp[$parents[B]][chromosome][$i];
    }
    
    return $person_new;
    
}

function is_optimal($person_new) {
    
    $con = 0;

    for ($i=0; $i<POPULATION_SIZE; $i++) {
        
        $sum = 0;
        for($j=0;$j<CHROMOSOME_SIZE;$j++)
            $sum += $person_new[$i][chromosome][$j];
        
        if ($sum == CHROMOSOME_SIZE)
           $con = 1;
        
    }
    return $con;
}

                     


print "READY."
