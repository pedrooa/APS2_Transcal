
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
        self.cos = math.cos(self.calc_angle())
        # seno da barra
        self.sin = math.sin(self.calc_angle())
        # Matriz de rigidez de elemento de barra no sistema global
        self.ke_matrix = []

    def calc_length(self):
        return float(math.sqrt((self.node_1.x - self.node_2.x)**2 + (self.node_1.y - self.node_2.y)**2))

    def calc_angle(self):
        return math.atan(abs(self.node_1.y - self.node_2.y)/abs(self.node_1.x - self.node_2.x))
