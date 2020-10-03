# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 13:25:14 2020

@author: Benjamim
"""
import time
import random
import math

'''---Representação do problema---'''

pessoas = [('Amanda','CWB'),
           ('Pedro','GIG'),
           ('Marcos','POA'),
           ('Priscila','FLN'),
           ('Jessica','CNF'),
           ('Paulo','GYN')]

destino = 'GRU'

'''Intanciar base de dados de voos em um dicionario'''
voos = {}

for linha in open('recursos/voos.txt'):
    '''criar variaveis locais p/cada coluna'''
    _origem, _destino, _saida, _chegada, _preco = linha.split(',')
    
    '''adiciona chaves ao dicionario '''
    voos.setdefault((_origem,_destino), [])
    
    '''gerar dicionario com todos os hoarios de voos de ou para guarulhos GRU'''
    voos[(_origem,_destino)].append((_saida,_chegada,int(_preco)))

'''listar voos escolhidos'''
def imprimir_agenda(agenda):
    contador = 0
    #variavel utilizada para percorrer registros da lista
    id_voo = -1
    # // divide e retorna valor inteiro
    for i in range(len(agenda)//2):
        contador +=1
        #obter nome da pessoa
        nome = pessoas[i][0]
        #obter aeroporto de partida
        origem = pessoas[i][1]
        id_voo += 1
        ida = voos[(origem, destino)][agenda[id_voo]]
        id_voo += 1
        volta = voos[(destino, origem)][agenda[id_voo]]
        print('%10s%10s %5s-%5s  R$%3s %5s-%5s R$%3s' % (nome, origem, ida[0],
              ida[1], ida[2], volta[0], volta[1], volta[2]))
    print(contador)
        
agenda = [1,4, 3,2, 7,3, 6,3, 2,4, 5,3]
#imprimir_agenda(agenda)
''' ---Inicio função de custo ---
    definindo o custo de tempo em minutos'''

def get_minutos(hora):
    #convertendo valores string
    x = time.strptime(hora,'%H:%M')
    #convertendo horas em minutos
    minutos = x[3] * 60 + x[4]
    return minutos

'''definindo função de custo'''
def funcao_custo(solucao):
    preco_total = 0
    ultima_chegada = 0
    #voo mais tarde 23:59
    primeira_partida = 1439
    
    id_voo = -1
    for i in range(len(solucao) // 2):
        #aeroporto de origem
        origem = pessoas[i][1]
        id_voo +=1
        ida = voos[(origem,destino)][solucao[id_voo]]
        id_voo +=1
        volta = voos[(destino,origem)][solucao[id_voo]]
        
        preco_total += ida[2]
        preco_total +=volta[2]
        
        if ultima_chegada < get_minutos(ida[1]):
            ultima_chegada = get_minutos(ida[1])
                        
        if primeira_partida > get_minutos(volta[0]):
            primeira_partida = get_minutos(volta[0])        
        
    total_espera = 0 
    id_voo = -1
    for i in range(len(solucao) // 2):
        origem = pessoas[i][1]
        id_voo +=1
        ida = voos[(origem,destino)][solucao[id_voo]]
        id_voo +=1
        volta = voos[(destino,origem)][solucao[id_voo]]
        
        total_espera += ultima_chegada - get_minutos(ida[1])
        total_espera += get_minutos(volta[0]) - primeira_partida
        
    if ultima_chegada > primeira_partida:
        preco_total += 50
        
    return preco_total + total_espera

''' ---inicio tecnicas de otimização--- '''
# 1 implementação pesquisa aleatoria ou randomica
def perquisa_randomica(dominio,funcao_custo):
    melhor_custo = 9999999999
    for i in range(0,1000):
        solucao = [random.randint(dominio[i][0],dominio[i][1]) for i in range(len(dominio))]
        custo = funcao_custo(solucao)
        if custo < melhor_custo:
            melhor_custo = custo
            melhor_solucao = solucao
    return melhor_solucao
    
dominio = [(0,9)] * (len(pessoas) * 2) 
'''  
solucao_randomica = perquisa_randomica(dominio,funcao_custo)
custo_randomica = funcao_custo(solucao_randomica)
imprimir_agenda(solucao_randomica)'''
            
''' ---hill climb---'''
# Comeca comeca com uma solucao aleatoria e procura os melhores vizinhos            
def subida_encosta(dominio,funcao_custo):
    #definindo solucao randomica
    solucao = [random.randint(dominio[i][0],dominio[i][1]) for i in range(len(dominio))]
    while True:
        vizinhos = []
        for i in range(len(dominio)):
            if solucao[i] > dominio[i][0]:
                if solucao[i] != dominio[i][1]:
                    vizinhos.append(solucao[0:i] + [solucao[i] + 1] + solucao[i + 1:])
            if solucao[i]<dominio[i][1]:
                if solucao[i] != dominio[i][0]:
                    vizinhos.append(solucao[0:i] + [solucao[i] - 1] + solucao[i + 1:])
        
        '''calculando custo'''
        atual = funcao_custo(solucao)
        melhor = atual
        for i in range(len(vizinhos)):
            custo = funcao_custo(vizinhos[i])
            if custo < melhor:
                melhor = custo
                solucao = vizinhos[i]
        
        if melhor == atual:
            break
        
    return solucao

solucao_subida_encosta = subida_encosta(dominio,funcao_custo)
custo_suboda_encosta = funcao_custo(solucao_subida_encosta)
imprimir_agenda(solucao_subida_encosta)
        
        
        
        
        
        
    



    
    
    
    
    
    
    
    
    
    
    
    
    
    



