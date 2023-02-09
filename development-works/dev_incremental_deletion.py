from class_SimpleGraph import *
from class_SimpleNode import *
import math, copy, re

INF = math.inf

simple_graph = [
    [INF, 13, 40, INF],
    [13, INF, 16, 9],
    [40, 16, INF, 5],
    [INF, 9, 16, INF]
]

nodeAdded = [INF, INF, 7, 3, INF]

node_deleted = [
    [INF, 13, 40, INF],
    [13, INF, 16, INF],
    [40, 16, INF, 7],
    [INF, INF, 7, INF]
]

# simple_graph = [
#     [INF, 11, 21, 18, 18, 20], 
#     [11, INF, 33, 41, 36, 17], 
#     [21, 33, INF, 15, 24, 42], 
#     [18, 41, 15, INF, 23, 36], 
#     [18, 36, 24, 23, INF, 36], 
#     [20, 17, 42, 36, 36, INF], 
# ]

# node_deleted = [
#     [INF, 11, 21, 18, 20], 
#     [11, INF, 33, 36, 17], 
#     [21, 33, INF, 24, 42], 
#     [18, 36, 24, INF, 36], 
#     [20, 17, 42, 36, INF], 
# ]

nodeDictionary = {}
nodeDictionary[0] = SimpleNode(0, None, 1)
nodeDictionary[1] = SimpleNode(1, None, 2)
nodeDictionary[2] = SimpleNode(2, None, 2)
nodeDictionary[3] = SimpleNode(3, None, 1)
# nodeDictionary[4] = SimpleNode(4, None, 2)
# nodeDictionary[5] = SimpleNode(5, None, 1)

modifiedDict = {}
modifiedDict[0] = SimpleNode(0, None, 1)
modifiedDict[1] = SimpleNode(1, None, 2)
modifiedDict[2] = SimpleNode(2, None, 2)
modifiedDict[3] = SimpleNode(4, None, 1)
# modifiedDict[4] = SimpleNode(5, None, 1)


copy_adjM = copy.deepcopy(simple_graph)
graphInstance = SimpleGraph(nodeDictionary, copy_adjM)
graphInstance.calculate_APSP_matrix_using_Floyd_Warshall_algorithm()
newNode = SimpleNode(len(nodeDictionary), None, 2)
graphInstance.add_new_node(newNode, nodeAdded)
tmp = graphInstance.get_APSP_Matrix()
graphInstance.delete_node(3)
apspM = graphInstance.get_APSP_Matrix()

copy_adjM = copy.deepcopy(node_deleted)
deletedNodeGraph = SimpleGraph(modifiedDict, copy_adjM)
deletedNodeGraph.calculate_APSP_matrix_using_Floyd_Warshall_algorithm()
newAPSPM = deletedNodeGraph.get_APSP_Matrix()

for row in apspM:
    print(row)

print()
for row in newAPSPM:
    print(row)

print()
for rid in range(len(apspM)):
    for cid in range(len(apspM)):
        cellValue = apspM[rid][cid]
        errorString = False
        for string in cellValue[2]:
            if re.search('[0-9]+ -> 3|3 -> [0-9]+', string):
                errorString = True
                break
        print('x', end=' ') if errorString else print('-', end=' ')
    print() if rid != 3 else print(end='')