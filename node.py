class Node:
    def __init__(self, id_number, coordinates, restrictions=[], loads=[]):
        self.id = id_number
        self.coordinates = coordinates
        self.restrictions = restrictions
        self.load = loads
        self.degrees = []  # degrees of freedom
        self.displacement_x = 0  # COLOCAR AQUI O RESULTADO DO DESOLOCAMENTO
        self.displacement_y = 0  # COLOCAR AQUI O RESULTADO DO DESLOCAMENTO
        self.Rx = 0             # COLOCAR AQUI O RESULTADO DO DESLOCAMENTO
        self.Ry = 0            # COLOCAR AQUI O RESULTADO DO DESLOCAMENTO
