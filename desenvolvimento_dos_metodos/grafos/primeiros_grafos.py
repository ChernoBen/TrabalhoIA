# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 19:41:08 2020

@author: Benjamim
"""
import random
n = 8
'''gerando representação do problema'''
matrix = []

for i in range(n):
    for j in range(n):
       print(i,j)
       matrix.append((i,j))
       
'''vetor de estado - sorteio de posições''' 
vetor_estado = []
for x in range(8):
    vetor_estado.append(random.choice(matrix))
    
    
'''funcao objetivo'''
def f_objetivo(vetor_estado):
    '''
        verificar se  as coordenadar compartilhando diagonais,
        verticais ou retas
        decobrir o angulo entre o ponto e o proximo
    '''
    pass