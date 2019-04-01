from node import *


def calc_dof(nodes):
    count = 0
    for i in nodes:
        i.degrees[0] = count
        count += 1
        i.degrees[1] = count
        count += 1


# def calc_dof(nodes):
#     buffer = []
#     count = 0
#     for i in nodes:
#         print(i.id_number)
#       # i.restriction[0] : restriçao do nó em x(tem se for 1)
#       # i.restriction[1] : restrição do nó em y(tem se for 2)
#         if(i.restrictions[0] == 1):
#             buffer.append([i, i.restrictions[0], 'x'])
#         else:
#             i.degrees[0] = count
#             count += 1
#         if (i.restrictions[1] == 1):
#             buffer.append([i, i.restrictions[1], 'y'])
#         else:
#             i.degrees[1] = count
#             count += 1
#     for e in buffer:
#         if(e[2] == 'x'):
#             e[0].degrees[0] = count
#             count += 1
#         if(e[2] == 'y'):
#             e[0].degrees[1] = count
#             count += 1
