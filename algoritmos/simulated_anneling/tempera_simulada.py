# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 12:51:20 2020

@author: Benjamim
"""
import os
import math
import sys
import psutil
import random
from random import choice
import time
import pandas as pd
from collections import Counter
####plot libs######
from pandas.plotting import register_matplotlib_converters
#conversor de objetos pandas para plot
register_matplotlib_converters()

process = psutil.Process(os.getpid())

def geraEstadoInicial(N):
    global lista_global
    lista = list(random.randrange(N) for i in range(N))
    lista_global = lista
    return lista
           
def h(state):
    a, b, c = [Counter() for i in range(3)]
    for row, col in enumerate(state):
        a[col] += 1
        b[row - col] += 1
        c[row + col] += 1
    h = 0  
    for count in [a, b, c]:
        for key in count:
            h += count[key] * (count[key] - 1) / 2
    return -h

def goal_test(state):
    a, b, c = (set() for i in range(3))
    for row, col in enumerate(state):
        if col in a or row - col in b or row + col in c:
            return False
        a.add(col)
        b.add(row - col)
        c.add(row + col)
    return True

#   Retorna todos os estados acessiveis a partir do atual movendo as pecas por coluna
def estadosProximos(estado):
    estProx = []
    # Para cada state[coluna] verfica se as colunas vizinhas estao vazias
    for linha in range(N):
        for coluna in range(N):
            if coluna != estado[linha]:
                melhorEstado = list(estado)
                melhorEstado[linha] = coluna  
                estProx.append(list(melhorEstado))  
    return estProx

# Retorna uma escolha aleatoria dentre os estados proximos
def geraEstado(estado):
    return choice(estadosProximos(estado))

# Variação da temperatura
def vtemp(temperatura=1000, decaimentoPercent=0.001,iteracoes = 99999):
    # a cada iteração reduzir temperatura pelo decaimento
    # teperatura é um parametro de controle 
    return lambda temp: (temperatura * math.exp(-decaimentoPercent * temp)if iteracoes>temp else 0)

def temperaSimulada(estado,vtemp = vtemp()):
    atual = estado 
    objetivoAtual = h(atual) 
    for i in range(sys.maxsize): 
        # a cada iteração reduzir alpha% a temperatura 
        temperatura = vtemp(i)
        print(temperatura)
        global var_temp
        var_temp.append(temperatura)
        if temperatura == 0 or goal_test(atual):
            return atual
        vizinho = geraEstado(atual)
        global var_vizinhos
        var_vizinhos.append(vizinho)
        print(vizinho)
        if not vizinho:
            return atual
        novoObjetivo = h(vizinho)
        variacao = novoObjetivo - objetivoAtual
        # Tomada de decisao com base na variacao de temperatura e probabilidade sendo 0 = 0% e 1 = 1%
        if variacao > 0 or math.exp(variacao / temperatura) > random.uniform(0.0, 1.0):
            atual = vizinho
            objetivoAtual = novoObjetivo

###chamadas
var_temp =[]
var_vizinhos = []
lista_global = []
N = 64
eixos = [i for i in range(N)]
estado_inicial  = pd.DataFrame(index=(eixos),columns=(eixos))
estado_final = pd.DataFrame(index=(eixos),columns=(eixos))
#definindo estado inicial
estado = geraEstadoInicial(N)

#povoando estado inicial no tabuleiro
for b in range(len(lista_global)):
    estado_inicial[b][lista_global[b]] = 'Rainha'
    
#executando algoritimo    
inicio = time.time()
teste = temperaSimulada(estado)
fim = time.time()
#print("{:.5f}s".format(fim - inicio))
tempo_total = fim-inicio 

#povoando dataframe de estado final no tabuleiro
for a in range(len(teste)):
    estado_final[a][teste[a]] = "Rainha"
    
# preparando plot de demontração da função do comportamento do algoritimo    
indices = [i for i in var_temp]    
colunas = [j for j in range(len(var_temp))]
 
data = {'Temperatura': indices,
        'Iterações': colunas}

dframe = pd.DataFrame(data,columns=['Temperatura','Iterações'])

#print(dframe)

dframe.plot(x='Iterações',y='Temperatura',kind='line')

memoria = (process.memory_info()[0])/1000000

print('variação da temp :',var_temp[len(var_temp)-1],'\n','memoria em mbytes:',memoria,'\n','tempo em segundos :',(fim - inicio) )  
##### tratando plot    
    
########## conceitos #########
# Estados do sistema : solucoes viaveis
# Energia : Custo
# Mudança de estado : Estrutura de vizinhança
# Temperatura : parametro de controle
# estado congelado : Solução heuristica(estado em que acabou o processo de tempera do material)
######objtivos######
# atingir soluções vizinhas a partir do estado inicial 
# 
### criando series ####

