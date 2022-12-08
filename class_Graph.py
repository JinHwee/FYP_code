import math, random
from class_Node import Node

random.seed(42)

class Graph:
    # @params vertices: dictionary in the format int(id): Node(int(i), data)
    # @params adjacencyDictionary: adjacencyDictionary[id] is a dictionary that 
    #                              represents id of direct neighbours and len(adjacencyDictionary) <= n; 
    #                              where n = number of vertices in graph
    # self.edgesWeightDictionary is not available at this point of initialization; will be randomly generated
    def __init__(self, vertices, adjacencyDictionary):
        self.vertices = vertices 
        self.adjDictionary = adjacencyDictionary
        self.edgeWeightsDictionary = {}
        self.adjacencyMatrix = None     # placeholder variable
        self.__set_edges_weight()       # calling private function to initialize the weights of edges; populates edgeWeightsDictionary

    # @params newVertexID: Node object for vertex to be added to graph topology
    # @params data: data which the newVertex will have
    # @params listOfVertexNeighbours: list of neighbour ids newVertex is connected to
    # check if there is any nodes that had not been initialized in listOfVertexNeighbours
    def add_vertex(self, newVertexID, data, listOfVertexNeighbours):
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
        self.__set_weights_for_new_edges(newVertexID, listOfVertexNeighbours)   # calling private function; to randomly generate weights for new edges
        for id in listOfVertexNeighbours:
            self.vertices[id].update_neighbours(newVertexID)

    # check if edge exist using the source and destination node id
    def check_edge(self, srcID, destID):
        if (srcID, destID) in self.edgeWeightsDictionary.keys():
            return self.edgeWeightsDictionary[(srcID, destID)]
        elif (destID, srcID) in self.edgeWeightsDictionary.keys():
            return self.edgeWeightsDictionary[(destID, srcID)]
        return float(math.inf)
        
    # function to display information about the graph; in matrix format
    def print_graph_information(self):
        self.__update_adjacency_matrix()
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
    
    ######################################################################################################
    # functions below are private functions, they are not meant to be called externally from this script #
    ######################################################################################################

    # private function to randomly generate weights of edges
    def __set_edges_weight(self):
        for id, neighbourList in self.adjDictionary.items():
            self.vertices[id].update_neighbours(neighbourList)
            for neighbourID in neighbourList:
                if self.check_edge(id, neighbourID) == float(math.inf):
                    self.edgeWeightsDictionary[(id, neighbourID)] = random.randint(1,100)

    # private function to update weights; randomly generate weights for newly added vertex
    def __set_weights_for_new_edges(self, vertexID, listOfNeighbours):
        for id in listOfNeighbours: 
            self.edgeWeightsDictionary[(vertexID, id)] = random.randint(1, 100) 
    
    # private function to update adjacencyMatrix to latest information on graph
    def __update_adjacency_matrix(self):
        self.adjacencyMatrix = []
        for id in self.vertices.keys():
            tmp_list = []
            for neighbourID in self.vertices.keys():
                edgePresent = self.check_edge(id, neighbourID)
                tmp_list.append(edgePresent)
            self.adjacencyMatrix.append(tmp_list)

    #################################################
    # functions below are getter & setter functions #
    #################################################

    # obtain the adjacency matrix 
    def get_adjacency_matrix(self):
        self.__update_adjacency_matrix()
        return self.adjacencyMatrix