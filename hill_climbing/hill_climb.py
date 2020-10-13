# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 12:51:20 2020

@author: Benjamim
"""

import os
import psutil
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
process = psutil.Process(os.getpid())
heuristica = [] 

def print_board(state_board): #print_board
    for i in range(len(state_board)):
        for j in range(len(state_board)):
            if state_board[j] == i:
                estado_final[i][j] = 'Rainha'
                 
def conflicted(state, row, col):
    """Would placing a queen at (row, col) conflict with anything?"""
    return any(conflict(row, col, state[c], c)for c in range(col))
    
  

def conflict(row1, col1, row2, col2):
    """Would putting two queens in (row1, col1) and (row2, col2) conflict?"""
    '''retorna True se existir conflito entre as duas colunas'''
    return ( (row1 == row2 or  # same row
              col1 == col2 or  # same column
              row1 - col1 == row2 - col2 or  # same \ diagonal
              row1 + col1 == row2 + col2 ) )  # same / diagonal

def goal_test(state):
    """Check if all columns filled, no conflicts."""
    if state[-1] == -1:
        return False
    return not any(conflicted(state, state[col], col)
                  for col in range(len(state)))

def buscaEstadosProximos(N,estado):
    estadosProximos = []
    # Para cada state[coluna] verfica se as colunas vizinhas estao vazias
    for row in range(N):
        for col in range(N):
            if col != estado[row]:
                aux = list(estado)
                aux[row] = col  # Troca a coluna para a vazia
                estadosProximos.append(list(aux))  # E inclui na lista de nearStates
    #print('near_states:',near_states)
    return estadosProximos


def h(estado):
    num_conflicts = 0
    for (r1, c1) in enumerate(estado):
        for (r2, c2) in enumerate(estado):
            if (r1, c1) != (r2, c2):
                num_conflicts += conflict(r1, c1, r2, c2)
    #retorna a quantidade de conflitos negativo dividido p/2 
              
    return -num_conflicts/2


def procuraVizinhos(vizinhos, estado):
    #lista de melhores vizinhos
    melhorVizinho = []
    #
    vizinho = max(vizinhos, key=lambda estado: h(estado))
    
    melhorVizinho.append(vizinho)
    #para cada intem em neighbours verifique:
    for n in vizinhos:
        #se o numero de conflitos em (neigh) for igual a (n), adicione (n) na lista (b_neigh)
    	if(h(vizinho) == h(n)):
    		melhorVizinho.append(n)
    global heuristica
    heuristica.append(h(vizinho))          
    #pos recebe um numero entre 0 e tamanho da lista (b_neigh -1)  
        
    pos = random.randint(0,len(melhorVizinho)-1)
    print('formação : ',vizinho)
    return melhorVizinho[pos]

def hillclimbing(N,estadoInicial):
     
	atual = estadoInicial
	contador = 0
	while True:
        #variavel recebe estados proximos para se mover rainhas
		vizinhos = buscaEstadosProximos(N, atual)
		#print('tamanho:',len(neighbours))
        #se nao existem então pare
		if not vizinhos:
		    break	
        #vizinho recebe resultado da busca dos melhores vizinhos
		vizinho = procuraVizinhos(vizinhos, estadoInicial)
		#print(neighbour)
        #se a quantidade de conflitos em (neighbour) for menor que em estado atual (current)
        #pare
		if h(vizinho) < h(atual):
		  break
      # contador +=1
		contador += 1 
		atual = vizinho
    
	print("Quantidade de mudanças até a resposta : ",contador)
	return atual
#############################
#variavel global para receber pontuação da solução

N = 8
#criando dataframe de estados
eixos = [i for i in range(N)]
estado_inicial  = pd.DataFrame(index=(eixos),columns=(eixos))
estado_final = pd.DataFrame(index=(eixos),columns=(eixos))

#gerando estado aleatório
estadoInicial = list(random.randrange(N) for i in range(N))
for i in range(len(estadoInicial)):
    estado_inicial[eixos[i]][estadoInicial[i]] = 'Rainha'   
    
#inicia hill climb    
inicio = time.time()
resultado = hillclimbing(N, estadoInicial)  
fim = time.time()

#Povoando dataframe com resultado
print_board(resultado)

'''verifica se o resultado segue as regras do problema'''
result = goal_test(resultado)

### plot grafico 


indices = [i for i in heuristica]    
colunas = [j for j in range(len(heuristica))]
 
data = {'Heuristica': indices,
        'Iterações': colunas}

dframe = pd.DataFrame(data,columns=['Heuristica','Iterações'])


dframe.plot(x='Iterações',y='Heuristica',kind='line')
plt.show()



memoria = (process.memory_info()[0])/1000000
print('memoria mbytes :',memoria,'\n','tempo em segundos :',(fim - inicio) )



