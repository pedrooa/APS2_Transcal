import numpy as np
from elemento import *
from node import *
from degreesOfFreedom import calc_dof
from Leitor_entrada import *


# Leitura da entrada
node_list, element_list = Reader(
    input("Qual arquivo deseja abrir?"))


# Encontra os graus de liberdade de cada node
calc_dof(node_list)

for n in node_list:
    if(n.restrictions[0] == 1):
        n.load[0] = "x"
    if(n.restrictions[1] == 1):
        n.load[1] = "x"
    print("#########node id: {}########".format(n.id_number))
    print("Coordinates : ", n.coordinates)
    print("Restricoes : ", n.restrictions)
    print("Loads : ", n.load)
    print("graus de liberdade", n.degrees)
    print("########################")


# MATRIZ PARA CADA ELEMENTO
for element in element_list:
    EA_L = (element.elasticity_value * element.area)/element.length

    c2 = element.cos**2
    cs = element.cos * element.sin
    s2 = element.sin**2

    c2 *= EA_L
    cs *= EA_L
    s2 *= EA_L

    element.ke_matrix = [[c2, cs, -c2, -cs],
                         [cs, s2, -cs, -s2],
                         [-c2, -cs, c2, cs],
                         [-cs, -s2, cs, s2]]

    # counter1 = 0
    # counter2 = 0
    # while(counter1 < element.ke_matrix[0]):

    x1 = element.node_1.degrees[0]
    y1 = element.node_1.degrees[1]
    x2 = element.node_2.degrees[0]
    y2 = element.node_2.degrees[1]
    for counter1, e in enumerate(element.ke_matrix):
        for counter2, i in enumerate(e):
            if(-0.001 < i < 0.001):
                element.ke_matrix[counter1][counter2] = 0
            else:
                element.ke_matrix[counter1][counter2] = i/10

    element.ke_matrix[0][0] = [element.ke_matrix[0][0], x1, x1]
    element.ke_matrix[0][1] = [element.ke_matrix[0][1], x1, y1]
    element.ke_matrix[0][2] = [element.ke_matrix[0][2], x1, x2]
    element.ke_matrix[0][3] = [element.ke_matrix[0][3], x1, y2]

    element.ke_matrix[1][0] = [element.ke_matrix[1][0], y1, x1]
    element.ke_matrix[1][1] = [element.ke_matrix[1][1], y1, y1]
    element.ke_matrix[1][2] = [element.ke_matrix[1][2], y1, x2]
    element.ke_matrix[1][3] = [element.ke_matrix[1][3], y1, y2]

    element.ke_matrix[2][0] = [element.ke_matrix[2][0], x2, x1]
    element.ke_matrix[2][1] = [element.ke_matrix[2][1], x2, y1]
    element.ke_matrix[2][2] = [element.ke_matrix[2][2], x2, x2]
    element.ke_matrix[2][3] = [element.ke_matrix[2][3], x2, y2]

    element.ke_matrix[3][0] = [element.ke_matrix[3][0], y2, x1]
    element.ke_matrix[3][1] = [element.ke_matrix[3][1], y2, y1]
    element.ke_matrix[3][2] = [element.ke_matrix[3][2], y2, x2]
    element.ke_matrix[3][3] = [element.ke_matrix[3][3], y2, y2]
    # print(element.ke_matrix)


#####################################################################
# matriz global

# DEFINIR
number_of_nodes = len(node_list)

# lista com todos os elementos = element_list

global_matrix = np.zeros((number_of_nodes*2, number_of_nodes*2))

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

    if(n.load[0] != "x"):  # so adiciona os termos numericos e conhecidos
        new_global_list.append(n.load[0])
    if(n.load[1] != "x"):  # so adiciona os termos numericos e conhecidos
        new_global_list.append(n.load[1])

new_global_vector = np.array(new_global_list)
global_vector = np.array(global_list)


#####################################################################
# Aplicar as condicoes de contorno na matriz global

new_global_matrix = global_matrix
temp = 0

for i, item in enumerate(global_vector):
    if(item == 'x'):  # nos itens q tiverem com uma incognita significa q tem uma codicao de contorno (tira o index deles da matriz)
        new_global_matrix = np.delete(new_global_matrix, i-temp, axis=0)
        new_global_matrix = np.delete(new_global_matrix, i-temp, axis=1)
        temp += 1

#####################################################################
U_vector = []

lte = 100
tol = 0.011

for i in range(len(new_global_vector)):
    U_vector.append(0)

while(lte > 0):
    for i, item in enumerate(new_global_matrix):
        bi = new_global_vector[i]
        for l in range(len(item)):
            if(i == l):
                divisor = item[l]
            else:
                bi -= item[l] * U_vector[l]

        U_vector[i] = bi/divisor

    lte -= 1

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
count = 0
for node in node_list:
    node.displacement_x = full_U_vector[count]
    count += 1
    node.displacement_y = full_U_vector[count]
    count += 1


#####################################################################
# descobrindo o vetor de reacoes completo


full_global_vector = np.matmul(global_matrix, full_U_vector)
# print("full_global_vector ------> ", full_global_vector)  # vetor das forcas
count = 0
for node in node_list:
    node.Rx = full_global_vector[count]
    count += 1
    node.Ry = full_global_vector[count]
    count += 1


#####################################################################
# descobrindo a deformacao e tensao de cada elemento
index = 0
for e in element_list:
    # print(e.length)
    # print(e.node_1.degrees)
    # print(e.node_2.degrees)
    u1 = full_U_vector[index]
    v1 = full_U_vector[index + 1]

    if(index + 4 > len(full_U_vector)):
        index = -2
    u2 = full_U_vector[index + 2]
    v2 = full_U_vector[index + 3]
    e.strain = 1/e.length * \
        np.dot([-e.cos, -e.sin, e.cos, e.sin], [u1, v1, u2, v2])
    e.stress = e.strain * e.elasticity_value
    index += 2
    # print(e.strain)  # deformacao de cada elemento
    # print(e.stress)  # tensao em cada elemento

#####################################################################
# PREENCHER OS RESULTADOS NOS ATRIBUTOS DOS ELEMENTOS E NODES
txt_out = "*DISPLACEMENTS\n"
for i in node_list:
    txt_out += str(i.id_number) + " " + str(i.displacement_x) + \
        " " + str(i.displacement_y) + " 0.0000e+00\n"

txt_out += "*REACTION_FORCES\n"
for i in node_list:
    if(i.restrictions[0] == 1):
        txt_out += str(i.id_number) + " " + "FX = " + str(i.Rx) + "\n"
    if(i.restrictions[1] == 1):
        txt_out += str(i.id_number) + " " + "FY = " + str(i.Ry) + "\n"

txt_out += "*ELEMENT_STRAINS\n"
for e in element_list:
    txt_out += str(e.id_number) + " " + str(e.strain) + "\n"
txt_out += "*ELEMENT_STRESSES\n"
for e in element_list:
    txt_out += str(e.id_number) + " " + str(e.stress) + "\n"

out = open("arquivoSaida.out", "w+")
out.write(txt_out)
out.close()
