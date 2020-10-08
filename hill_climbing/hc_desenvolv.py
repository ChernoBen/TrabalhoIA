# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 10:33:11 2020

@author: Benjamim
"""
import pandas as pd
import numpy as np
#from livelossplot import PlotLosses
import random
#from deap import creator, base, tools, algorithms


#N = Número de rainhas
N = 8
#log_N = número de bits para representar cada rainha
log_N = int(np.log2(N))
#criando tabuleiro
colunas = [i for i in range(N)]
tabuleiro = pd.DataFrame(index = (colunas),columns = (colunas))

#Funções extraídas do código original do livro
#https://github.com/aimacode/aima-python
def conflicted(state, row, col):
    """Would placing a queen at (row, col) conflict with anything?"""
    #print(state,row,col) 
    #print(any(conflict(row, col, state[h],h)
               #for h in range(col)))
    return any(conflict(row, col, state[c], c)
               for c in range(col))

def conflict(row1, col1, row2, col2):
    """Would putting two queens in (row1, col1) and (row2, col2) conflict?"""
    #print(row1,col1,row2,col2)
    
    return (row1 == row2 or  # same row
            col1 == col2 or  # same column
            row1 - col1 == row2 - col2 or  # same \ diagonal
            row1 + col1 == row2 + col2)  # same / diagonal


def hc(node):
    
    num_conflicts = 0
    sol = []
    vf = False
    for (r1, c1) in enumerate(node):
        #print('r1 e c1',(r1,c1))
        for (r2, c2) in enumerate(node):
            #print((r1,c1),':',(r2,c2))
            if (r1, c1) != (r2, c2):
                vf = conflict(r1, c1, r2, c2)
                num_conflicts += conflict(r1, c1, r2, c2)
                if num_conflicts > 0 :
                    print(num_conflicts)
                    sol.append([[r1,c1],[r2,c2],[vf]]) 
               
    
    return sol
        
                
def goal_test(state):
    """Check if all columns filled, no conflicts."""
    if state[-1] == -1:
        return False
    return not any(conflicted(state, state[col], col)
                   for col in range(len(state)))

def h(node):
    """Return number of conflicting queens for a given node"""
    num_conflicts = 0
    confli_list =[]
    for (r1, c1) in enumerate(node):
        #print('r1 e c1',(r1,c1))
        for (r2, c2) in enumerate(node):
            #print((r1,c1),':',(r2,c2))
            if (r1, c1) != (r2, c2):
                num_conflicts += conflict(r1, c1, r2, c2)
                confli_list.append([r1, c1, r2, c2])
    #print(confli_list)    
    
    #print("numero conf",num_conflicts)
    return num_conflicts

def nqueen_fitness(node):
    node_int = []
    for i in range(0, len(node), log_N):
        a = map(str, node[i:i+log_N])    
        node_int.append(int(''.join(a), 2))

    return h(node_int),

#goal_test([2,4,6,8,3,1,7,4])
hh = h([5,2,0,7,4,1,3,6])


'''codigo do professor até aqui'''
arr = [i for i in range(N)]
random.shuffle(arr)
param = arr


def hill_clim(arr):
    #arr1 = arr
    arr2 = arr
    contador = 1
    selects = arr[1:len(arr)]
    while True:
        
        if goal_test(arr2) != False:
            #result = [j for j in arr2]
            #for x in range(len(arr1)):
                #print(x,arr2[x])
            return arr2
        
        contador = 1
        for i in range(len(selects)):
            arr2[contador] = selects[i]
            contador +=1
        
        else:
            print(arr2)
            random.shuffle(selects)

'''testando uma nova forma de seleção de coordenadas'''
solist = hc(param)
contagem = []
peneira = []

for item in solist:
    if item[2] == [False]:
        print('ok')
    elif item[2] != False:
        contagem.append([item[0],item[2]])
        
for obj in contagem:
    if obj[0] in solist[0][0]:
        if solist[0][2] == [True]:
            peneira.append(obj)
            
    
    
    
'''
eiy = [y for y in range(N)]
antes = goal_test(param)
eix = hill_clim(param)
depois = goal_test(param)

'''



'''adicionando rainhas em suas posições
for i in range(len(eiy)):
    tabuleiro[eiy[i]][eix[i]] = 'Rainha' 
#eix[i]
'''




[5,2,0,7,4,1,3,6]
