import random
from class_Graph import Graph
from class_Node import Node
from floyd_warshall import all_pair_shortest_path, floyd_warshall_checker
import tracemalloc

### Global variables ###
nodeDictionary = {}
neighbourDictionary = {}
objectives = [1.1, 1.2, 2.1] 
########################

def test_retrieve_path():
    for i in range(1, 8):
        nodeDictionary[i] = Node(i, None)

    # generate adjacencyDictionary, in the format int(id): [int(id of neighbour), ...]
    neighbourDictionary[nodeDictionary[1].id] = [nodeDictionary[2].id, nodeDictionary[3].id]
    neighbourDictionary[nodeDictionary[2].id] = [nodeDictionary[1].id, nodeDictionary[3].id]
    neighbourDictionary[nodeDictionary[3].id] = [nodeDictionary[1].id, nodeDictionary[2].id, nodeDictionary[4].id, nodeDictionary[6].id, nodeDictionary[7].id]
    neighbourDictionary[nodeDictionary[4].id] = [nodeDictionary[3].id, nodeDictionary[5].id]
    neighbourDictionary[nodeDictionary[5].id] = [nodeDictionary[4].id, nodeDictionary[6].id]
    neighbourDictionary[nodeDictionary[6].id] = [nodeDictionary[3].id, nodeDictionary[5].id, nodeDictionary[7].id]
    neighbourDictionary[nodeDictionary[7].id] = [nodeDictionary[3].id, nodeDictionary[6].id]

    for id, nodeInstance in nodeDictionary.items():
        index = random.randint(0, 2)
        nodeDictionary[id].set_objective(objectives[index])

    print("Adjacency matrix of graph instantiated:")
    pathRetrievalGraph = Graph(nodeDictionary, neighbourDictionary)
    # pathRetrievalGraph.print_graph_information()
    pathRetrievalGraph.groupings_w_similar_objective()

    adjacencyMatrix = pathRetrievalGraph.get_adjacency_matrix()
    print("\nAll pair shortest pair matrix:")
    tracemalloc.start()
    apsp_matrix, pathDict = all_pair_shortest_path(adjacencyMatrix)
    print(tracemalloc.get_traced_memory())
    tracemalloc.stop()
    for cost in apsp_matrix:
        print(cost)

    print('\nPrinting the paths:')
    for i in range(1, len(adjacencyMatrix)+1):
        print(f'\nPaths for Node {i}:')
        listRelevantKeys = [key for key in pathDict.keys() if key[0] == i]
        for key in listRelevantKeys:
            print('\t', key, pathDict[key])

    floyd_warshall_checker(adjacencyMatrix)

if __name__ == "__main__":
    random.seed(42)
    test_retrieve_path()