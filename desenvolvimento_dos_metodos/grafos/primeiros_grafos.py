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
var_estado = []
var_estado = random.choice(df[:][0])

lista_estados = [var_estado]
ps = df[:][1]
    
'''funcao objetivo'''
def f_objetivo(var_estado,df,lista_estados,n):
    proximo_estado = df[:][1]
    
    
    
    pass