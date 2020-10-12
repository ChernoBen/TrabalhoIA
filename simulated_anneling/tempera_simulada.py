# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 12:51:20 2020

@author: Benjamim
"""
import math
import sys
import psutil
import random
from random import choice
import time
import pandas as pd
from collections import Counter

def initial(N):
    global lista_global
    lista = list(random.randrange(N) for i in range(N))
    lista_global = lista
    return lista
           

def goal_test(state):
    a, b, c = (set() for i in range(3))
    for row, col in enumerate(state):
        if col in a or row - col in b or row + col in c:
            return False
        a.add(col)
        b.add(row - col)
        c.add(row + col)
    return True


def heuristic(state):
    # define a,b,c como contadores
    a, b, c = [Counter() for i in range(3)]
    # contar quantas rainhas tem o os valores (a,b,c)
    # de forma que se obtem por exemplo quantas rainhas tem o valor de a=1
    for row, col in enumerate(state):
        a[col] += 1
        b[row - col] += 1
        c[row + col] += 1
    h = 0  # inicia as colisoes com 0
    # varre as estruturas de contagem (a,b,c) apenas incrementando o valor das colisoes
    # caso para algum valor de (a/b/c)>1 ja que e feito cnt[key]-1
    # divide para retirar contagens dobradas
    for count in [a, b, c]:
        for key in count:
            h += count[key] * (count[key] - 1) / 2
    return -h

# Children ou estados vizinhos: children[]
#   Retorna todos os estados acessiveis a partir do atual movendo as pecas por coluna
def nearStates(state):
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

# Retorna uma escolha aleatoria dentre os estados proximos
def randomNearState(state):
    return choice(nearStates(state))

##############################
# Definindo funçao #
    
def exp_schedule(k=4, alpha=0.001, limit=20000):
    return lambda t: (k * math.exp(-alpha * t) if t < limit else 0)

#problem.initial= numero de rainhas
#problem.heuristic(current) = funcao he(current)
def simulated_annealing(estado, schedule=exp_schedule()):
    current = estado #problem.initial()
    current_h = heuristic(current) #problem.heuristic(current)
    for t in range(sys.maxsize): #alterado
        T = schedule(t)
        if T == 0 or goal_test(current):
            return current
        neighbour = randomNearState(current)
        if not neighbour:
            return current
        # OBS: problem.heuristic(state) retorna -h
        new_h = heuristic(neighbour)
        delta_e = new_h - current_h
        # Tomada de decisao com base na variacao de energia e na probabilidade
        if delta_e > 0 or math.exp(delta_e / T) > random.uniform(0.0, 1.0):
            current = neighbour
            current_h = new_h

###chamadas
lista_global = []
N = 8
eixos = [i for i in range(N)]
estado_inicial  = pd.DataFrame(index=(eixos),columns=(eixos))
estado_final = pd.DataFrame(index=(eixos),columns=(eixos))
#definindo estado inicial
estado = initial(N)
for b in range(len(lista_global)):
    estado_inicial[b][lista_global[b]] = 'Queen'
inicio = time.time()
teste = simulated_annealing(estado)
fim = time.time()
print("{:.5f}ms".format((fim - inicio) * 1000))


#criando dataframe de estados

for a in range(len(teste)):
    estado_final[a][teste[a]] = "Queen"


