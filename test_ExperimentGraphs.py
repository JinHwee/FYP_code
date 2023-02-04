import unittest
from class_SimpleGraph import *
from class_SimpleNode import *
import math, copy, random

INF = math.inf

class Test_ExperimentGraphs(unittest.TestCase):

    objectivesDictionary = {1.1: "CIFAR 10", 1.2: "CIFAR 100", 2.1:"NLP"}       # what each float represents

    G1 = [
        [INF, 2, 5, INF, INF, INF, INF, INF, INF, INF, INF], 
        [2, INF, INF, 2, INF, INF, INF, INF, INF, INF, INF], 
        [5, INF, INF, 2, 1, INF, INF, INF, INF, 6, INF], 
        [INF, 2, 2, INF, INF, 6, 3, INF, INF, INF, INF], 
        [INF, INF, 1, INF, INF, INF, 1, 2, INF, 5, INF], 
        [INF, INF, INF, 6, INF, INF, 7, INF, INF, INF, 6], 
        [INF, INF, INF, 3, 1, 7, INF, INF, 4, INF, INF], 
        [INF, INF, INF, INF, 2, INF, INF, INF, INF, 5, INF], 
        [INF, INF, INF, INF, INF, INF, 4, INF, INF, INF, 5], 
        [INF, INF, 6, INF, 5, INF, INF, 5, INF, INF, 7], 
        [INF, INF, INF, INF, INF, 6, INF, INF, 5, 7, INF], 
    ]

    G2 = [
        [INF, 11, 21, 18, 18, 20], 
        [11, INF, 33, 41, 36, 17], 
        [21, 33, INF, 15, 24, 42], 
        [18, 41, 15, INF, 23, 36], 
        [18, 36, 24, 23, INF, 36], 
        [20, 17, 42, 36, 36, INF], 
    ]

    G3 = [
        [INF, 5, INF, INF, INF, INF, INF, INF], 
        [5, INF, 5, 4, 3, INF, INF, INF], 
        [INF, 5, INF, INF, INF, INF, INF, INF], 
        [INF, 4, INF, INF, INF, 1, 2, 3], 
        [INF, 3, INF, INF, INF, 2, INF, INF], 
        [INF, INF, INF, 1, 2, INF, INF, INF], 
        [INF, INF, INF, 2, INF, INF, INF, 2], 
        [INF, INF, INF, 3, INF, INF, 2, INF], 
    ]

    # create a new SimpleNode to be inserted, with varying edge weights
    def create_newNode(self, size, large, max=False, min=False):
        if max:
            newNode = [9999 for _ in range(size)]
        elif min:
            newNode = [1 for _ in range(size)]
        elif large:
            newNode = [random.randint(10, 50) for _ in range(size)]
        else:
            newNode = [random.randint(1, 6) for _ in range(size)]
        newNode.append(INF)

        return newNode
    
    # pass in the adjacency matrix of the graph and the new node
    def combine_matrix(self, adjM, newNode):
        for rowID in range(len(adjM)):
            adjM[rowID].append(newNode[rowID])
        adjM.append(newNode)

    # instantiation of variables in one common code block
    def common_code_block(self, ID, large, max=False, min=False):
        if ID == 1:
            adjM = copy.deepcopy(self.G1)
        elif ID == 2:
            adjM = copy.deepcopy(self.G2)
        elif ID == 3:
            adjM = copy.deepcopy(self.G3)

        size = len(adjM)
        newNodeAdjM = self.create_newNode(size, large, max, min)

        nodeDictionary = {}
        for i in range(size):
            nodeDictionary[i] = SimpleNode(i, None, 0)
        
        copy_adjM = copy.deepcopy(adjM)
        copy_newNodeAdjM = copy.deepcopy(newNodeAdjM)
        graphInstance = SimpleGraph(nodeDictionary)
        graphInstance.calculate_APSP_matrix_using_Floyd_Warshall_algorithm(copy_adjM)

        newNode = SimpleNode(size, None, 0)
        graphInstance.add_new_node(newNode, copy_newNodeAdjM)
        apspM = graphInstance.get_APSP_Matrix()

        copy_adjM = copy.deepcopy(adjM)        
        copy_newNodeAdjM = copy.deepcopy(newNodeAdjM)
        self.combine_matrix(copy_adjM, copy_newNodeAdjM)
        nodeDictionary[size] = newNode
        graphCheckerInstance = SimpleGraph(nodeDictionary)
        graphCheckerInstance.calculate_APSP_matrix_using_Floyd_Warshall_algorithm(copy_adjM)
        checkerAdjM = graphCheckerInstance.get_APSP_Matrix()

        return apspM, checkerAdjM

    # test_?_G? are for addition of nodes to the graph
    def test_1_G1(self):
        apspM, checkerAdjM = self.common_code_block(1, True)
        for rowId in range(len(checkerAdjM)):
            for colId in range(len(checkerAdjM[rowId])):
                self.assertEqual(apspM[rowId][colId], checkerAdjM[rowId][colId])
        
    def test_2_G1(self):
        apspM, checkerAdjM = self.common_code_block(1, False)
        for rowId in range(len(checkerAdjM)):
            for colId in range(len(checkerAdjM[rowId])):
                self.assertEqual(apspM[rowId][colId], checkerAdjM[rowId][colId])

    def test_3_G1(self):
        apspM, checkerAdjM = self.common_code_block(1, True, max=True)
        for rowId in range(len(checkerAdjM)):
            for colId in range(len(checkerAdjM[rowId])):
                self.assertEqual(apspM[rowId][colId], checkerAdjM[rowId][colId])
        
    def test_4_G1(self):
        apspM, checkerAdjM = self.common_code_block(1, False, min=True)
        for rowId in range(len(checkerAdjM)):
            for colId in range(len(checkerAdjM[rowId])):
                self.assertEqual(apspM[rowId][colId], checkerAdjM[rowId][colId])

    def test_1_G2(self):
        apspM, checkerAdjM = self.common_code_block(2, True)
        for rowId in range(len(checkerAdjM)):
            for colId in range(len(checkerAdjM[rowId])):
                self.assertEqual(apspM[rowId][colId], checkerAdjM[rowId][colId])
    
    def test_2_G2(self):
        apspM, checkerAdjM = self.common_code_block(2, False)
        for rowId in range(len(checkerAdjM)):
            for colId in range(len(checkerAdjM[rowId])):
                self.assertEqual(apspM[rowId][colId], checkerAdjM[rowId][colId])
    
    def test_3_G2(self):
        apspM, checkerAdjM = self.common_code_block(2, True, max=True)
        for rowId in range(len(checkerAdjM)):
            for colId in range(len(checkerAdjM[rowId])):
                self.assertEqual(apspM[rowId][colId], checkerAdjM[rowId][colId])
    
    def test_4_G2(self):
        apspM, checkerAdjM = self.common_code_block(2, False, min=True)
        for rowId in range(len(checkerAdjM)):
            for colId in range(len(checkerAdjM[rowId])):
                self.assertEqual(apspM[rowId][colId], checkerAdjM[rowId][colId])
    
    def test_1_G3(self):
        apspM, checkerAdjM = self.common_code_block(3, True)
        for rowId in range(len(checkerAdjM)):
            for colId in range(len(checkerAdjM[rowId])):
                self.assertEqual(apspM[rowId][colId], checkerAdjM[rowId][colId])
    
    def test_2_G3(self):
        apspM, checkerAdjM = self.common_code_block(3, False)
        for rowId in range(len(checkerAdjM)):
            for colId in range(len(checkerAdjM[rowId])):
                self.assertEqual(apspM[rowId][colId], checkerAdjM[rowId][colId])

    def test_3_G3(self):
        apspM, checkerAdjM = self.common_code_block(3, True, max=True)
        for rowId in range(len(checkerAdjM)):
            for colId in range(len(checkerAdjM[rowId])):
                self.assertEqual(apspM[rowId][colId], checkerAdjM[rowId][colId])
    
    def test_4_G3(self):
        apspM, checkerAdjM = self.common_code_block(3, False, min=True)
        for rowId in range(len(checkerAdjM)):
            for colId in range(len(checkerAdjM[rowId])):
                self.assertEqual(apspM[rowId][colId], checkerAdjM[rowId][colId])