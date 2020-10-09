# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 10:07:15 2020

@author: Benjamim
"""

import pandas as pd
import numpy as np
#from livelossplot import PlotLosses
import random
N = 8

from random import choice
from collections import Counter
from random import randrange

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

#print(goal_test(arr))


def nearStates(state,N):
    
    near_states = []
    # Para cada state[coluna] verfica se as colunas vizinhas estao vazias
    for row in range(N):
        
        for col in range(N):
            # Se for diferente:
            #   entao a col atual da iteracao esta disponivel para movimentar-se
            #   visto que o state[] guarda o valor das colunas em que estao as rainhas
            if col != state[row]:
                aux = list(state)
                aux[row] = col  # Troca a coluna para a vazia
                near_states.append(list(aux))  # E inclui na lista de nearStates
    return near_states



dftest = pd.DataFrame(index = (colunas),columns = (colunas))
testando = nearStates([0,1,2,3,4,5,6,7], N)
ltest = testando[0]


for p in range(len(eiy)):
    dftest[eiy[p]][ltest[p]] = 'Rainha'


          
