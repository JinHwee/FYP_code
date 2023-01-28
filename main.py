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

#########################
# functions declaration #
#########################

# loading data and allocating the data to a node
def read_cifar_data(filePath):
    # print(f"\nLoading from {filePath}")
    dataset = tf.data.experimental.load(filePath)
    # print(f"Size of dataset loaded: {len(dataset)}")
    return dataset

# setting up node objectives for each node in the graph
def setting_objective_of_node(manual_setting = False):
    # to generate a graph that is exactly the same as in report
    if manual_setting:
        # based on the graph in report, vertices 1, 3, 4 have the same objective (blue group)
        nodeDictionary[1].set_objective(objectives[0])
        nodeDictionary[3].set_objective(objectives[0])
        nodeDictionary[4].set_objective(objectives[0])

        # based on the graph in report, vertices 2, 5, 6, 7 have the same objective (red group)
        nodeDictionary[2].set_objective(objectives[2])
        nodeDictionary[5].set_objective(objectives[2])
        nodeDictionary[6].set_objective(objectives[2])
        nodeDictionary[7].set_objective(objectives[2])
    
    # to generate a graph with objectives randomly allocated to each vertices
    else:
        for id in nodeDictionary.keys():
            index = random.randint(0, 2)
            nodeDictionary[id].set_objective(objectives[index])

# check and update list of relevant nodes for each vertex from path information
def update_list_of_relevant_nodes(pathInfo):
    # because each vertex has already been updated with relevant IDs of vertices that have the same objectives
    # the path can be retrieved by using the current node as the source and each IDs in the list as the destination
    # if path contains additional vertices required for the path to be completed, then add the missing vertices into the list of relevant nodes
    for id in nodeDictionary.keys():
        relevantNodes = nodeDictionary[id].get_dict_of_relevant_nodes()
        for relevantID in list(relevantNodes.keys()):
            # print(f'Current node {id} Relevant node {relevantID}', end=' ')
            relevantPaths = {path:pathCost for path, pathCost in pathInfo.items() if path[0] == id and path[-1] == relevantID}
            shortestRelevantPaths = {path:pathCost for path, pathCost in relevantPaths.items() if pathCost == min(relevantPaths.values())}
            for path in shortestRelevantPaths.keys():
                # each node that is missing will be tagged as transmission only nodes, False because these nodes do not have the same objectives
                path = {node:False for node in list(path) if node != id and node not in relevantNodes.keys()}
                nodeDictionary[id].DictionaryOfRelevantNodes.update(path)

def update_node_with_paths(pathInfo):
    for id in nodeDictionary.keys():
        relevantNodes = nodeDictionary[id].get_dict_of_relevant_nodes()
        for relevantID in list(relevantNodes.keys()):
            relevantPaths = {path:pathCost for path, pathCost in pathInfo.items() if path[0] == id and path[-1] == relevantID}
            shortestRelevantPaths = {path:pathCost for path, pathCost in relevantPaths.items() if pathCost == min(relevantPaths.values())}
            nodeDictionary[id].set_paths_to_relevant_nodes(shortestRelevantPaths)

def combine_into_adjacency(apsp_matrix):
    updated_matrix = []
    for nodeID in range(len(apsp_matrix)):
        # relevant nodes are those nodes which are either on the shortest path or have similar objectives
        nodeInformation = nodeDictionary[nodeID+1].get_dict_of_relevant_nodes()
        # some of the nodes that does not have similar objective and did not appear on the shortest path will be missing from the list, excluding itself
        missingInformation = {id:False for id in nodeDictionary.keys() if id not in nodeInformation.keys() and id != nodeID+1}
        # combine nodeInformation and missingInformation to get all information
        nodeInformation.update(missingInformation)
        newAPSPInformation = []
        for nestNodeID in range(len(apsp_matrix)):
            newAPSPInformation.append((apsp_matrix[nodeID][nestNodeID], nodeInformation.get(nestNodeID+1, 'Self')))
        updated_matrix.append(newAPSPInformation)
    return updated_matrix

def update_graph_information(graphInstance, update):
    # updates each node with IDs of nodes that have the same objective as itself
    graphInstance.groupings_w_similar_objective(update)
    
    # apsp_matrix: shortest distance to each vertices in matrix format & all_paths: paths for each distance
    apsp_matrix, all_paths = graphInstance.all_pair_shortest_path()
    # print("\nPrinting all pair shortest path (Brute Force Floyd Warshall):")
    # for row in apsp_matrix:
    #     print(row)

    # check for disjointed sets and the need for transmission only nodes, using paths retrieved from previous step
    update_list_of_relevant_nodes(all_paths)
    update_node_with_paths(all_paths)

    # # node information must be retrieved after update to the nodes has been completed
    # for _, nodeInstance in nodeDictionary.items():
    #     nodeInstance.print_node_information()

    ########################################################################################################
    print("\nUpdated Adjacency Matrix for the graph created:")      # print statements for clarity of output
    print('\t', end='')                                             # print statements for clarity of output
    for _ in range(len(apsp_matrix)):                               # print statements for clarity of output
        print(_+1, end='\t\t')                                      # print statements for clarity of output
    print()                                                         # print statements for clarity of output
    ########################################################################################################

    # retrieve updated adjacency matrix
    updated_matrix = combine_into_adjacency(apsp_matrix)
    # printing out the entire graph in updated adjacency matrix
    for rowID in range(len(updated_matrix)):
        print(rowID+1, end='\t')
        for colID in range(len(updated_matrix)):
            print(updated_matrix[rowID][colID], end="\t")
        print()

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

    # manual_setting = False -> generate a graph with nodes randomly allocated an objective
    setting_objective_of_node(manual_setting=True)
    update_graph_information(graphTest, update=False)

    # adding a sample vertex
    client8DataPath = os.path.join(os.getcwd(), "all_data/saved_data_client_10")
    client8Dataset = read_cifar_data(client8DataPath)
    print("\nAdding an additional vertex...")
    graphTest.add_vertex(8, client8Dataset, [1, 2], objectives[random.randint(0,2)])
    graphTest.print_graph_information()

    update_graph_information(graphTest, update=True)

if __name__ == "__main__":
    random.seed(42)
    generate_graph()