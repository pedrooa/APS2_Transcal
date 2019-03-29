from node import *


def calc_dof(nodes):
    buffer = []
    count = 1
    for i in nodes:
      # i.restriction[0] : restriçao do nó em x(tem se for 1)
      # i.restriction[1] : restrição do nó em y(tem se for 2)
        if(i.restrictions[0] == 1):
            buffer.append([i, i.restrictions[0]])
        else:
            i.degrees[0] = count
            count += 1
        if (i.restrictions[1] == 2):
            buffer.append([i, i.restrictions[1]])
        else:
            i.degrees[1] = count
            count += 1
    for e in buffer:
        if(e[1] == 1):
            e[0].degrees[0] = count
            count += 1
        if(e[1] == 2):
            e[0].degrees[1] = count
            count += 1
