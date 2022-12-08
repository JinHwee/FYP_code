import os, random
from class_Graph import Graph
from class_Node import Node
from floyd_warshall import all_pair_shortest_path
import tensorflow as tf

def read_cifar_data(filePath):
    print(f"\nLoading from {filePath}")
    dataset = tf.data.experimental.load(filePath)
    print(f"Size of dataset loaded: {len(dataset)}")
    return dataset

def generate_graph():

    # generate vertices and store in nodeDictionary, in the format int(id): Node(i, data)
    nodeDictionary = {}
    data_path = os.path.join(os.getcwd(), "all_data/saved_data_client_")
    for i in range(1, 8):
        currentFile = data_path + str(i)
        dataDict = read_cifar_data(currentFile)
        tmp = Node(i, dataDict)
        nodeDictionary[i] = tmp

    # generate adjacencyDictionary, in the format int(id): [int(id of neighbour), ...]
    neighbourDictionary = {}
    neighbourDictionary[nodeDictionary[1].id] = [nodeDictionary[2].id, nodeDictionary[3].id]
    neighbourDictionary[nodeDictionary[2].id] = [nodeDictionary[1].id, nodeDictionary[3].id]
    neighbourDictionary[nodeDictionary[3].id] = [nodeDictionary[1].id, nodeDictionary[2].id, nodeDictionary[4].id, nodeDictionary[6].id, nodeDictionary[7].id]
    neighbourDictionary[nodeDictionary[4].id] = [nodeDictionary[3].id, nodeDictionary[5].id]
    neighbourDictionary[nodeDictionary[5].id] = [nodeDictionary[4].id, nodeDictionary[6].id]
    neighbourDictionary[nodeDictionary[6].id] = [nodeDictionary[3].id, nodeDictionary[5].id, nodeDictionary[7].id]
    neighbourDictionary[nodeDictionary[7].id] = [nodeDictionary[3].id, nodeDictionary[6].id]
    
    # creating the first graph
    print("\nTesting the creation of the graph instance...")
    graphTest = Graph(nodeDictionary, neighbourDictionary)
    matrix = graphTest.get_adjacency_matrix()
    graphTest.print_graph_information()

    # setting up node objectives for each node in the graph
    objectives = [1.1, 1.2, 2.1]                                                # values allocateed to each node
    objectivesDictionary = {1.1: "CIFAR 10", 1.2: "CIFAR 100", 2.1:"NLP"}       # what each float represents
    for id, nodeInstance in nodeDictionary.items():
        index = random.randint(0, 2)
        nodeDictionary[id].set_objective(objectives[index])

    # testing for nodeObjectiveMatrix
    nodeObjectiveMatrix = {i:[] for i in nodeDictionary.keys()}
    allIDs = [id for id in nodeDictionary.keys()]
    for index1 in range(len(allIDs) - 1):
        for index2 in range(index1, len(allIDs)):
            id1, id2 = allIDs[index1], allIDs[index2]
            if nodeDictionary[id1].get_objective() == nodeDictionary[id2].get_objective():
                if id2 not in nodeObjectiveMatrix[id1]:
                    nodeObjectiveMatrix[id1].append(id2)
                if id1 not in nodeObjectiveMatrix[id2]:
                    nodeObjectiveMatrix[id2].append(id1)

    print()
    for id, objectiveMatrix in nodeObjectiveMatrix.items():
        nodeDictionary[id].set_node_objective_matrix(objectiveMatrix)

    print()
    for id, nodeInstance in nodeDictionary.items():
        nodeInstance.print_node_information()
    
    print("\nPrinting all pair shortest path (Brute Force Floyd Warshall)")
    all_pair_shortest_path(matrix)

    # adding a sample vertex
    client10DataPath = os.path.join(os.getcwd(), "all_data/saved_data_client_10")
    client10Dataset = read_cifar_data(client10DataPath)
    print("\nAdding an additional vertex...")
    graphTest.add_vertex(10, client10Dataset, [1, 2])
    matrix = graphTest.get_adjacency_matrix()
    graphTest.print_graph_information()

    print()
    for id, nodeInstance in nodeDictionary.items():
        nodeInstance.print_node_information()

    print("\nPrinting all pair shortest path (Brute Force Floyd Warshall)")
    all_pair_shortest_path(matrix)

if __name__ == "__main__":
    generate_graph()