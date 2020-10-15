"""
Created on Thu Oct 15 19:26:20 2020

@author: Benjamim
"""
import numpy as np
from livelossplot import PlotLosses
import random
from deap import creator, base, tools, algorithms
import pandas as pd

#N = Número de rainhas
N = 8
#log_N = número de bits para representar cada rainha
log_N = int(np.log2(N))


#Funções extraídas do código original do livro
#https://github.com/aimacode/aima-python
def conflicted(state, row, col):
    """Would placing a queen at (row, col) conflict with anything?"""
    return any(conflict(row, col, state[c], c)
               for c in range(col))

def conflict(row1, col1, row2, col2):
    """Would putting two queens in (row1, col1) and (row2, col2) conflict?"""
    return (row1 == row2 or  # same row
            col1 == col2 or  # same column
            row1 - col1 == row2 - col2 or  # same \ diagonal
            row1 + col1 == row2 + col2)  # same / diagonal

def goal_test(state):
    """Check if all columns filled, no conflicts."""
    if state[-1] == -1:
        return False
    return not any(conflicted(state, state[col], col)
                   for col in range(len(state)))

def h(node):
    """Return number of conflicting queens for a given node"""
    num_conflicts = 0
    for (r1, c1) in enumerate(node):
        for (r2, c2) in enumerate(node):
            if (r1, c1) != (r2, c2):
                num_conflicts += conflict(r1, c1, r2, c2)
    return num_conflicts

def nqueen_fitness(node):
    node_int = []
    for i in range(0, len(node), log_N):
        a = map(str, node[i:i+log_N])    
        node_int.append(int(''.join(a), 2))

    return h(node_int),
#funçao que converte lista de binarios em  decimais com razão igual a log_N rainhas
def binToDec(top,lg):
    j = top
    cont = 0
    ras = lg
    res =[]
    c = []
    ini = 0

    while True:
        if cont >=len(j)//lg:
            break
        c.append("".join(map(str,j[ini:ras]))) 
        ini = ras
        ras += lg
        cont += 1

    for item in c:
        res.append(int(item,2))
        
    return res

#Cria ferramenta de geração de indivíduos
creator.create("Fitness", base.Fitness, weights=(-1.0, )) #Peso -1 por ser um problema de minimização
#Cada indíviduo é composto por um cromossomo que é uma lista de valores
creator.create("Individual", list, fitness=creator.Fitness)

#Toolbox é onde definiremos os operadores para a execução
toolbox = base.Toolbox()

#Função para criação do cromossomo
#x = 0|1
toolbox.register("attr_bool", random.randint, 0, 1) #np.random.randint(0,1)
#Função para Definir a criação do indivíduo. Será feita a repetição da função attr_bool por n vezes
#cromossomo = [x, x, x, x, ..., x]     len(cromossomo) = n
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=N*log_N)
#Função para criar população. Repetição de indivíduos para formar uma lista
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

#função de avaliação
toolbox.register("evaluate", nqueen_fitness)
#função de cruzamento
toolbox.register("mate", tools.cxOnePoint)
#função de mutação
#indpb probabilidade de mutação em bit
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
#função de seleção
toolbox.register("select", tools.selTournament, tournsize=3)

#configuração do gráfico diâmico
groups = {'h': ['top', 'average','worst']}
plotlosses = PlotLosses(groups=groups)

#Inicia população con n indivíduos
population = toolbox.population(n=100)

#Número máximo de gerações
NGEN=1000

#Avalia todos os indivíduos
fits = toolbox.map(toolbox.evaluate, population)
for fit, ind in zip(fits, population):
    ind.fitness.values = fit

for gen in range(NGEN):
    #Faz seleção
    population = toolbox.select(population, k=len(population))
    #Faz o cruzamento e mutação
    #cxpb = probabilidade de cruzamento
    #mutpb = probabilidade de mutação
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)
    
    #Reavalia
    avg_h = 0
    fits = toolbox.map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
        avg_h += fit[0]
        ind.fitness.values = fit
        
    #nova população
    population[:] = offspring
        
    #pega melhor e pior indivíduos para montar o gráfico
    top = tools.selBest(population, k=1)
    worst = tools.selWorst(population, k=1)
    
    avg_h = avg_h/len(population)
    top_h = nqueen_fitness(top[0])[0]
    worst_h = nqueen_fitness(worst[0])[0]
    plotlosses.update({'top': top_h,
                       'average': avg_h,
                       'worst': worst_h})
    plotlosses.send()
    
    #Avalia critério de parada
    if(nqueen_fitness(top[0])[0] == 0): 
        print(top[0])
        resultado = binToDec(top[0],log_N)
        #dataframe
        eixos = [i for i in range(N)]
        estado_inicial  = pd.DataFrame(index=(eixos),columns=(eixos))
        estadoInicial = list(random.randrange(N) for i in range(N))
        for i in range(len(estadoInicial)):
            estado_inicial[eixos[i]][resultado[i]] = 'rainha'
            
        break


 