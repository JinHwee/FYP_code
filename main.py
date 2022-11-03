import os
from classesDefinition import Graph, Node
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
    print("Testing the creation of the graph instance...")
    graphTest = Graph(nodeDictionary, neighbourDictionary)
    matrix = graphTest.get_adjacency_matrix(printOut=True)

    print()
    for id, nodeInstance in nodeDictionary.items():
        nodeInstance.print_information()
    
    print("\nPrinting all path shortest path (Brute Force Floyd Warshall)")
    all_pair_shortest_path(matrix)

    # adding a sample vertex
    client10DataPath = os.path.join(os.getcwd(), "all_data/saved_data_client_10")
    client10Dataset = read_cifar_data(client10DataPath)
    print("\nAdding an additional vertex...")
    graphTest.add_vertex(10, client10Dataset, [1, 2])
    matrix = graphTest.get_adjacency_matrix(printOut=True)

    print()
    for id, nodeInstance in nodeDictionary.items():
        nodeInstance.print_information()

    print("\nPrinting all path shortest path (Brute Force Floyd Warshall)")
    all_pair_shortest_path(matrix)

if __name__ == "__main__":
    generate_graph()