# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 13:25:14 2020

@author: Benjamim
"""

import time
import random
import math

'''Representação do problema'''

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
    #variavel utilizada para percorrer registros da lista
    id_voo = -1
    # // divide e retorna valor inteiro
    for i in range(len(agenda)//2):
        #obter nome da pessoa
        nome = pessoas[i][0]
        #obter aeroporto de partida
        origem = pessoas[i][1]
        id_voo += 1
        ida = voos[origem, destino][agenda[id_voo]]
        id_voo += 1
        volta = voos[(destino,origem)][agenda[id_voo]]
        print('%10s%10s %5s-%5s  R$%3s %5s-%5s R$%3s' % nome,origem,ida[0],ida[1],ida[2],volta[0],volta[1,volta[2]])
        

agenda = [1,4, 3,2, 7,3, 6,3, 2,4, 5,3]
