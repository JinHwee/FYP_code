import random, math

random.seed(42)     # setting a fixed seed for experiments

class Graph:
    # initialize one class variable for edgeWeighsDictionary, so that one can update the weights of edges from Node class
    # is there a better implementation of this? How to update weights of edges using Graph instance from Node instance?
    edgeWeighsDictionary = None

    def __init__(self, vertices, adjacencyDictionary, edgeWeightsDictionary):
        # @params vertices: dictionary in the format int(id): Node(int(i), data)
        # @params adjacencyDictionary: adjacencyDictionary[id] is a dictionary that 
        #                              represents id of direct neighbours and len(adjacencyDictionary) <= n; 
        #                              where n = number of vertices in graph
        self.vertices = vertices 
        self.adjDictionary = adjacencyDictionary
        Graph.edgeWeighsDictionary = edgeWeightsDictionary
    
    def add_vertex(self, newVertexID, data, listOfVertexNeighbours):
        # @params newVertexID: Node object for vertex to be added to graph topology
        # @params data: data which the newVertex will have
        # @params listOfVertexNeighbours: list of neighbour ids newVertex is connected to
        self.vertices[newVertexID] = Node(newVertexID, data)
        self.adjDictionary[newVertexID] = listOfVertexNeighbours
        self.vertices[newVertexID].update_neighbours(listOfVertexNeighbours)
        self.__update_edges_weight(newVertexID, listOfVertexNeighbours)             # adds (newVertexID, neighbourID) to edgeWeighsDictionary
        for id in listOfVertexNeighbours:
            self.vertices[id].update_neighbours(newVertexID)

    # not supposed to be called externally (private update function)
    def __update_edges_weight(self, vertexID, listOfNeighbours):
        for id in listOfNeighbours:
            # assumes that the weight of the edges are 1s
            # self.edgeWeighsDictionary[(vertexID, id)] = 1
            # assume that the weight of src->dest =/= dest->src   
            self.edgeWeighsDictionary[(vertexID, id)] = random.randint(50, 100) 
    
    # check if edge exist; assuming that it might not be a bidirectional edge
    def check_edge(cls, srcID, destID):
        if (srcID, destID) in cls.edgeWeighsDictionary.keys():
            return cls.edgeWeighsDictionary[(srcID, destID)]
        elif (destID, srcID) in cls.edgeWeighsDictionary.keys():
            return cls.edgeWeighsDictionary[(destID, srcID)]
        return float(math.inf)

    # to print out adjacency matrix of graph
    def print_information(self):
        print('\t', end='')
        for id in self.vertices.keys():
            print(id, end='\t')
        print()
        for id in self.vertices.keys():
            print(id, end='\t')
            for neighbourID in self.vertices.keys():
                results = self.check_edge(id, neighbourID)
                print(results, end="\t") if math.isinf(results) == False else print("inf", end='\t')
            print()

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
            self.initialized = True         # if just initialized, assumes edgeWeighsDictionary had been populated prior to calling this function
        else:
            # adds (currentID, newVertexID) to edgeWeighsDictionary
            # assumes that the weight of the edge is 1, update the class variable directly
            # Graph.edgeWeighsDictionary[(self.id, vertexID)] = 1    
            # assume that the weight of src->dest =/= dest->src   
            Graph.edgeWeighsDictionary[(self.id, vertexID)] = random.randint(1, 100) 
            self.neighbours.append(vertexID)
    
    # to print out information on the node
    def print_information(self):
        print(f"Node {self.id} has data {self.data} and is connected to nodes {self.neighbours}")
