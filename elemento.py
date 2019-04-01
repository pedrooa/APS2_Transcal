
from node import *
import math


class Element:
    def __init__(self, id_number, node_1, node_2, geometric_value=None):
        self.id_number = id_number
        # Node_1 e node_2
        self.node_1 = node_1
        self.node_2 = node_2
        # Modulo de elasticidade
        self.elasticity_value = 0
        # tensao de tração admissível
        self.max_traction = 0
        # tensão a compressão admissível
        self.max_tension = 0
        # seção transversal da barra
        self.area = geometric_value
        # tamanho da barra
        self.length = self.calc_length()
        self.stress = 0  # COLOCAR AQUI RESULTADOS
        self.strain = 0  # COLOCAR AQUI RESULTADOS
        # cosseno da barra
        self.cos = (self.node_2.coordinates[0] -
                    self.node_1.coordinates[0])/self.length
        self.sin = (self.node_2.coordinates[1] -
                    self.node_1.coordinates[1])/self.length
        # self.cos = math.cos(self.calc_angle())
        # if(-0.001 < self.cos < 0.001):
        #     self.cos = 0
        # seno da barra
        # self.sin = math.sin(self.calc_angle())
        # if(-0.001 < self.sin < 0.001):
        #     self.sin = 0
        # Matriz de rigidez de elemento de barra no sistema global
        self.ke_matrix = [0][0]

    def calc_length(self):
        length = float(math.sqrt((self.node_1.coordinates[0] - self.node_2.coordinates[0])**2 + (
            self.node_1.coordinates[1] - self.node_2.coordinates[1])**2))
        if(length < 0.001):
            return 0
        return length

    # def calc_angle(self):
    #     if(abs(self.node_2.coordinates[0] - self.node_1.coordinates[0]) == 0):
    #         return math.pi/2
    #     angle = math.atan((self.node_1.coordinates[1] - self.node_2.coordinates[1])/(
    #         self.node_1.coordinates[0] - self.node_2.coordinates[0]))
    #     if(-0.001 < angle < 0.001):
    #         return 0
    #     return 2*math.pi-angle
