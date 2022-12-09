import math, random

random.seed(42)

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
        self.NodeObjectiveMatrix = None # NodeObjectiveMatrix refers to list of nodes that have relevant objective(s) as self

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
        print(f"Node {self.id} has objective {self.NodeObjective}, data {self.data} and is connected to nodes {self.neighbours}")
        print(f'Relevant nodes with similar objectives: {self.NodeObjectiveMatrix}')

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
    def get_node_objective_matrix(self):
        return self.NodeObjectiveMatrix

    def set_node_objective_matrix(self, matrix):
        self.NodeObjectiveMatrix = matrix
