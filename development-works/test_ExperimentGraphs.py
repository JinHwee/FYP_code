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
    def create_newNode(self, size, max=False, min=False):
        if max:
            newNode = [9999 for _ in range(size)]
        elif min:
            newNode = [1 for _ in range(size)]
        else:
            newNode = [random.randint(1, 50) for _ in range(size)]
        newNode.append(INF)

        return newNode
    
    # pass in the adjacency matrix of the graph and the new node
    def combine_matrix(self, adjM, newNode):
        for rowID in range(len(adjM)):
            adjM[rowID].append(newNode[rowID])
        adjM.append(newNode)

    # instantiation of variables in one common code block
    def common_code_block(self, ID, max=False, min=False, objective=False, changeObj=False):
        if ID == 1:
            adjM = copy.deepcopy(self.G1)
        elif ID == 2:
            adjM = copy.deepcopy(self.G2)
        elif ID == 3:
            adjM = copy.deepcopy(self.G3)

        size = len(adjM)
        newNodeAdjM = self.create_newNode(size, max, min)

        nodeDictionary = {}
        objectives = [i for i in self.objectivesDictionary.keys()]
        for i in range(size):
            if objective:
                nodeDictionary[i] = SimpleNode(i, None, random.choice(objectives))
            else:
                nodeDictionary[i] = SimpleNode(i, None, 0)
        
        copy_adjM = copy.deepcopy(adjM)
        copy_newNodeAdjM = copy.deepcopy(newNodeAdjM)
        graphInstance = SimpleGraph(nodeDictionary)
        graphInstance.calculate_APSP_matrix_using_Floyd_Warshall_algorithm(copy_adjM)

        if objective:
            newNode = SimpleNode(size, None, random.choice(objectives))
        else:
            newNode = SimpleNode(size, None, 0)
        graphInstance.add_new_node(newNode, copy_newNodeAdjM)
        if changeObj:
            graphInstance.update_node_objective(newNode.get_node_id(), 5)       # node objective 5 doesn't exist; for checking only
        apspM = graphInstance.get_APSP_Matrix()

        copy_adjM = copy.deepcopy(adjM)        
        copy_newNodeAdjM = copy.deepcopy(newNodeAdjM)
        self.combine_matrix(copy_adjM, copy_newNodeAdjM)
        nodeDictionary[size] = newNode
        graphCheckerInstance = SimpleGraph(nodeDictionary)
        graphCheckerInstance.calculate_APSP_matrix_using_Floyd_Warshall_algorithm(copy_adjM)
        checkerAdjM = graphCheckerInstance.get_APSP_Matrix()

        return apspM, checkerAdjM

    def common_code_block_multiple_newNodes(self, ID):
        if ID == 1:
            adjM = copy.deepcopy(self.G1)
        elif ID == 2:
            adjM = copy.deepcopy(self.G2)
        elif ID == 3:
            adjM = copy.deepcopy(self.G3)

        size = len(adjM)
        nodeDictionary = {}
        objectives = [i for i in self.objectivesDictionary.keys()]
        for i in range(size):
            nodeDictionary[i] = SimpleNode(i, None, random.choice(objectives))

        newNode1 = SimpleNode(size, None, 5)
        newNode2 = SimpleNode(size+1, None, 5)
        newNode3 = SimpleNode(size+2, None, 5)
        newNode4 = SimpleNode(size+3, None, 5)

        newNodeAdjM1 = self.create_newNode(size)
        newNodeAdjM2 = self.create_newNode(size+1)
        newNodeAdjM3 = self.create_newNode(size+2)
        newNodeAdjM4 = self.create_newNode(size+3)

        copy_adjM = copy.deepcopy(adjM)
        graphInstance = SimpleGraph(nodeDictionary)
        graphInstance.calculate_APSP_matrix_using_Floyd_Warshall_algorithm(copy_adjM)

        copy_newNodeAdjM = copy.deepcopy(newNodeAdjM1)
        graphInstance.add_new_node(newNode1, copy_newNodeAdjM)
        copy_newNodeAdjM = copy.deepcopy(newNodeAdjM2)
        graphInstance.add_new_node(newNode2, copy_newNodeAdjM)
        copy_newNodeAdjM = copy.deepcopy(newNodeAdjM3)
        graphInstance.add_new_node(newNode3, copy_newNodeAdjM)
        copy_newNodeAdjM = copy.deepcopy(newNodeAdjM4)
        graphInstance.add_new_node(newNode4, copy_newNodeAdjM)
        apspM = graphInstance.get_APSP_Matrix()

        copy_adjM = copy.deepcopy(adjM)
        copy_newNodeAdjM = copy.deepcopy(newNodeAdjM1)
        self.combine_matrix(copy_adjM, copy_newNodeAdjM)
        copy_newNodeAdjM = copy.deepcopy(newNodeAdjM2)
        self.combine_matrix(copy_adjM, copy_newNodeAdjM)
        copy_newNodeAdjM = copy.deepcopy(newNodeAdjM3)
        self.combine_matrix(copy_adjM, copy_newNodeAdjM)
        copy_newNodeAdjM = copy.deepcopy(newNodeAdjM4)
        self.combine_matrix(copy_adjM, copy_newNodeAdjM)

        nodeDictionary[size] = newNode1
        nodeDictionary[size+1] = newNode2
        nodeDictionary[size+2] = newNode3
        nodeDictionary[size+3] = newNode4

        graphCheckerInstance = SimpleGraph(nodeDictionary)
        graphCheckerInstance.calculate_APSP_matrix_using_Floyd_Warshall_algorithm(copy_adjM)
        checkerAdjM = graphCheckerInstance.get_APSP_Matrix()
        
        return apspM, checkerAdjM

    def verifier(self, apspM, checkerAdjM):
        for rowId in range(len(checkerAdjM)):
            for colId in range(len(checkerAdjM[rowId])):
                self.assertEqual(apspM[rowId][colId], checkerAdjM[rowId][colId])

    # test_?_G? are for addition of nodes to the graph
    def test_1_G1(self):
        apspM, checkerAdjM = self.common_code_block(1, max=True)
        self.verifier(apspM, checkerAdjM)
        
    def test_2_G1(self):
        apspM, checkerAdjM = self.common_code_block(1, min=True)
        self.verifier(apspM, checkerAdjM)

    def test_3_G1(self):
        apspM, checkerAdjM = self.common_code_block(1)
        self.verifier(apspM, checkerAdjM)

    def test_1_G2(self):
        apspM, checkerAdjM = self.common_code_block(2, max=True)
        self.verifier(apspM, checkerAdjM)
    
    def test_2_G2(self):
        apspM, checkerAdjM = self.common_code_block(2, min=True)
        self.verifier(apspM, checkerAdjM)
    
    def test_3_G2(self):
        apspM, checkerAdjM = self.common_code_block(2)
        self.verifier(apspM, checkerAdjM)
    
    def test_1_G3(self):
        apspM, checkerAdjM = self.common_code_block(3, max=True)
        self.verifier(apspM, checkerAdjM)
    
    def test_2_G3(self):
        apspM, checkerAdjM = self.common_code_block(3, min=True)
        self.verifier(apspM, checkerAdjM)

    def test_3_G3(self):
        apspM, checkerAdjM = self.common_code_block(3)
        self.verifier(apspM, checkerAdjM)

    # testing objective; note that id of SimpleNodes ranges from 0 to len(nodeDictionary)-1
    def test_Obj_1_G1(self):
        apspM, checkerAdjM = self.common_code_block(1, min=True, objective=True)
        self.verifier(apspM, checkerAdjM)
    
    def test_Obj_2_G1(self):
        apspM, checkerAdjM = self.common_code_block(1, max=True, objective=True)
        self.verifier(apspM, checkerAdjM)

    def test_Obj_1_G2(self):
        apspM, checkerAdjM = self.common_code_block(2, min=True, objective=True)
        self.verifier(apspM, checkerAdjM)
    
    def test_Obj_2_G2(self):
        apspM, checkerAdjM = self.common_code_block(2, max=True, objective=True)
        self.verifier(apspM, checkerAdjM)

    def test_Obj_1_G3(self):
        apspM, checkerAdjM = self.common_code_block(3, min=True, objective=True)
        self.verifier(apspM, checkerAdjM)
    
    def test_Obj_2_G3(self):
        apspM, checkerAdjM = self.common_code_block(3, min=True, objective=True)
        self.verifier(apspM, checkerAdjM)
    
    # objective change
    def test_ObjChange_1_G1(self):
        apspM, checkerAdjM = self.common_code_block(1, min=True, objective=True, changeObj=True)
        self.verifier(apspM, checkerAdjM)

    def test_ObjChange_2_G1(self):
        apspM, checkerAdjM = self.common_code_block(1, max=True, objective=True, changeObj=True)
        self.verifier(apspM, checkerAdjM)
    
    def test_ObjChange_1_G2(self):
        apspM, checkerAdjM = self.common_code_block(2, min=True, objective=True, changeObj=True)
        self.verifier(apspM, checkerAdjM)

    def test_ObjChange_2_G2(self):
        apspM, checkerAdjM = self.common_code_block(2, max=True, objective=True, changeObj=True)
        self.verifier(apspM, checkerAdjM)

    def test_ObjChange_1_G3(self):
        apspM, checkerAdjM = self.common_code_block(3, min=True, objective=True, changeObj=True)
        self.verifier(apspM, checkerAdjM)

    def test_ObjChange_2_G3(self):
        apspM, checkerAdjM = self.common_code_block(3, max=True, objective=True, changeObj=True)
        self.verifier(apspM, checkerAdjM)

    # adding multiple new nodes
    def test_add_multiple_nodes_G1(self):
        apspM, checkerAdjM = self.common_code_block_multiple_newNodes(1)
        self.verifier(apspM, checkerAdjM)

    def test_add_multiple_nodes_G2(self):
        apspM, checkerAdjM = self.common_code_block_multiple_newNodes(2)
        self.verifier(apspM, checkerAdjM)

    def test_add_multiple_nodes_G3(self):
        apspM, checkerAdjM = self.common_code_block_multiple_newNodes(3)
        self.verifier(apspM, checkerAdjM)