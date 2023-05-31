import copy, random, math
from class_SimpleGraph import *
from class_SimpleNode import *

INF = math.inf

def generate_matrix(number):
    values = [INF] + [_ for _ in range(number)]
    newNodeAdjM = [random.choice(values) for _ in range(number)] + [INF]
    
    adjM = []
    for rowID in range(number):
        tmp = []
        for colID in range(number):
            if rowID == colID:
                tmp.append(INF)
            else:
                tmp.append(random.choice(values))
        adjM.append(tmp)
    
    return adjM, newNodeAdjM


def common_code_block():    
    nodeDictionary = {}
    objectivesDictionary = {1.1: "CIFAR 10", 1.2: "CIFAR 100", 2.1:"NLP"}
    objectives = list(objectivesDictionary.keys())

    adjM, newNodeAdjM = generate_matrix(50)
    copy_adjM = copy.deepcopy(adjM)
    copy_newNodeAdjM = copy.deepcopy(newNodeAdjM)
    for id in range(len(adjM)):
        nodeDictionary[id] = SimpleNode(id, None, random.choice(objectives))
    nodeObj = random.choice(objectives)
    newNode = SimpleNode(len(nodeDictionary), None, nodeObj)
    graphInstance = SimpleGraph(nodeDictionary, copy_adjM)
    graphInstance.calculate_APSP_matrix_using_Floyd_Warshall_algorithm()
    # graphInstance.add_new_node(newNode, copy_newNodeAdjM)

    modified_nodeDictionary = copy.deepcopy(nodeDictionary)
    # added = SimpleNode(len(nodeDictionary), None, nodeObj)
    # modified_nodeDictionary[len(modified_nodeDictionary)] = added
    allKeys = [_ for _ in range(len(modified_nodeDictionary))]
    idToRemove = random.choice(allKeys)
    graphInstance.delete_node(idToRemove)
    apspM = graphInstance.get_APSP_Matrix()

    id = 0
    tmpDict = {}
    while id < len(modified_nodeDictionary)-1:
        if modified_nodeDictionary[allKeys[id]].get_node_id() == idToRemove:
            allKeys.pop(id)
        else:
            tmpDict[id] = modified_nodeDictionary[allKeys[id]]
            id += 1
    modified_nodeDictionary = tmpDict
    del tmpDict

    copy_adjM = copy.deepcopy(adjM)
    copy_newNodeAdjM = copy.deepcopy(newNodeAdjM)
    for rowID in range(len(copy_adjM)):
        copy_adjM[rowID].append(copy_newNodeAdjM[rowID])
        del copy_adjM[rowID][idToRemove]
    del copy_newNodeAdjM[idToRemove]
    # copy_adjM.append(copy_newNodeAdjM)
    del copy_adjM[idToRemove]

    graphChecker = SimpleGraph(modified_nodeDictionary, copy_adjM)
    graphChecker.calculate_APSP_matrix_using_Floyd_Warshall_algorithm()
    checkerAdjM = graphChecker.get_APSP_Matrix()

    for rowID in range(len(apspM)):
        for colID in range(len(apspM)):
            if apspM[rowID][colID] != checkerAdjM[rowID][colID]:
                print(apspM[rowID][colID], checkerAdjM[rowID][colID])

if __name__ == "__main__":
    common_code_block()