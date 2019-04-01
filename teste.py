import numpy as np
import math
from elemento import *
from node import *
from degreesOfFreedom import calc_dof
from Leitor_entrada import *

# DADOS PARA TESTE


class Element:
    def __init__(self, id_number, node_1, node_2, geometric_value=None):
        self.id_number = id_number
        # Node_1 e node_2
        self.node_1 = node_1
        self.node_2 = node_2
        # Modulo de elasticidade
        self.elasticity_value = 210 * (10**8)
        # tensao de tração admissível
        self.max_traction = 0
        # tensão a compressão admissível
        self.max_tension = 0
        # seção transversal da barra
        self.area = 2 * 10**(-4)
        # tamanho da barra
        #self.length = self.calc_length()
        self.stress = 0  # COLOCAR AQUI RESULTADOS
        self.strain = 0  # COLOCAR AQUI RESULTADOS
        # cosseno da barra
        #self.cos = math.cos(self.calc_angle())
        # seno da barra
        #self.sin = math.sin(self.calc_angle())
        # Matriz de rigidez de elemento de barra no sistema global
        self.ke_matrix = [0][0]


class Node:
    def __init__(self, id_number, coordinates, restrictions=[0, 0], loads=[0, 0]):
        self.id = id_number
        self.coordinates = coordinates
        self.restrictions = restrictions
        if(restrictions[0] == 1):
            loads[0] = "x"
        if(restrictions[1] == 1):
            loads[1] = "x"
        self.load = loads
        self.degrees = [0, 0]  # degrees of freedom
        self.displacement_x = 0  # COLOCAR AQUI O RESULTADO DO DESOLOCAMENTO
        self.displacement_y = 0  # COLOCAR AQUI O RESULTADO DO DESLOCAMENTO
        self.Rx = 0             # COLOCAR AQUI O RESULTADO DO DESLOCAMENTO
        self.Ry = 0            # COLOCAR AQUI O RESULTADO DO DESLOCAMENTO


#elasticity_value = 210 * (10**8)
#area = 2 * 10**(-4)

n0 = Node(0, [0, 0], [1, 0], [0, 0])
n0.degrees = [0, 1]

n1 = Node(1, [0, 0.4], [1, 1], [0, 0])
n1.degrees = [2, 3]

n2 = Node(2, [0.3, 0.4], [0, 0], [150, -100])
n2.degrees = [4, 5]


#######################################


e0 = Element(1, n0, n1)
e0.length = 0.4
e0.cos = 0
e0.sin = 1
e0.node_1.degrees = [0, 1]
e0.node_2.degrees = [2, 3]


e1 = Element(2, n1, n2)
e1.length = 0.3
e1.cos = 1
e1.sin = 0
e1.node_1.degrees = [2, 3]
e1.node_2.degrees = [4, 5]

e2 = Element(3, n2, n0)
e2.length = 0.5
e2.cos = -0.6
e2.sin = -0.8
e2.node_1.degrees = [4, 5]
e2.node_2.degrees = [0, 1]


element_list = [e0, e1, e2]

#######################################

'''
# Leitura da entrada
node_list, element_list = Reader(
    input("Qual arquivo deseja abrir?"))
'''

# Encontra os graus de liberdade de cada node
# calc_dof(node_list)


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

    x1 = element.node_1.degrees[0]
    y1 = element.node_1.degrees[1]
    x2 = element.node_2.degrees[0]
    y2 = element.node_2.degrees[1]

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

    print(element.ke_matrix)


#####################################################################
# matriz global

# DEFINIR
node_list = [n0, n1, n2]
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
# 1 - resolver os sistemas de equacoes
'''
U_vector = np.linalg.solve(new_global_matrix, global_vector)
'''
# 2 - resolver os sistemas de equacoes por solucao numerica
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


print("full_U_vector ------> ", full_U_vector)  # vetor dos deslocamentos
#####################################################################
# descobrindo o vetor de reacoes completo


full_global_vector = np.matmul(global_matrix, full_U_vector)
print("full_global_vector ------> ", full_global_vector)  # vetor das forcas

#####################################################################
# descobrindo a deformacao e tensao de cada elemento
index = 0
for e in element_list:
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
    print(e.strain)  # deformacao de cada elemento
    print(e.stress)  # tensao em cada elemento

#####################################################################
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

out = open("arquivoSaida.out", "w+")
out.write(txt_out)
out.close()
