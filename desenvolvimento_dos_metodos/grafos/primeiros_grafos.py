# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 19:41:08 2020

@author: Benjamim
"""

from igraph import Graph
from igraph impot plot

'''Definição do grafo com as arestas'''
grafo1 = Graph(edges=[(0,1),(1,2),(2,3),(3,0)], directed = True)

'''Definição do rotulo de cada vertice'''
grafo1.vs['label']=range(grafo.vcount())
print(grafo1)