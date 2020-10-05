# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 19:41:08 2020

@author: Benjamim
"""
import pandas as pd
import numpy as np
import random


n = 8
'''gerando representação do problema'''
lista = []
colunas = [i for i in range(n)]
df = pd.DataFrame( index=(colunas), columns=(colunas))
i,j=0,0
for i in range(n):
    for j in range(n):
       print(i,j)
       lista.append((i,j))
       df[i][j]= (i,j)
       


       
'''vetor de estado - sorteio de posições''' 
vetor_estado = []
for x in range(8):
    vetor_estado.append(random.choice(lista))
    
    
'''funcao objetivo'''
def f_objetivo(vetor_estado):
    '''
        verificar se  as coordenadar compartilhando diagonais,
        verticais ou retas
        decobrir o angulo entre o ponto e o proximo
    '''
    pass