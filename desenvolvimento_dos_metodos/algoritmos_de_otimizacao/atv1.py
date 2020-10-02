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
    voos[(_origem,_destino)].append((_saida,_chegada,int(_preco)))
