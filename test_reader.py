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

    nodes = []
    elements = []

    key_words = {
        "COORDINATES": "COORDENADAS",
        "ELEMENT_GROUPS": "Elementos",
        "INCIDENCES": "Incidencias",
        "MATERIALS": materials,
        "GEOMETRIC_PROPERTIES": "propriedades geometricas",
        "BCNODES": "bc nodes",
        "LOADS": "loads"
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
                if(counter == "MATERIALS"):
                    nodes, elements = key_words[counter](
                        parameters.split(','), nodes, elements)
                counter = ''
        return nodes, elements


Reader(input("Qual arquivo deseja abrir?"))
