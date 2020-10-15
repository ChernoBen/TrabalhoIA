# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 12:20:49 2020

@author: Benjamim
"""
import os
import random
import numpy
import pandas as pd
import psutil
import time

process = psutil.Process(os.getpid())
#Gera a população de possiveis soluções
#retrorna uma lista de listas de tamaanho N
def geraPoulacao(qtdSolucoes,N):
    #N is the number of queens
    populacao = []
    for i in range (qtdSolucoes):
        populacao.append(random.sample(range(N), N))   
    return populacao
    
#cria descendentes
def geraDescendentes(ascendentes):
    descendentes = []
    for i in range(0,len(ascendentes)-2,3):
        if chanceMudar():
            descendentes.extend(geraDescendente(ascendentes[i:i+3]))
        else:    
            descendentes.extend(ascendentes[i:i+3])
    return descendentes

#altera o gene ou item na lista
def geraMutacoes(solucao):
    novaSolucao = solucao[:]
    i,j=0,0
    while i==j:
        i = random.randint(0,len(solucao)-1)
        j = random.randint(0,len(solucao)-1)
    temp1 = novaSolucao[j]
    temp2 = novaSolucao[i]
    novaSolucao[i] = temp1
    novaSolucao[j] = temp2
    return novaSolucao 
   
#seleção de individuos,avaliza os melhores individuos para nova geração
def obterFitness(solucao):
    pontuacao = (len(solucao)-1)*len(solucao)
    for i in range(0,len(solucao)):
        for j in range(0,len(solucao)):
            if i!=j:
                if i-solucao[i] == j-solucao[j] or i+solucao[i] == j+solucao[j]:
                    pontuacao-=1       
    return pontuacao/2            
  
#cruzamento
#uma parte do primeiro individuo + o primeiro gerando um novo cromossomo  
def geraCruzamento(solucao1,solucao2):
    n = int(len(solucao1)/2)
    novaSolucao1 = solucao1[:n] + solucao2[n:]
    novaSolucao2 = solucao1[n:] + solucao2[:n]
    return (novaSolucao1,novaSolucao2)

def chanceMudar():
    taxaDeCruzamento = 1
    n = random.random()
    if taxaDeCruzamento > n:
    	return n
    
#descendentes
def geraDescendente(ascendentes): #c1 and c2 are chromosomes
    descendente = ascendentes
    fitness = [obterFitness(each_sol) for each_sol in descendente]
    descendente.pop(fitness.index(min(fitness)))
    novoDescendente = geraMutacoes(descendente[random.randint(0, 1)])
    descendente.append(novoDescendente)
    return(descendente) 

#Variable Definition
#crossover_rate = 1
inicio = time.time()
qtdSolucoes = 45
N = 128
geracoes = 999
#Variable Definition
solucoes = geraPoulacao(qtdSolucoes,N)
fitness = [obterFitness(item) for item in solucoes]
df = []
criterioParada = False

j = 0
while j < geracoes:
    for i in range(len(fitness)):
        if fitness[i] == N*(N-1)/2:
            print(solucoes[i])
            df = solucoes[0]
            criterioParada = True
            break
        else:
            j+=1
        if criterioParada:
            break
    gr = j    
    probability_matrix = [x/sum(fitness) for x in fitness]
    ns = numpy.random.choice([i for i in range(qtdSolucoes)],size = qtdSolucoes,p = probability_matrix)
    ascendentes = [solucoes[i] for i in ns]
    solucoes = ascendentes
    solucoes = geraDescendentes(ascendentes)
    sol_fitness = [obterFitness(item) for item in solucoes]
    
### criando df para teste de solucao #####

if df:
    eixos = [i for i in range(len(df))]
    estado_final = pd.DataFrame(index=(eixos),columns=(eixos))
    for j in range(len(eixos)):
        estado_final[j][df[j]] = 'Rainha'
    print(estado_final)    
 
fim = time.time()    
memoria = (process.memory_info()[0])/1000000 
print('grerações:',gr,'\n','memoria em mbytes:',memoria,'\n','tempo em segundos :',(fim - inicio) )     
