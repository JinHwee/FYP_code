import math, random

class Node:
    # @params id: unique vertex identification number
    # @params data: data that this particular vertex has (training data)
    # @params listOfDirectNeighbours: list containing ids of vertices it is directly connected to; 
    #                                 listOfDirectNeighbours is empty at start, and will be populated
    def __init__(self, id, data):
        self.id = id
        self.data = data 
        self.neighbours = []            # direct edge between 2 nodes; immediate neighbours
        self.initialized = False        # will be called when graph is initialized; for new nodes to be added
        self.IdleState = False          # IdleState refers to whether node is available for training
        self.NodeObjective = None       # NodeObjective refers to ML task identifier        
        self.DictionaryOfRelevantNodes = {}   # DictionaryOfRelevantNodes refers to list of nodes that have relevant objective(s) as self
        self.distanceToRelevantNodes = None     # adjacency matrix that combines both distance and relevant nodes 
        self.pathToRelevantNodes = {}

    # @params vertexID: unique identification of new vertex
    # @params initialized: whether the node has been init
    def update_neighbours(self, vertexID):
        if not self.initialized:
            self.neighbours.extend(vertexID)
            self.initialized = True
        else:
            # appends the newest neighbour into the list
            self.neighbours.append(vertexID)
    
    # to print out information on the node
    def print_node_information(self):
        print(f"\nNode {self.id} has \tObjective: {self.NodeObjective},\n\t\tAllocated data: {self.data},\n\t\tConnected to nodes: {self.neighbours}")
        output_RelevantNodes = {id:relevance for id, relevance in self.DictionaryOfRelevantNodes.items()}
        print(f'\t\tRelevant nodes: {output_RelevantNodes}')
        print('\t\tPath costs to each relevant nodes:')
        for path, pathCost in self.pathToRelevantNodes.items():
            print(f'\t\t\t{path}: {pathCost}')

    #################################################
    # functions below are getter & setter functions #
    #################################################

    # returns the current status/state of the node
    def get_IdleState(self):
        return self.IdleState
    
    # sets whether Node is Idle or not (T/F)
    def set_IdleState(self, state):
        self.IdleState = state

    # returns the data the node currently holds
    def get_data(self):
        return self.data

    # update and sets data that node currently holds
    def set_data(self, newData):
        self.data = newData

    # node.objective (1.1 = CIFAR 10, 1.2 = CIFAR 100, 2.1 = NLP)
    def get_objective(self):
        return self.NodeObjective

    def set_objective(self, objective):
        self.NodeObjective = objective

    # NodeObjectiveMatrix refers to nodes that has the same/relevant objectives as the current node
    def get_dict_of_relevant_nodes(self):
        return self.DictionaryOfRelevantNodes

    def set_dict_of_relevant_nodes(self, dict, update=False):
        if update:
            self.DictionaryOfRelevantNodes.update(dict)
        else:
            self.DictionaryOfRelevantNodes = dict

    def set_distance_to_relevant_node(self, distanceDict):
        self.distanceToRelevantNodes = distanceDict

    def get_distance_to_relevant_node(self):
        return self.distanceToRelevantNodes

    def set_paths_to_relevant_nodes(self, paths):
        self.pathToRelevantNodes.update(paths)
    
    def get_paths_to_relevant_nodes(self):
        return self.pathToRelevantNodes