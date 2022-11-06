import random, math

random.seed(42)     # setting a fixed seed for experiments

class Graph:
    def __init__(self, vertices, adjacencyDictionary):
        # @params vertices: dictionary in the format int(id): Node(int(i), data)
        # @params adjacencyDictionary: adjacencyDictionary[id] is a dictionary that 
        #                              represents id of direct neighbours and len(adjacencyDictionary) <= n; 
        #                              where n = number of vertices in graph
        # self.edgesWeightDictionary is not available at this point of initialization; will be randomly generated
        self.vertices = vertices 
        self.adjDictionary = adjacencyDictionary
        self.edgeWeighsDictionary = {}
        self.adjacencyMatrix = None
        self.__set_edges_weight()

    # private function to randomly generate weights of edges
    def __set_edges_weight(self):
        for id, neighbourList in self.adjDictionary.items():
            self.vertices[id].update_neighbours(neighbourList)
            for neighbourID in neighbourList:
                if self.check_edge(id, neighbourID) == float(math.inf):
                    self.edgeWeighsDictionary[(id, neighbourID)] = random.randint(1,100)
    
    # adding a new vertex into the graph
    def add_vertex(self, newVertexID, data, listOfVertexNeighbours):
        # @params newVertexID: Node object for vertex to be added to graph topology
        # @params data: data which the newVertex will have
        # @params listOfVertexNeighbours: list of neighbour ids newVertex is connected to

        # check if there is any nodes that had not been initialized in listOfVertexNeighbours
        setList = set(listOfVertexNeighbours)
        setID = set(self.vertices.keys())
        if len(setList - setID) != 0:
            try:
                raise ValueError("Uninitialized node detected!")
            except ValueError as e:
                print(e)

        self.vertices[newVertexID] = Node(newVertexID, data)
        self.adjDictionary[newVertexID] = listOfVertexNeighbours
        self.vertices[newVertexID].update_neighbours(listOfVertexNeighbours)
        self.__set_weights_for_new_edges(newVertexID, listOfVertexNeighbours)             # adds (newVertexID, neighbourID) to edgeWeighsDictionary
        for id in listOfVertexNeighbours:
            self.vertices[id].update_neighbours(newVertexID)

    # not supposed to be called externally (private update function)
    # randomly generate weights for newly added vertex
    def __set_weights_for_new_edges(self, vertexID, listOfNeighbours):
        for id in listOfNeighbours: 
            self.edgeWeighsDictionary[(vertexID, id)] = random.randint(1, 100) 
    
    # check if edge exist
    def check_edge(self, srcID, destID):
        if (srcID, destID) in self.edgeWeighsDictionary.keys():
            return self.edgeWeighsDictionary[(srcID, destID)]
        elif (destID, srcID) in self.edgeWeighsDictionary.keys():
            return self.edgeWeighsDictionary[(destID, srcID)]
        return float(math.inf)

    # obtain the adjacency matrix and print out information (if needed)
    def get_adjacency_matrix(self, printOut=False):
        self.adjacencyMatrix = []
        for id in self.vertices.keys():
            tmp_list = []
            for neighbourID in self.vertices.keys():
                edgePresent = self.check_edge(id, neighbourID)
                tmp_list.append(edgePresent)
            self.adjacencyMatrix.append(tmp_list)
        
        if printOut:
            print('\t', end='')
            for id in self.vertices.keys():
                print(id, end='\t')
            print()
            allIDs = [i for i in self.vertices.keys()]
            for i in range(len(self.adjacencyMatrix)):
                print(allIDs[i], end='\t')
                for weight in self.adjacencyMatrix[i]:
                    print(weight, end='\t')
                print()
        
        return self.adjacencyMatrix

class Node:
    def __init__(self, id, data):
        # @params id: unique vertex identification number
        # @params data: data that this particular vertex has (training data)
        # @params listOfDirectNeighbours: list containing ids of vertices it is directly connected to; 
        #                                 listOfDirectNeighbours is empty at start, and will be populated
        self.id = id
        self.data = data 
        self.neighbours = []            # direct edge between 2 nodes
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
            # appends the newest neighbour into the list
            self.neighbours.append(vertexID)

    # returns the current status/state of the node
    def get_IdleState(self):
        return self.IdleState
    
    # sets whether Node is Idle or not (T/F)
    def set_IdleState(self, state):
        self.IdleState = state
    
    # to-do node.set_data(file) (lowest priority)

    # to-do node.set_objective() / node.get_objective
    # on node.objective (1.1 = CIFAR 10, 1.2 = CIFAR 100, 2.1 = NLP)
    def set_objective(self, objective):
        self.NodeObjective = objective

    def get_objective(self):
        return self.NodeObjective

    # to-do node_specific_objective_matrix: stores all nodes with same objective
    # node.objective_adj_matrix: nodes that have objectives that are relevant to self 

    # to print out information on the node
    def print_information(self):
        print(f"Node {self.id} has data {self.data} and is connected to nodes {self.neighbours}")
