from elemento import Element
from degreesOfFreedom import calc_dof
from node import Node


def coordinates(parameters, node_list, element_list):
    # Pula ("COORDINATES" e numero de elementos)
    for coordinates in parameters[2::]:
        coordinates = coordinates.split()
        if(len(coordinates) != 0):
            node = Node(int(coordinates[0]), [
                        float(coordinates[1]), float(coordinates[2])])
            node_list.append(node)
    return node_list, element_list


def incidences(parameters, node_list, element_list):
    print(node_list[0])
    for incidence in parameters[1::]:
        incidence = incidence.split()
        if(len(incidence) != 0):
            for node in node_list:
                if(int(incidence[1]) == node.id_number):
                    node_1 = node
                if(int(incidence[2]) == node.id_number):
                    node_2 = node
            element = Element(int(incidence[0]), node_1, node_2)
            element_list.append(element)
    return node_list, element_list


def materials(parameters, node_list, element_list):
    parameters = parameters[2::]
    for i in range(len(parameters)):
        mater = parameters[i].split()
        e = 0
        while(e < len(mater)):
            if 'E' in mater[e]:
                value = mater[e].split('E')
                mater[e] = float(float(value[0]))*(10**int(value[1]))
            else:
                mater[e] = float(mater[e])
            e += 1
            element_list[i].elasticity_value = mater[0]
            element_list[i].max_traction = mater[1]
            element_list[i].max_tension = mater[2]

    return node_list, element_list


def geom_properties(parameters, node_list, element_list):
    parameters = parameters[2::]
    e = 0
    while(e < len(parameters)):
        if 'E' in parameters[e]:
            value = parameters[e].split('E')
            parameters[e] = float(float(value[0]))*(10**int(value[1]))
        # else:
        #     parameters[e] = float(parameters[e])
            element_list[e].area = parameters[e]
        e += 1
    return node_list, element_list


def bc_nodes(parameters, node_list, element_list):
    parameters = parameters[2::]
    for i in parameters:
        e = i.split()
        if(len(e) > 0):
            for node in node_list:
                if(node.id_number == int(e[0])):
                    if(int(e[1]) == 1):
                        node.restrictions[0] = 1
                    elif(int(e[1]) == 2):
                        node.restrictions[1] = 1
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


def element_groups(parameters, node_list, element_list):
    return node_list, element_list


def Reader(file_name):
    nodes = []
    elements = []
    key_words = {
        "COORDINATES": coordinates,
        "ELEMENT_GROUPS": element_groups,
        "INCIDENCES": incidences,
        "MATERIALS": materials,
        "GEOMETRIC_PROPERTIES": geom_properties,
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
                nodes, elements = key_words[counter](
                    parameters.split(','), nodes, elements)
                counter = ''
    return nodes, elements
