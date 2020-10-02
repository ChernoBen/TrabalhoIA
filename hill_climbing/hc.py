# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 10:39:12 2020

@author: Benjamim
"""
import random

def subida_encosta(dominio,funcao_custo):
    solucao = [randon.randint(dominio[i][0],dominio[i][1]) for i in range(len(dominio))]
    while True:
        vizinhos = []
        for i in range (len(dominio)):
            if solucao[i] > dominio[i][0]:
                if solucao[i] != dominio[i][1]:
                    vizinhos.append(solucao[0:i]+ [solucao[i] + 1] + solucao[i + 1:])
            if solucao[i] < dominio[i][1]:
                if solucao[i] != dominio[i][0]:
                    vizinhos.append(solucao[0:i]+[solucao[i]-1] + solucao[i+1:])
                    
        '''calcular custo'''
        atual = funcao_custo(solucao)
        melhor = atual
        for i in range(len(vizinhos)):
            custo = funcao_custo(vizinhos[i])
            if custo<melhor:
                melhor = custo
                solucao = vizinhos[i]
                
            if melhor == atual:
                break
            
    return solucao

solucao_subida_encosta = subida_encosta(dominio, funcao_custo)
custo_subida_encosta = funcao_custo(solucao_subida_encosta)
imprimir_agenda(solucao_subida_encosta)