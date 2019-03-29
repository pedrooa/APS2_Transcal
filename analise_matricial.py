import numpy as np
from elemento import *
from node import *
from degreesOfFreedom import calc_dof
from Leitor_entrada import *


node_list, element_list = Reader(
    input("Qual arquivo deseja abrir?"))  # Leitura da entrada


calc_dof(node_list)   # Encontra os graus de liberdade de cada node


# MATRIZ PARA CADA ELEMENTO
for element in element_list:
    EA_L = (element.elasticity_value * element.area)/element.length

    c2 = element.cos**2
    cs = element.cos * element.sin
    s2 = element.sin**2

    c2 *= EA_L
    cs *= EA_L
    s2 *= EA_L

    ke_matrix = [	[c2, cs, -c2, -cs],
                  [cs, s2, -cs, -s2],
                  [-c2, -cs, c2, cs],
                  [-cs, -s2, cs, s2]]

    x1 = element.node_1.degrees[0]
    y1 = element.node_1.degrees[1]
    x2 = element.node_2.degrees[0]
    y2 = element.node_2.degrees[1]

    ke_matrix[0][0] = [ke_matrix[0][0], x1, x1]
    ke_matrix[0][1] = [ke_matrix[0][1], x1, y1]
    ke_matrix[0][2] = [ke_matrix[0][2], x1, x2]
    ke_matrix[0][3] = [ke_matrix[0][3], x1, y2]

    ke_matrix[1][0] = [ke_matrix[1][0], y1, x1]
    ke_matrix[1][1] = [ke_matrix[1][1], y1, y1]
    ke_matrix[1][2] = [ke_matrix[1][2], y1, x2]
    ke_matrix[1][3] = [ke_matrix[1][3], y1, y2]

    ke_matrix[2][0] = [ke_matrix[2][0], x2, x1]
    ke_matrix[2][1] = [ke_matrix[2][1], x2, y1]
    ke_matrix[2][2] = [ke_matrix[2][2], x2, x2]
    ke_matrix[2][3] = [ke_matrix[1][3], x2, y2]

    ke_matrix[3][0] = [ke_matrix[3][0], y2, x1]
    ke_matrix[3][1] = [ke_matrix[3][1], y2, y1]
    ke_matrix[3][2] = [ke_matrix[3][2], y2, x2]
    ke_matrix[3][3] = [ke_matrix[3][3], y2, y2]

    element.ke_matrix = ke_matrix

print(ke_matrix)


#####################################################################
# matriz global

# DEFINIR
number_of_nodes = len(node_list)

# lista com todos os elementos = elementos

# def matriz_global(element_list):
global_matrix = np.zeros((number_of_nodes, number_of_nodes))

for e in element_list:
    ke_matrix = e.ke_matrix

    for line in ke_matrix:
        for c in line:
            global_matrix[c[1]][c[2]] += c[0]

    #global_matrix = np.multiply(10**8, global_matrix)


#####################################################################
# Vetor global das forcas

global_list = []  # cond de contorno nao aplicadas
new_global_list = []  # cond de contorno aplicadas

# node.load = [x, y]   	---> formato do load dos nodes
# nodes = []				---> lista com todos os nodes da estrutura

for n in node_list:  # populando a lista completa
    global_list.append(n.load[0])
    global_list.append(n.load[1])


for n in node_list:  # populando a lista com as cond de controno aplicadas
    if(n != "x"):  # so adiciona os termos numericos e conhecidos
        new_global_list.append(n.load[0])
        new_global_list.append(n.load[1])

new_global_vector = np.array(new_global_list)
global_vector = np.array(global_list)

#####################################################################
# Aplicar as condicoes de contorno na matriz global

for i, item in enumerate(global_vector):
    if(item == "x"):  # nos itens q tiverem com uma incognita significa q tem uma codicao de contorno (tira o index deles da matriz)
        new_global_matrix = np.delete(global_matrix, (i), axis=0)
        new_global_matrix = np.delete(new_global_matrix, (i), axis=1)


#####################################################################
# 1 - resolver os sistemas de equacoes
'''
U_vector = np.linalg.solve(new_global_matrix, global_vector)
'''
# 2 - resolver os sistemas de equacoes por solucao numerica
U_vector = []

lte = 100
tol = 0.011

for i in range(len(global_vector)):
    X.append(0)  # UNICO ERRO

while(lte > 0):
    for i, item in enumerate(new_global_matrix):
        bi = global_vector[i]
        for l in range(len(item)):
            if(i == l):
                divisor = item[l]
            else:
                bi -= item[l] * U_vector[l]

        U_vector[i] = bi/divisor

    lte -= 1

print(U_vector)

#####################################################################
# completando o vetor U com os zeros

index_u = 0
full_U_vector = []  # lista com os zeros e os valores encontrados

for i, item in enumerate(global_vector):
    if(item == "x"):
        full_U_vector.append(0)
    else:
        full_U_vector.append(U_vector[index_u])
        index_u += 1

#####################################################################
# descobrindo o vetor de reacoes completo


full_global_vector = np.matmul(global_matrix, full_U_vector)


# PREENCHER OS RESULTADOS NOS ATRIBUTOS DOS ELEMENTOS E NODES
txt_out = "*DISPLACEMENTS\n"
for i in node_list:
    txt_out += str(i.id_number) + " " + str(i.displacement_x) + \
        " " + str(i.displacement_y) + "0.0000e+00\n"

txt_out += "*REACTION_FORCES\n"
for i in node_list:
    if(i.restriction[0] == 1):
        txt_out += str(i.id_number) + "FX = " + str(i.Rx) + "\n"
    if(i.restriction[1] == 2):
        txt_out += str(i.id_number) + "FY = " + str(i.Ry) + "\n"

txt_out += "*ELEMENT_STRAINS\n"
for e in element_list:
    txt_out += str(e.id_number) + str(e.strain) + "\n"
txt_out += "*ELEMENT_STRESSES\n"
for e in element_list:
    txt_out += str(e.id_number) + str(e.stress) + "\n"
