import os, random
from class_Graph import Graph
from class_Node import Node
import tensorflow as tf

###############################
# global variable declaration #
###############################
nodeDictionary = {}
neighbourDictionary = {}
objectives = [1.1, 1.2, 2.1]                                                # values allocateed to each node
objectivesDictionary = {1.1: "CIFAR 10", 1.2: "CIFAR 100", 2.1:"NLP"}       # what each float represents
nodeObjectiveMatrix = None

#########################
# functions declaration #
#########################

def read_cifar_data(filePath):
    print(f"\nLoading from {filePath}")
    dataset = tf.data.experimental.load(filePath)
    print(f"Size of dataset loaded: {len(dataset)}")
    return dataset

def generate_graph():
    # generate vertices and store in nodeDictionary, in the format int(id): Node(i, data)
    data_path = os.path.join(os.getcwd(), "all_data/saved_data_client_")
    for i in range(1, 8):
        currentFile = data_path + str(i)
        dataDict = read_cifar_data(currentFile)
        nodeDictionary[i] = Node(i, dataDict)

    # generate adjacencyDictionary, in the format int(id): [int(id of neighbour), ...]
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
    graphTest.print_graph_information()

    # setting up node objectives for each node in the graph
    for id, nodeInstance in nodeDictionary.items():
        index = random.randint(0, 2)
        nodeDictionary[id].set_objective(objectives[index])
    graphTest.groupings_w_similar_objective()

    print()
    for id, nodeInstance in nodeDictionary.items():
        nodeInstance.print_node_information()
    
    apsp_matrix = graphTest.all_pair_shortest_path()
    print("\nPrinting all pair shortest path (Brute Force Floyd Warshall)")
    for cost in apsp_matrix:
        print(cost)

    # adding a sample vertex
    client10DataPath = os.path.join(os.getcwd(), "all_data/saved_data_client_10")
    client10Dataset = read_cifar_data(client10DataPath)
    print("\nAdding an additional vertex...")
    graphTest.add_vertex(10, client10Dataset, [1, 2], objectives[random.randint(0,2)])
    graphTest.print_graph_information()
    graphTest.groupings_w_similar_objective()

    print()
    for id, nodeInstance in nodeDictionary.items():
        nodeInstance.print_node_information()

    apsp_matrix = graphTest.all_pair_shortest_path()
    print("\nPrinting all pair shortest path (Brute Force Floyd Warshall)")
    for cost in apsp_matrix:
        print(cost)

    # from apsp_matrix, create distanceToRelevantNodes in each instantiated node
    print()
    nodeIDs = list(nodeDictionary.keys())
    for rowIndex in range(len(apsp_matrix)):
        tmp_dict = {}
        currNodeRelevantList = nodeDictionary[nodeIDs[rowIndex]].get_node_objective_matrix()
        for id in currNodeRelevantList:
            tmp_dict[id] = apsp_matrix[rowIndex][nodeIDs.index(id)]
        nodeDictionary[nodeIDs[rowIndex]].set_distance_to_relevant_nodes(tmp_dict)
    
    for key, node in nodeDictionary.items():
        print(f"Node {key}:", end=" ")
        print(node.get_distance_to_relevant_nodes())

if __name__ == "__main__":
    generate_graph()