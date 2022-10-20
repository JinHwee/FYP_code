import random
from classesDefinition import Graph, Node

def generate_graph():

    # generate vertices and store in nodeDictionary, in the format int(id): Node(i, data)
    nodeDictionary = {}
    for i in range(1, 8):
        tmp = Node(i, None)
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

    edgeDictionary = {}     # weights of each edges
    # to update node of its neighbours after initialization
    for id in nodeDictionary.keys():
        for neighbourID in neighbourDictionary[id]:
            # assume that the weight of the edge is 1
            # edgeDictionary[(id, neighbourID)] = 1
            # assume that the weight of src->dest =/= dest->src                  
            edgeDictionary[(id, neighbourID)] = random.randint(0, 100)
        nodeDictionary[id].update_neighbours(neighbourDictionary[id])
    
    # creating the first graph
    print("Testing the creation of the graph instance...")
    graphTest = Graph(nodeDictionary, neighbourDictionary, edgeDictionary)
    graphTest.print_information()

    # adding a sample vertex
    print("\nAdding an additional vertex...")
    graphTest.add_vertex(10, None, [1, 2])
    graphTest.print_information()

    print()
    for id, nodeInstance in nodeDictionary.items():
        nodeInstance.print_information()

    print()
    for IDpair, weight in Graph.edgeWeighsDictionary.items():
        print(IDpair, weight)

if __name__ == "__main__":
    generate_graph()