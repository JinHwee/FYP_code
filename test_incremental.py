import unittest
from dev_incremental_approach import *
import math, copy

class  TestIncrementalAPSP(unittest.TestCase):

    adjM = [
        [math.inf, 13, 40, math.inf],
        [13, math.inf, 16, math.inf],
        [40, 16, math.inf, 5],
        [math.inf, math.inf, 5, math.inf]
    ]

    adjNewNode_One = [math.inf, 2, math.inf, math.inf, math.inf]        # new node with one edge added, connected to Node 2
    adjNewNode_Two = [math.inf, 2, math.inf, 3, math.inf]               # new node with two edge added, connected to Node 2 and 4
    adjNewNode_Three = [math.inf, 2, 5, 3, math.inf]                    # new node with three edge added, connected to 2, 3 and 4

    complicatedGraph = [
        [math.inf, 82, 15, math.inf, math.inf, math.inf, math.inf],
        [82, math.inf, 4, math.inf, math.inf, math.inf, math.inf],
        [15, 4, math.inf, 95, math.inf, 36, 32],
        [math.inf, math.inf, 95, math.inf, 29, math.inf, math.inf],
        [math.inf, math.inf, math.inf, 29, math.inf, 18, math.inf],
        [math.inf, math.inf, 36, math.inf, 18, math.inf, 95],
        [math.inf, math.inf, 32, math.inf, math.inf, 95, math.inf],
    ]

    complicatedNewNode_One = [87, math.inf, math.inf, math.inf, math.inf, math.inf, math.inf, math.inf]
    complicatedNewNode_Four = [87, 95, 70, 12, math.inf, math.inf, math.inf, math.inf]
    complicatedNewNode_Seven = [87, 95, 70, 12, 37, 12, 9, math.inf]

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
        combinedAdjM = combine_adjM(copyAdjM, copyNewNode)
        checkerAdjM = floyd_warshall(combinedAdjM)

        return updateAdjM, checkerAdjM

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
        
if __name__ == "__main__":
    unittest.main()