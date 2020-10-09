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
estado_inicial = pd.DataFrame(index=(colunas),columns=(colunas))
tabuleiro = pd.DataFrame(index = (colunas),columns = (colunas))
# coordenadas eixo Y
eiy = [y for y in range(N)]
#coordenadas eixo X
arr = [i for i in range(N)]
random.shuffle(arr)
param = arr


'''criando estado inicial'''
for i in range(len(eiy)):
    estado_inicial[eiy[i]][param[i]] = 'Rainha' 

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

'''funcao verifica base de dados txt'''
def verify(ls):  
    #spl = [ls]
    listnumeros = []
    leitura = open('documento.txt','r')
      
    for item in leitura:
        #print(int(item))
        #print(item)
        #spl.append(item.split())
      
        for numero in item:
          # print(int(numero))
            if numero != '\n':
                listnumeros.append(int(numero))
                if 1 == int(numero):
                    pass
                    #print('bom')
    leitura.close()           
    nivel = open('documento.txt','r')
    pr = str(ls)
    pb = pr.split('[')
    pc = pb[1].split(']')
    pd = pc[0].split(',')
    lp =''
    for valor in pd:
        lp += valor
    lp += '\n'    
    arrParam = lp.replace(" ","")    
    for nv in nivel:
        '''se o valor ja existe no arquivo txt retorne True'''
        if nv == arrParam:
            print('ok')
            return True
       
    nivel.close()
                 
'''codigo do professor termina aqui'''

def hill_clim(arr):
    #arr1 = arr
    global list_control
    arr2 = arr

    documento = open('documento.txt','w')
    while True:
        if goal_test(arr2) != False:
            return arr2
        else:
            #list_control[str(indice)] = selects
            for num in arr2:
                documento.write(str(num))
            documento.write('\n') 
            random.shuffle(arr2)
            if verify(arr2) == True:
                random.shuffle(arr2)              
    documento.close()       

    
'''testando uma nova forma de seleção de coordenadas'''
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
                    #verifica combinações sem conflito
                    if vf == True:    
                        sol.append([c1,c2])             
    
    return sol

hh  = hc(param)
eix = hill_clim(arr)
'''
adicionando rainhas em suas posições
'''
for i in range(len(eiy)):
    tabuleiro[eiy[i]][eix[i]] = 'Rainha' 
#eix[i]
ls = [5,2,0,7,4,1,3,6]
result = verify(ls)
        
        
        
'''
solist = hc(param)
contagem = []
peneira = []

for item in solist:
    if item[2] == [False]:
        print('ok')
    elif item[2] != False:
        contagem.append([item[0],item[]])
        
for obj in contagem:
    if obj[0] in solist[0][0]:
        if solist[0][2] == [True]:
            peneira.append(obj)
            
verificar conlfitos e tomar decisão''' 
