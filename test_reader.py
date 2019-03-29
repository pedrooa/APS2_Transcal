class Node:
    def __init__(self, id_number, restrictions):
        self.id_number = id_number
        self.load = restrictions


def coordinates(parameters, node_list, element_list):
    # Pula ("COORDINATES" e numero de elementos)
    for coordinates in parameters[2::]:
        coordinates = coordinates.split()
        if(len(coordinates) != 0):
            print(coordinates[0], [coordinates[1], coordinates[2]])
    return node_list, element_list


def bc_nodes(parameters, node_list, element_list):
    parameters = parameters[2::]
    for i in parameters:
        e = i.split()
        # print(e)
        if(len(e) > 0):
            for node in node_list:
                if(node.id_number == int(e[0])):
                    if(int(e[1]) == 1):
                        node.restrictions[0] = 1
                    if(int(e[1]) == 2):
                        node.restrictions[1] = 2
    return node_list, element_list


def loads(parameters, node_list, element_list):
    parameters = parameters[2::]
    for i in parameters:
        e = i.split()
        if(len(e) > 0):
            for node in node_list:
                if(node.id_number == int(e[0])):

                    if(int(e[1]) == 1):
                        node.load[0] = int(e[2])
                    if(int(e[1]) == 2):
                        node.load[1] = int(e[2])

    return node_list, element_list


def materials(parameters, node_list, element_list):
    parameters = parameters[2::]
    print(parameters)
    for i in range(len(parameters)):
        mater = parameters[i].split()
        e = 0
        while(e < len(mater)):
            if 'E' in mater[e]:
                value = mater[e].split('E')
                mater[e] = float(float(value[0]))*(10**int(value[1]))
            else:
                mater[e] = float(e)
            e += 1
        print(mater)
    return node_list, element_list


def Reader(file_name):

    nodes = [Node(1, [0, 0]), Node(2, [0, 0]), Node(3, [0, 0])]
    elements = []

    key_words = {
        "COORDINATES": coordinates,
        "ELEMENT_GROUPS": "Elementos",
        "INCIDENCES": "Incidencias",
        "MATERIALS": materials,
        "GEOMETRIC_PROPERTIES": "propriedades geometricas",
        "BCNODES": bc_nodes,
        "LOADS": loads
    }

    with open(file_name, 'r') as text_input:

        body = text_input.read().replace("\n", ",").replace("\r", '').split(
            '*')
        counter = ''
        for parameters in body:
            for letter in parameters:
                if letter == ",":
                    break
                counter += letter
            if counter in key_words.keys():
                if(counter == "LOADS"):
                    nodes, elements = key_words[counter](
                        parameters.split(','), nodes, elements)
                counter = ''
        return nodes, elements


Reader(input("Qual arquivo deseja abrir?"))
