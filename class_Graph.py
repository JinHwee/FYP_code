import math, random, copy
from class_Node import Node

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
    def add_vertex(self, newVertexID, data, listOfVertexNeighbours, objective):
        setList = set(listOfVertexNeighbours)
        setID = set(self.vertices.keys())
        if len(setList - setID) != 0:
            try:
                raise ValueError("Uninitialized node detected!")
            except ValueError as e:
                print(e)

        self.vertices[newVertexID] = Node(newVertexID, data)
        self.vertices[newVertexID].set_objective(objective)
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

    # updates node class's DictionaryOfRelevantNodes variable; to populate it with ids of relevant nodes
    def groupings_w_similar_objective(self, update):
        # id: [ list of nodes with similar objectives]
        nodeGroupings = {i:{} for i in self.vertices.keys()}
        for index1 in self.vertices.keys():
            allIDs = [id for id in self.vertices.keys()]
            for index1 in range(len(allIDs) - 1):
                for index2 in range(index1, len(allIDs)):
                    id1, id2 = allIDs[index1], allIDs[index2]
                    # update the list with nodes other than self, if nodes have the same objective as self
                    # all these ids will be having the value True because the objective is similar
                    if self.vertices[id1].get_objective() == self.vertices[id2].get_objective() and id1 !=id2:
                        if id2 not in nodeGroupings[id1]:
                            nodeGroupings[id1].update({id2:True})
                        if id1 not in nodeGroupings[id2]:
                            nodeGroupings[id2].update({id1:True})

        print("\nSet of nodes with similar objectives to current node\n")
        for id, objectiveDict in nodeGroupings.items():
            print(f"\tNode {id}", end=': ')
            # updating node <id> with nodes that have the same objective
            self.vertices[id].set_dict_of_relevant_nodes(objectiveDict, update)
            # testing to verify that node_objective_matrix is updated successfully
            print(self.vertices[id].get_dict_of_relevant_nodes())
        
    # returns path cost for each pair of nodes
    def all_pair_shortest_path(self):
        # pathCostMatrix [
        #    1   2   ...     n
        # 1 [inf, x, ...     y]
        # 2 [x, inf, ...     z]
        # ]
        # pathCostMatrix[i][j] = pathCostMatrix[row][column]
        matrix = self.get_adjacency_matrix()
        previousPathCost = copy.deepcopy(matrix)          # initilisation of matrix
        newPathCost = []

        paths = {}
        counter = 0
        for currentNode in range(len(matrix)):
            for i in range(len(matrix)):
                tmp_matrix = []
                for j in range(len(matrix)):
                    if i == j:
                        tmp_matrix.append(0)
                    else:
                        presentEdge = previousPathCost[i][j]
                        newCost = previousPathCost[i][currentNode] + previousPathCost[currentNode][j]
                        if counter < len(matrix) ** 2 and presentEdge < math.inf:
                            # stores the direct edges between 2 distinct vertices
                            paths[(i+1, j+1)] = presentEdge
                        counter += 1
                        # key[0] is the source node, key[-1] is the last added node
                        if newCost < math.inf and newCost < presentEdge:
                            allDetectedPaths = [key for key in paths.keys() if key[0] == i+1 and key[-1] == currentNode+1]
                            additionalPaths = [key for key in paths.keys() if key[0] == currentNode+1]
                            for basePath in allDetectedPaths:
                                for pathToBeMerged in additionalPaths:
                                    setBasePath = set(basePath)
                                    setPathToBeMerged = set(pathToBeMerged)
                                    # ensures that only the destination from first set is the common vertex between the 2 sets
                                    if len(setBasePath.intersection(setPathToBeMerged)) == 1:
                                        listBasePath = list(basePath)
                                        listPathToBeMerged = list(pathToBeMerged)
                                        listBasePath.extend(listPathToBeMerged[1:])
                                        if tuple(listBasePath) not in paths.keys():
                                            paths[tuple(listBasePath)] = paths.get(tuple(basePath)) + paths.get(tuple(pathToBeMerged))
                        tmp_matrix.append(min(presentEdge, newCost))
                newPathCost.append(tmp_matrix)
            previousPathCost = newPathCost
            newPathCost = []
            
        return previousPathCost, paths

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