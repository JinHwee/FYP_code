import random

class Graph:
    def __init__(self, vertices, adjacencyDictionary):
        # @params vertices: dictionary in the format int(id): Node(int(i), data)
        # @params adjacencyDictionary: adjacencyDictionary[id] is a dictionary that 
        #                              represents id of direct neighbours and len(adjacencyDictionary) <= n; 
        #                              where n = number of vertices in graph
        self.seed = random.seed(42)     # setting a fixed seed for experiments
        self.vertices = vertices 
        self.adjDictionary = adjacencyDictionary
    
    def add_vertex(self, newVertexID, data, listOfVertexNeighbours):
        # @params newVertexID: Node object for vertex to be added to graph topology
        # @params data: data which the newVertex will have
        # @params listOfVertexNeighbours: list of neighbour ids newVertex is connected to
        self.vertices[newVertexID] = Node(newVertexID, data)
        self.adjDictionary[newVertexID] = listOfVertexNeighbours
        self.vertices[newVertexID].update_neighbours(listOfVertexNeighbours)
        for id in listOfVertexNeighbours:
            self.vertices[id].update_neighbours(newVertexID)

    # to print out information on the graph
    def print_information(self):
        print(f"All vertices currently present in graph network: {list(self.vertices.keys())}")
        for id, _ in self.vertices.items():
            self.vertices[id].print_information()

class Node:
    def __init__(self, id, data):
        # @params id: unique vertex identification number
        # @params data: data that this particular vertex has (training data)
        # @params listOfDirectNeighbours: list containing ids of vertices it is directly connected to; 
        #                                 listOfDirectNeighbours is empty at start, and will be populated
        self.id = id
        self.data = data 
        self.neighbours = []
        self.initialized = False
        self.IdleState = False          # IdleState refers to whether node is available for training
        self.NodeObjective = None       # NodeObjective refers to ML task identifier

    def update_neighbours(self, vertexID):
        # @params vertexID: unique identification of new vertex
        # @params initialized: whether the node has been init
        if not self.initialized:
            self.neighbours.extend(vertexID)
            self.initialized = True
        else:
            self.neighbours.append(vertexID)
    
    # to print out information on the node
    def print_information(self):
        print(f"Node {self.id} has data {self.data} and is connected to nodes {self.neighbours}")
