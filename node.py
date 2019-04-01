class Node:
    def __init__(self, id_number, coordinates):
        self.id_number = id_number
        self.coordinates = coordinates
        self.restrictions = [0, 0]
        self.load = [0, 0]
        self.degrees = [0, 0]  # degrees of freedom
        self.displacement_x = 0  # COLOCAR AQUI O RESULTADO DO DESOLOCAMENTO
        self.displacement_y = 0  # COLOCAR AQUI O RESULTADO DO DESLOCAMENTO
        self.Rx = 0             # COLOCAR AQUI O RESULTADO DO DESLOCAMENTO
        self.Ry = 0            # COLOCAR AQUI O RESULTADO DO DESLOCAMENTO
