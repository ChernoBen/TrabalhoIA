# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
from livelossplot import PlotLosses
from livelossplot.outputs import MatplotlibPlot,ExtremaPrinter
import random
from deap import creator,base,tools,algorithms
import matplotlib.pyplot as plt

'''numero de rainhas'''
N = 8
log_N = int(np.log2(N))

def conflicted(state,row,col):
    return any(conflicted(row,col,state[c],c)
               for c in range(col))

def conflict(row1,col1,row2,col2):
    return(row1 == row2 or 
           col1 == col2 or
           row1 - col1 == row2 - col2 or
           row1 + col1 == row2 + col2)

def goal_test(state):
    if state[-1] == -1:
        return False
    return not any(conflicted(state,state[col],col)
                   for col in range(len(state)))


def h(node):
    num_conflicts = 0
    for (r1,c1) in enumerate(node):
        for (r2,c2) in enumerate(node):
            if (r1,c1) != (r2,c2):
                num_conflicts += conflict(r1,c1,r2,c2)
    return num_conflicts


def nqueen_fitness(node):
    node_int = []
    for i in range(0,len(node),log_N):
        a = map(str,node[i:i+log_N])
        node_int.append(int(''.join(a),2))
    return h(node_int)

goal_test([2,4,6,8,3,1,7,4])


h([2,2,6,7,3,1,7,4])


creator.create("Fitness",base.Fitness,weights=(-1.0, ))

creator.create("Individual",list,fitness=creator.Fitness)

toolbox = base.Toolbox()

toolbox.register("attr_bool",random.randint,0,1)

toolbox.register("individual",tools.initRepeat,creator.Individual,toolbox.attr_bool,
                 n=N*log_N)

toolbox.register("population",tools.initRepeat,list,toolbox.individual)


toolbox.register("evaluate",nqueen_fitness)

toolbox.register("mate",tools.cxOnePoint)

toolbox.register("mutate",tools.mutFLipBit,indpb=0.05)

toolbox.register("select",tools.selRoulette)

population = toolbox.population(n=1)

population[0]

nqueen_fitness(population[0])[0]

groups={'h':['top','average','worst']}

plotlosses = PlotLosses(outputs=[MatplotlibPlot(cell_size=(4,2)),ExtremaPrinter()],
                        groups=groups)

population = toolbox.population(n=100)

NGEN = 50

fits = toolbox.map(toolbox.evaluate,population)

for fit, ind in zip(fits,population):
    ind.fitness.values = fit
    
for gen in range(NGEN):
    population = toolbox.select(population,len(population))
    offspring = algorithms.varAnd(population,toolbox,cspb=0.5,mutpb=0.1)


    avg_h = 0
    
    fits = toolbox.map(toolbox.evaluate,offspring)
    
    for fit, ind in zip(fits,offspring):
        avg_h +=fit[0]
        ind.fitness.values = fit
    
    population[:] = offspring
    
    top = tools.selBest(population,k=1)
    worst = tools.selWorst(population,k=1)
    
    avg_h = avg_h/len(population)
    top_h = nqueen_fitness(top[0])[0]
    worst_h = nqueen_fitness(worst[0])[0]
    plotlosses.update({'top':top_h,
                       'average':avg_h,
                       'worst':worst_h})
    
    plotlosses.send()
    
    
    if (nqueen_fitness(top[0])[0]==0): break





    
    
    
    
    
    
    
    

















    
    
    
    
    