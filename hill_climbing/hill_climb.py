import psutil
import random
from random import choice
import time
import pandas as pd

def print_board(state_board):
    for i in range( len(state_board) ):
        for j in range( len(state_board) ):
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

def nearStates(N_Queens,state):
    near_states = []
    # Para cada state[coluna] verfica se as colunas vizinhas estao vazias
    for row in range(N_Queens):
        for col in range(N_Queens):
            if col != state[row]:
                aux = list(state)
                aux[row] = col  # Troca a coluna para a vazia
                near_states.append(list(aux))  # E inclui na lista de nearStates
    #print('near_states:',near_states)
    return near_states


def he(state):
    
    #Return number of conflicting queens for a given node
    num_conflicts = 0
    for (r1, c1) in enumerate(state):
        for (r2, c2) in enumerate(state):
            if (r1, c1) != (r2, c2):
                num_conflicts += conflict(r1, c1, r2, c2)
    #retorna a quantidade de conlitos negativo dividido p/2   
              
    return -num_conflicts/2


def randomNearStates(N_Queens, state):
    #recebe o numero de rainhas e a lista contendo o estado
    # e retorna um elemento aleatorio dentro da lista retornada pela função nearStates
    return choice( nearStates(N_Queens, state) )

def search_bests_neighs(neighbours, state):
    #lista de melhores vizinhos
    b_neigh = []
    #
    neigh = max(neighbours, key=lambda state: he(state))
    b_neigh.append(neigh)
    #para cada intem em neighbours verifique:
    for n in neighbours:
        #se o numero de conflitos em (neigh) for igual a (n), adicione (n) na lista (b_neigh)
    	if(he(neigh) == he(n)):
    		b_neigh.append(n)
    #pos recebe um numero entre 0 e tamanho da lista (b_neigh -1)        
    pos = random.randint(0,len(b_neigh)-1)
    print('search:',neigh)
    return b_neigh[pos]

def hill_climbing(N_Queens,state):

	current = state
	count_t = 0
	while True:
        #variavel recebe estados proximos para se mover rainhas
		neighbours = nearStates(N_Queens, current)
		#print('tamanho:',len(neighbours))
        #se nao existem então pare
		if not neighbours:
		    break	
        #vizinho recebe resultado da busca dos melhores vizinhos
		neighbour = search_bests_neighs(neighbours, state)
		#print(neighbour)
        #se a quantidade de conflitos em (neighbour) for menor que em estado atual (current)
        #pare
		if he(neighbour) < he(current):
		  break
      # contador +=1
		count_t += 1 
		current = neighbour
	print("Quantidade de mudanças até a resposta : ",count_t,'\n','loss :',he(neighbour))
	return current
#############################
floss = 0
N = 8
#criando dataframe de estados
eixos = [i for i in range(N)]
estado_inicial  = pd.DataFrame(index=(eixos),columns=(eixos))
estado_final = pd.DataFrame(index=(eixos),columns=(eixos))

#gerando estado aleatório
state_board = list(random.randrange(N) for i in range(N))
for i in range(len(state_board)):
    estado_inicial[eixos[i]][state_board[i]] = 'Rainha'    
begin = time.time()
state_board = hill_climbing(N, state_board)  
end = time.time()

#Povoando dataframe com resultado
print_board(state_board)
'''verifica se o resultado segue as regras do problema'''
print(goal_test(state_board))
'''note que a ultima lista impressa contem conflitos'''
print("{:.5f}ms".format((end - begin) * 1000))
print(psutil.swap_memory())