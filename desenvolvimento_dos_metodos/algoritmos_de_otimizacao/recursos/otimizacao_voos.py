import time
import random
import math

pessoas = [('Amanda', 'CWB'),
           ('Pedro', 'GIG'),
           ('Marcos', 'POA'),
           ('Priscila', 'FLN'),
           ('Jessica', 'CNF'),
           ('Paulo', 'GYN')]

destino = 'GRU'

voos = {}
for linha in open('voos.txt'):
    #print(linha)
    _origem, _destino, _saida, _chegada, _preco = linha.split(',')
    voos.setdefault((_origem, _destino), [])
    voos[(_origem, _destino)].append((_saida, _chegada, int(_preco)))
    
# [1,4, 3,2, 7,3, 6,3, 2,4, 5,3]
def imprimir_agenda(agenda):
    id_voo = -1
    for i in range(len(agenda) // 2):
        nome = pessoas[i][0] 
        origem = pessoas[i][1]
        id_voo += 1
        ida = voos[(origem, destino)][agenda[id_voo]]
        id_voo += 1
        volta = voos[(destino, origem)][agenda[id_voo]]
        print('%10s%10s %5s-%5s R$%3s %5s-%5s R$%3s' % (nome, origem, ida[0], ida[1], ida[2],
                                                       volta[0], volta[1], volta[2]))
        
agenda = [1,4, 3,2, 7,3, 6,3, 2,4, 5,3]
imprimir_agenda(agenda)

def get_minutos(hora):
    x = time.strptime(hora, '%H:%M')
    minutos = x[3] * 60 + x[4]
    return minutos

get_minutos('6:13')
get_minutos('23:59')
get_minutos('00:00')

def funcao_custo(solucao):
    preco_total = 0
    ultima_chegada = 0
    primeira_partida = 1439
    
    id_voo = -1
    for i in range(len(solucao) // 2):
        origem = pessoas[i][1]
        id_voo += 1
        ida = voos[(origem, destino)][solucao[id_voo]]
        id_voo += 1
        volta = voos[(destino, origem)][solucao[id_voo]]
        
        preco_total += ida[2]
        preco_total += volta[2]
        
        if ultima_chegada < get_minutos(ida[1]):
            ultima_chegada = get_minutos(ida[1])
            
        if primeira_partida > get_minutos(volta[0]):
            primeira_partida = get_minutos(volta[0])
            
    total_espera = 0
    id_voo = -1
    for i in range(len(solucao) // 2):
        origem = pessoas[i][1]
        id_voo += 1
        ida = voos[(origem, destino)][solucao[id_voo]]
        id_voo += 1
        volta = voos[(destino, origem)][solucao[id_voo]]
        
        total_espera += ultima_chegada - get_minutos(ida[1])
        total_espera += get_minutos(volta[0]) - primeira_partida
        
    if ultima_chegada > primeira_partida:
        preco_total += 50
        
    return preco_total + total_espera
        
funcao_custo(agenda)  

def pesquisa_randomica(dominio, funcao_custo):
    melhor_custo = 999999999
    for i in range(0, 10000):
        solucao = [random.randint(dominio[i][0], dominio[i][1]) for i in range(len(dominio))]
        custo = funcao_custo(solucao)
        if custo < melhor_custo:
            melhor_custo = custo
            melhor_solucao = solucao
    return melhor_solucao
     
dominio = [(0,9)] * (len(pessoas) * 2)
solucao_randomica = pesquisa_randomica(dominio, funcao_custo)
custo_randomica = funcao_custo(solucao_randomica)
imprimir_agenda(solucao_randomica)
    
def subida_encosta(dominio, funcao_custo):
    solucao = [random.randint(dominio[i][0], dominio[i][1]) for i in range(len(dominio))]
    while True:
        vizinhos = []
        
        for i in range(len(dominio)):
            if solucao[i] > dominio[i][0]:
                if solucao[i] != dominio[i][1]:
                    vizinhos.append(solucao[0:i] + [solucao[i] + 1] + solucao[i + 1:])
            if solucao[i] < dominio[i][1]:
                if solucao[i] != dominio[i][0]:
                    vizinhos.append(solucao[0:i] + [solucao[i] - 1] + solucao[i + 1:])
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

solucao_subida_encosta = subida_encosta(dominio, funcao_custo)
custo_subida_encosta = funcao_custo(solucao_subida_encosta)
imprimir_agenda(solucao_subida_encosta)
                    
def tempera_simulada(dominio, funcao_custo, temperatura = 10000.0, resfriamento = 0.95, passo = 1):
    solucao = [random.randint(dominio[i][0], dominio[i][1]) for i in range(len(dominio))]

    while temperatura > 0.1:
        i = random.randint(0, len(dominio) - 1) 
        direcao = random.randint(-passo, passo)
        
        solucao_temp = solucao[:]
        solucao_temp[i] += direcao
        if solucao_temp[i] < dominio[i][0]:
            solucao_temp[i] = dominio[i][0]
        elif solucao_temp[i] > dominio[i][1]:
            solucao_temp[i] = dominio[i][1]
            
        custo_solucao = funcao_custo(solucao)
        custo_solucao_temp = funcao_custo(solucao_temp)
        probabilidade = pow(math.e, (-custo_solucao_temp - custo_solucao) / temperatura)
        
        if (custo_solucao_temp < custo_solucao or random.random() < probabilidade):
            solucao = solucao_temp
        
        temperatura = temperatura * resfriamento
    return solucao

solucao_tempera_simulada = tempera_simulada(dominio, funcao_custo)
custo_tempera_simulada = funcao_custo(solucao_tempera_simulada)
imprimir_agenda(solucao_tempera_simulada)


def mutacao(dominio, passo, solucao):
    i = random.randint(0, len(dominio) - 1)
    mutante = solucao
    
    if random.random() < 0.5:
        if solucao[i] != dominio[i][0]:
            mutante = solucao[0:i] + [solucao[i] - passo] + solucao[i + 1:]
    else:
        if solucao[i] != dominio[i][1]:
            mutante = solucao[0:i] + [solucao[i] + passo] + solucao[i + 1:]
    
    return mutante

s = [1,4, 3,2, 7,3, 6,3, 2,4, 5,3]
s1 = mutacao(dominio, 1, s)

def cruzamento(dominio, solucao1, solucao2):
    i = random.randint(1, len(dominio) - 2)
    return solucao1[0:i] + solucao2[i:]

s1 = [1,4, 3,2, 7,3, 6,3, 2,4, 5,3]
s2 = [0,1, 2,5, 8,9, 2,3, 5,1, 0,6]
s3 = cruzamento(dominio, s1, s2)

def genetico(dominio, funcao_custo, tamanho_populacao = 100, passo = 1,
             probabilidade_mutacao = 0.2, elitismo = 0.2, numero_geracoes = 500):
    
    populacao = []
    for i in range(tamanho_populacao):
        solucao = [random.randint(dominio[i][0], dominio[i][1]) for i in range(len(dominio))]
        populacao.append(solucao)
    
    numero_elitismo = int(elitismo * tamanho_populacao)
    
    for i in range(numero_geracoes):
        custos = [(funcao_custo(individuo), individuo) for individuo in populacao]
        custos.sort()
        individuos_ordenados = [individuo for (custo, individuo) in custos]
        
        populacao = individuos_ordenados[0:numero_elitismo]
        
        while len(populacao) < tamanho_populacao:
            if random.random() < probabilidade_mutacao:
                m = random.randint(0, numero_elitismo)
                populacao.append(mutacao(dominio, passo, individuos_ordenados[m]))
            else:
                c1 = random.randint(0, numero_elitismo)
                c2 = random.randint(0, numero_elitismo)
                populacao.append(cruzamento(dominio, individuos_ordenados[c1], 
                                            individuos_ordenados[c2]))
                
    return custos[0][1]

solucao_genetico = genetico(dominio, funcao_custo)
custo_genetico = funcao_custo(solucao_genetico)
imprimir_agenda(solucao_genetico)

























    