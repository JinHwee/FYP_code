import os, random, math
import tensorflow as tf
from class_SimpleNode import *
from class_SimpleGraph import *

nodeDictionary = {}             # dictionary for all node instances instantiated
objectivesDictionary = {1.1: "CIFAR 10", 1.2: "CIFAR 100", 2.1:"NLP"}       # what each float represents
INF = math.inf

adjM_complicatedGraph = [
        [INF, 82, 15, INF, INF, INF, INF],
        [82, INF, 4, INF, INF, INF, INF],
        [15, 4, INF, 95, INF, 36, 32],
        [INF, INF, 95, INF, 29, INF, INF],
        [INF, INF, INF, 29, INF, 18, INF],
        [INF, INF, 36, INF, 18, INF, 95],
        [INF, INF, 32, INF, INF, 95, INF],
    ]
# adjM_NewNode = [87, INF, INF, INF, INF, INF, INF, INF]
adjM_NewNode = [87, 95, 70, 12, 37, 12, 9, INF]

# loading data and allocating the data to a node
def read_cifar_data(filePath):
    # print(f"\nLoading from {filePath}")
    dataset = tf.data.experimental.load(filePath)
    # print(f"Size of dataset loaded: {len(dataset)}")
    return dataset

# setting up node objectives for each node in the graph
def setting_objective_of_node(manual_setting = False):
    objectives = list(objectivesDictionary.keys())
    # to generate a graph that is exactly the same as in report
    if manual_setting:
        # based on the graph in report, vertices 1, 3, 4 have the same objective (blue group)
        nodeDictionary[0].update_node_objective(objectives[0])
        nodeDictionary[2].update_node_objective(objectives[0])
        nodeDictionary[3].update_node_objective(objectives[0])

        # based on the graph in report, vertices 2, 5, 6, 7 have the same objective (red group)
        nodeDictionary[1].update_node_objective(objectives[2])
        nodeDictionary[4].update_node_objective(objectives[2])
        nodeDictionary[5].update_node_objective(objectives[2])
        nodeDictionary[6].update_node_objective(objectives[2])
    
    # to generate a graph with objectives randomly allocated to each vertices
    else:
        for id in nodeDictionary.keys():
            index = random.randint(0, 2)
            nodeDictionary[id].update_node_objective(objectives[index])

def generate_graph():
    # generate vertices and store in nodeDictionary, in the format int(id): Node(i, data)
    data_path = os.path.join(os.getcwd(), "all_data/saved_data_client_")
    for i in range(7):
        currentFile = data_path + str(i+1)
        dataDict = read_cifar_data(currentFile)
        nodeDictionary[i] = SimpleNode(i, dataDict, 0)      # nodeObjective initialized as 0
    
    setting_objective_of_node(True)             # update nodeObjective to specific values
    graphInstance = SimpleGraph(nodeDictionary)
    graphInstance.calculate_APSP_matrix_using_Floyd_Warshall_algorithm(adjM_complicatedGraph)

    apspM = graphInstance.get_APSP_Matrix()

    newNodeFilePath = os.path.join(os.getcwd(), "all_data/saved_data_client_10")
    newNodeData = read_cifar_data(newNodeFilePath)
    newNode = SimpleNode(len(nodeDictionary)+1, newNodeData, 2.1)

    graphInstance.add_new_node(newNode, adjM_NewNode)

    newApspM = graphInstance.get_APSP_Matrix()

    print("\nAPSP Matrix after adding new node:")
    for row in newApspM:
        print(row)

if __name__ == "__main__":
    random.seed(42)
    generate_graph()