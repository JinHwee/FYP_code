import unittest
from dev_incremental_approach import *
from class_SimpleGraph import *
from class_SimpleNode import *
import math, copy, random

INF = math.inf

class  TestIncrementalAPSP(unittest.TestCase):

    adjM = [
        [INF, 13, 40, INF],
        [13, INF, 16, INF],
        [40, 16, INF, 5],
        [INF, INF, 5, INF]
    ]

    adjNewNode_One = [INF, 2, INF, INF, INF]        # new node with one edge added, connected to Node 2
    adjNewNode_Two = [INF, 2, INF, 3, INF]               # new node with two edge added, connected to Node 2 and 4
    adjNewNode_Three = [INF, 2, 5, 3, INF]                    # new node with three edge added, connected to 2, 3 and 4

    complicatedGraph = [
        [INF, 82, 15, INF, INF, INF, INF],
        [82, INF, 4, INF, INF, INF, INF],
        [15, 4, INF, 95, INF, 36, 32],
        [INF, INF, 95, INF, 29, INF, INF],
        [INF, INF, INF, 29, INF, 18, INF],
        [INF, INF, 36, INF, 18, INF, 95],
        [INF, INF, 32, INF, INF, 95, INF],
    ]

    complicatedNewNode_One = [87, INF, INF, INF, INF, INF, INF, INF]
    complicatedNewNode_Four = [87, 95, 70, 12, INF, INF, INF, INF]
    complicatedNewNode_Seven = [87, 95, 70, 12, 37, 71, 9, INF]

    def select_added_node(self, newNodeToBeAdded):
        if type(newNodeToBeAdded) == str:
            adjM = copy.deepcopy(self.complicatedGraph)
        else:
            adjM = copy.deepcopy(self.adjM)                      # ensure that each test starts with the same base adjacency matrix

        if newNodeToBeAdded == 1:
            node = copy.deepcopy(self.adjNewNode_One)            # ensure that each test starts with the same new node list
        elif newNodeToBeAdded == 2:
            node = copy.deepcopy(self.adjNewNode_Two)
        elif newNodeToBeAdded == 3:
            node = copy.deepcopy(self.adjNewNode_Three)
        elif newNodeToBeAdded == "C1":
            node = copy.deepcopy(self.complicatedNewNode_One)
        elif newNodeToBeAdded == "C4":
            node = copy.deepcopy(self.complicatedNewNode_Four)
        elif newNodeToBeAdded == "C7":
            node = copy.deepcopy(self.complicatedNewNode_Seven)

        return adjM, node

    def instantiation_of_variables(self, id):
        copyAdjM, copyNewNode = self.select_added_node(id)
        apspMatrix = floyd_warshall(copyAdjM)                        # obtains the partial APSP matrix, without new node added
        updateAdjM = add_new_node(apspMatrix, copyNewNode)           # obtains the full APSP matrix, with new node added

        copyAdjM, copyNewNode = self.select_added_node(id)
        combinedAdjM = combine_adjM(copyAdjM, copyNewNode)           # generates one combined adjacency matrix for the entire graph
        checkerAdjM = floyd_warshall(combinedAdjM)

        return updateAdjM, checkerAdjM

    def automating_matrix_creation(self, number):
        adjMatrix = [[] for _ in range(number)]
        newNode = [random.randint(1,100) for _ in range(number)]
        newNode.append(INF)
        for i in range(number):
            for j in range(i, number):
                if i == j:
                    adjMatrix[i].append(INF)
                else:
                    value = random.randint(1, 100)
                    adjMatrix[i].append(value)
                    adjMatrix[j].append(value)
        
        return adjMatrix, newNode

    def test_adding_node_with_edge(self):
        updatedMatrix, checkerAdjM = self.instantiation_of_variables(1)
        for rowId in range(len(checkerAdjM)):
            for colId in range(len(checkerAdjM[rowId])):
                self.assertEqual(updatedMatrix[rowId][colId], checkerAdjM[rowId][colId])
    
    def test_adding_node_with_two_edge(self):
        updatedMatrix, checkerAdjM = self.instantiation_of_variables(2)
        for rowId in range(len(checkerAdjM)):
            for colId in range(len(checkerAdjM[rowId])):
                self.assertEqual(updatedMatrix[rowId][colId], checkerAdjM[rowId][colId])

    def test_adding_node_with_three_edge(self):
        updatedMatrix, checkerAdjM = self.instantiation_of_variables(3)
        for rowId in range(len(checkerAdjM)):
            for colId in range(len(checkerAdjM[rowId])):
                self.assertEqual(updatedMatrix[rowId][colId], checkerAdjM[rowId][colId])

    def test_adding_to_complicated_graph_with_one_edge(self):
        updatedMatrix, checkerAdjM = self.instantiation_of_variables("C1")
        for rowId in range(len(checkerAdjM)):
            for colId in range(len(checkerAdjM[rowId])):
                self.assertEqual(updatedMatrix[rowId][colId], checkerAdjM[rowId][colId])

    def test_adding_to_complicated_graph_with_four_edge(self):
        updatedMatrix, checkerAdjM = self.instantiation_of_variables("C4")
        for rowId in range(len(checkerAdjM)):
            for colId in range(len(checkerAdjM[rowId])):
                self.assertEqual(updatedMatrix[rowId][colId], checkerAdjM[rowId][colId])

    def test_adding_to_complicated_graph_with_seven_edge(self):
        updatedMatrix, checkerAdjM = self.instantiation_of_variables("C7")
        for rowId in range(len(checkerAdjM)):
            for colId in range(len(checkerAdjM[rowId])):
                self.assertEqual(updatedMatrix[rowId][colId], checkerAdjM[rowId][colId])
        
    def test_auto_graph(self):
        for i in range(100):
            adjM, adjNewNode = self.automating_matrix_creation(100)

            copyAdjM = copy.deepcopy(adjM)
            copyNewNode = copy.deepcopy(adjNewNode)
            apspMatrix = floyd_warshall(copyAdjM)
            updatedMatrix = add_new_node(apspMatrix, copyNewNode)

            copyAdjM = copy.deepcopy(adjM)
            copyNewNode = copy.deepcopy(adjNewNode)
            combinedAdjM = combine_adjM(copyAdjM, copyNewNode)
            checkerAdjM = floyd_warshall(combinedAdjM)

            for rowId in range(len(checkerAdjM)):
                for colId in range(len(checkerAdjM[rowId])):
                    self.assertEqual(updatedMatrix[rowId][colId], checkerAdjM[rowId][colId])

    def test_SimpleGraph(self):
        numberOfNodes = 50
        adjM, adjNewNode = self.automating_matrix_creation(numberOfNodes)
        
        copyAdjM = copy.deepcopy(adjM)
        copyNewNode = copy.deepcopy(adjNewNode)

        nodeDictionary = {}                     # instantiating variables to initialize SimpleGraph variable
        for i in range(numberOfNodes):
            nodeDictionary[i] = SimpleNode(i, None, 0)

        graphInstance = SimpleGraph(nodeDictionary)
        graphInstance.calculate_APSP_matrix_using_Floyd_Warshall_algorithm(copyAdjM)
        newNode = SimpleNode(len(nodeDictionary)+1, None, 0)
        graphInstance.add_new_node(newNode, copyNewNode)
        apspM = graphInstance.get_APSP_Matrix()
        
        copyAdjM = copy.deepcopy(adjM)
        copyNewNode = copy.deepcopy(adjNewNode)
        combinedAdjM = combine_adjM(copyAdjM, copyNewNode)
        graphCheckerInstance = SimpleGraph(nodeDictionary)
        graphCheckerInstance.calculate_APSP_matrix_using_Floyd_Warshall_algorithm(combinedAdjM)
        checkerAdjM = graphCheckerInstance.get_APSP_Matrix()

        for rowId in range(len(checkerAdjM)):
                for colId in range(len(checkerAdjM[rowId])):
                    self.assertEqual(apspM[rowId][colId], checkerAdjM[rowId][colId])

if __name__ == "__main__":
    unittest.main()