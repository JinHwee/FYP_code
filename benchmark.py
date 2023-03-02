import copy, random, math, time
from class_SimpleGraph import *
from class_SimpleNode import *

INF = math.inf
objectivesDictionary = {1.1: "CIFAR 10", 1.2: "CIFAR 100", 2.1:"NLP"} 
objective = list(objectivesDictionary.keys())

result = {}

def combine_adjM(adjM, newNode):
    for rowIndex in range(len(adjM)):
        adjM[rowIndex].append(newNode[rowIndex])
    adjM.append(newNode)
    return adjM

def automating_matrix_creation(number):
    values = [_ for _ in range(1, 101)]
    adjMatrix = [[] for _ in range(number)]
    newNode = [random.choice(values) for _ in range(number)]
    newNode.append(INF)
    for i in range(number):
        for j in range(i, number):
            if i == j:
                adjMatrix[i].append(INF)
            else:
                value = random.choice(values)
                adjMatrix[i].append(value)
                adjMatrix[j].append(value)
    
    return adjMatrix, newNode

def generate_node_dictionary(num):
    
    nodeDictionary = {}
    for id in range(num):
        nodeDictionary[id] = SimpleNode(id, None, random.choice(objective))

    return nodeDictionary

def addition_benchmark(num):
    adjM, adjNewNode = automating_matrix_creation(num)
    nodeDictionary = generate_node_dictionary(num)
    copy_adjM = copy.deepcopy(adjM)
    copy_adjNewNode = copy.deepcopy(adjNewNode)
    graphInstance = SimpleGraph(nodeDictionary, copy_adjM)

    nodeObjective = random.choice(objective)
    newNode = SimpleNode(len(nodeDictionary), None, nodeObjective)
    calculateAPSP = time.time()
    graphInstance.calculate_APSP_matrix_using_Floyd_Warshall_algorithm()
    endCalculateAPSP = time.time()
    addNode = time.time()
    graphInstance.add_new_node(newNode, copy_adjNewNode)
    endAddNode = time.time()

    copy_nodeDict = copy.deepcopy(nodeDictionary)
    updateM = combine_adjM(adjM, adjNewNode)
    graphChecker = SimpleGraph(copy_nodeDict, updateM)
    APSPFullGraph = time.time()
    graphChecker.calculate_APSP_matrix_using_Floyd_Warshall_algorithm()
    endAPSPFullGraph = time.time()
    test = graphChecker.get_APSP_Matrix()

    allKeys = list(copy_nodeDict.keys())
    deleteNode = time.time()
    graphChecker.delete_node(random.choice(allKeys))
    endDeleteNode = time.time()
    test = graphChecker.get_APSP_Matrix()

    result[num] =f'Floyd (n+1): {endAPSPFullGraph - APSPFullGraph}, Floyd (n): {endCalculateAPSP - calculateAPSP}, AddNode: {endAddNode - addNode }, DeleteNode: {endDeleteNode - deleteNode}\n'
    

if __name__ == "__main__":
    
    for num in range(10, 501, 10):
        addition_benchmark(num)
    
    for numNodes, string in result.items():
        print(f'{numNodes}:\n\t{string}\n')
