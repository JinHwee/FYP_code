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

    nodeG1 = [5, 3, INF, INF, 6, INF, 4, INF, 5, INF, 7, INF]
    nodeG2 = [19, 12, 17, 11, 15, 14, INF]
    nodeG3 = [INF, INF, INF, 3, INF, INF, 2, INF, INF]

    def common_code_block(self, id):
        if id == 1:
            adjM = copy.deepcopy(self.G1)
            modified_adjM = copy.deepcopy(self.G1)
            newNodeAdjm = copy.deepcopy(self.nodeG1)
        elif id == 2:
            adjM = copy.deepcopy(self.G2)
            modified_adjM = copy.deepcopy(self.G2)
            newNodeAdjm = copy.deepcopy(self.nodeG2)
        elif id == 3:
            adjM = copy.deepcopy(self.G3)
            modified_adjM = copy.deepcopy(self.G3)
            newNodeAdjm = copy.deepcopy(self.nodeG3)
        
        objectives = list(self.objectivesDictionary.keys())
        nodeDictionary = {}
        for id in range(len(adjM)):
            nodeDictionary[id] = SimpleNode(id, None, random.choice(objectives))
        nodeObj = random.choice(objectives)
        newNode = SimpleNode(len(nodeDictionary), None, nodeObj)

        added = SimpleNode(len(nodeDictionary), None, nodeObj)
        modified_nodeDictionary = copy.deepcopy(nodeDictionary)
        modified_nodeDictionary[len(modified_nodeDictionary)] = added

        allKeys = [_ for _ in range(len(modified_nodeDictionary))]
        idToRemove = random.choice(allKeys)
        id = 0
        tmpDict = {}
        while id < len(modified_nodeDictionary)-1:
            if modified_nodeDictionary[allKeys[id]].get_node_id() == idToRemove:
                allKeys.pop(id)
            else:
                tmpDict[id] = modified_nodeDictionary[allKeys[id]]
                id += 1
        modified_nodeDictionary = tmpDict
        del tmpDict

        for rowID in range(len(modified_adjM)):
            modified_adjM[rowID].append(newNodeAdjm[rowID])
            del modified_adjM[rowID][idToRemove]
        modified_adjM.append(newNodeAdjm)
        del modified_adjM[idToRemove]

        return nodeDictionary, adjM, newNodeAdjm, newNode, modified_adjM, modified_nodeDictionary, idToRemove

    def verifier(self, apspM, checkerAdjM):
        for rowId in range(len(checkerAdjM)):
            for colId in range(len(checkerAdjM[rowId])):
                self.assertEqual(apspM[rowId][colId], checkerAdjM[rowId][colId])

    def test_G1_add_remove(self):
        nodeDictionary, adjM, newNodeAdjm, newNode, modified_adjM, modified_nodeDictionary, idToRemove = self.common_code_block(1)
        graphInstance = SimpleGraph(nodeDictionary, adjM)
        graphInstance.calculate_APSP_matrix_using_Floyd_Warshall_algorithm()
        graphInstance.add_new_node(newNode, newNodeAdjm)
        graphInstance.delete_node(idToRemove)
        apspM = graphInstance.get_APSP_Matrix()

        graphChecker = SimpleGraph(modified_nodeDictionary, modified_adjM)
        graphChecker.calculate_APSP_matrix_using_Floyd_Warshall_algorithm()
        checkerAdjM = graphChecker.get_APSP_Matrix()

        self.verifier(apspM, checkerAdjM)
    
    def test_G2_add_remove(self):
        nodeDictionary, adjM, newNodeAdjm, newNode, modified_adjM, modified_nodeDictionary, idToRemove = self.common_code_block(2)
        graphInstance = SimpleGraph(nodeDictionary, adjM)
        graphInstance.calculate_APSP_matrix_using_Floyd_Warshall_algorithm()
        graphInstance.add_new_node(newNode, newNodeAdjm)
        graphInstance.delete_node(idToRemove)
        apspM = graphInstance.get_APSP_Matrix()

        graphChecker = SimpleGraph(modified_nodeDictionary, modified_adjM)
        graphChecker.calculate_APSP_matrix_using_Floyd_Warshall_algorithm()
        checkerAdjM = graphChecker.get_APSP_Matrix()

        self.verifier(apspM, checkerAdjM)
    
    def test_G3_add_remove(self):
        nodeDictionary, adjM, newNodeAdjm, newNode, modified_adjM, modified_nodeDictionary, idToRemove = self.common_code_block(3)
        graphInstance = SimpleGraph(nodeDictionary, adjM)
        graphInstance.calculate_APSP_matrix_using_Floyd_Warshall_algorithm()
        graphInstance.add_new_node(newNode, newNodeAdjm)
        graphInstance.delete_node(idToRemove)
        apspM = graphInstance.get_APSP_Matrix()

        graphChecker = SimpleGraph(modified_nodeDictionary, modified_adjM)
        graphChecker.calculate_APSP_matrix_using_Floyd_Warshall_algorithm()
        checkerAdjM = graphChecker.get_APSP_Matrix()

        self.verifier(apspM, checkerAdjM)

    def automating_matrix_creation(self, number):
        adjMatrix = [[] for _ in range(number)]
        newNode = [random.randint(10,100) for _ in range(number)]
        newNode.append(INF)
        for i in range(number):
            for j in range(i, number):
                if i == j:
                    adjMatrix[i].append(INF)
                else:
                    value = random.randint(10, 100)
                    adjMatrix[i].append(value)
                    adjMatrix[j].append(value)
        
        return adjMatrix, newNode

    def automating_node_dictionary_creation(self, number):
        objective = list(self.objectivesDictionary.keys())
        nodeDictionary = {}
        for id in range(number):
            nodeDictionary[id] = SimpleNode(id, None, random.choice(objective))
        return nodeDictionary

    # def test_randomGraph(self):
    #     numberOfNodes = 50
    #     adjM , adjMNewNode = self.automating_matrix_creation(numberOfNodes)
    #     nodeDictionary = self.automating_node_dictionary_creation(numberOfNodes)
    #     objective = random.choice(list(self.objectivesDictionary.keys()))
    #     newNode = SimpleNode(len(adjM), None, objective)
    #     idToRemove = random.randint(0, numberOfNodes-1)

    #     copy_newNode = copy.deepcopy(newNode)
    #     copy_adjM = copy.deepcopy(adjM)
    #     copy_newNodeAdjM = copy.deepcopy(adjMNewNode)
    #     copy_nodeDictionary = copy.deepcopy(nodeDictionary)
    #     graphInstance = SimpleGraph(copy_nodeDictionary, copy_adjM)
    #     graphInstance.calculate_APSP_matrix_using_Floyd_Warshall_algorithm()
    #     graphInstance.add_new_node(copy_newNode, copy_newNodeAdjM)
    #     graphInstance.delete_node(idToRemove)
    #     apspM = graphInstance.get_APSP_Matrix()

    #     copy_newNode = copy.deepcopy(newNode)
    #     copy_adjM = copy.deepcopy(adjM)
    #     copy_newNodeAdjM = copy.deepcopy(adjMNewNode)
    #     copy_nodeDictionary = copy.deepcopy(nodeDictionary)
    #     copy_nodeDictionary[numberOfNodes] = copy_newNode

    #     allKeys = [_ for _ in range(len(copy_nodeDictionary))]
    #     id = 0
    #     tmpDict = {}
    #     while id < len(copy_nodeDictionary)-1:
    #         if copy_nodeDictionary[allKeys[id]].get_node_id() == idToRemove:
    #             allKeys.pop(id)
    #         else:
    #             tmpDict[id] = copy_nodeDictionary[allKeys[id]]
    #             id += 1
    #     copy_nodeDictionary = tmpDict
    #     del tmpDict

    #     for rowID in range(len(copy_adjM)):
    #         copy_adjM[rowID].append(copy_newNodeAdjM[rowID])
    #         del copy_adjM[rowID][idToRemove]
    #     del copy_newNodeAdjM[idToRemove]
    #     copy_adjM.append(copy_newNodeAdjM)
    #     del copy_adjM[idToRemove]

    #     graphChecker = SimpleGraph(copy_nodeDictionary, copy_adjM)
    #     graphChecker.calculate_APSP_matrix_using_Floyd_Warshall_algorithm()
    #     checkerAdjM = graphChecker.get_APSP_Matrix()

    #     self.verifier(apspM, checkerAdjM)

    def common_delete_only(self, id):
        if id == 1:
            adjM = copy.deepcopy(self.G1)
            modified_adjM = copy.deepcopy(self.G1)
        elif id == 2:
            adjM = copy.deepcopy(self.G2)
            modified_adjM = copy.deepcopy(self.G2)
        elif id == 3:
            adjM = copy.deepcopy(self.G3)
            modified_adjM = copy.deepcopy(self.G3)
        
        objectives = list(self.objectivesDictionary.keys())
        nodeDictionary = {}
        for id in range(len(adjM)):
            nodeDictionary[id] = SimpleNode(id, None, random.choice(objectives))

        modified_nodeDictionary = copy.deepcopy(nodeDictionary)

        allKeys = [_ for _ in range(len(modified_nodeDictionary))]
        idToRemove = random.choice(allKeys)
        id = 0
        tmpDict = {}
        while id < len(modified_nodeDictionary)-1:
            if modified_nodeDictionary[allKeys[id]].get_node_id() == idToRemove:
                allKeys.pop(id)
            else:
                tmpDict[id] = modified_nodeDictionary[allKeys[id]]
                id += 1
        modified_nodeDictionary = tmpDict
        del tmpDict

        for rowID in range(len(modified_adjM)):
            del modified_adjM[rowID][idToRemove]
        del modified_adjM[idToRemove]

        return nodeDictionary, adjM, modified_adjM, modified_nodeDictionary, idToRemove

    def test_remove_G1(self):
        nodeDictionary, adjM, modified_adjM, modified_nodeDictionary, idToRemove = self.common_delete_only(1)
        graphInstance = SimpleGraph(nodeDictionary, adjM)
        graphInstance.calculate_APSP_matrix_using_Floyd_Warshall_algorithm()
        graphInstance.delete_node(idToRemove)
        apspM = graphInstance.get_APSP_Matrix()

        graphChecker = SimpleGraph(modified_nodeDictionary, modified_adjM)
        graphChecker.calculate_APSP_matrix_using_Floyd_Warshall_algorithm()
        checkerAdjM = graphChecker.get_APSP_Matrix()

        self.verifier(apspM, checkerAdjM)
    
    def test_remove_G2(self):
        nodeDictionary, adjM, modified_adjM, modified_nodeDictionary, idToRemove = self.common_delete_only(2)
        graphInstance = SimpleGraph(nodeDictionary, adjM)
        graphInstance.calculate_APSP_matrix_using_Floyd_Warshall_algorithm()
        graphInstance.delete_node(idToRemove)
        apspM = graphInstance.get_APSP_Matrix()

        graphChecker = SimpleGraph(modified_nodeDictionary, modified_adjM)
        graphChecker.calculate_APSP_matrix_using_Floyd_Warshall_algorithm()
        checkerAdjM = graphChecker.get_APSP_Matrix()

        self.verifier(apspM, checkerAdjM)
    
    def test_remove_G3(self):
        nodeDictionary, adjM, modified_adjM, modified_nodeDictionary, idToRemove = self.common_delete_only(3)
        graphInstance = SimpleGraph(nodeDictionary, adjM)
        graphInstance.calculate_APSP_matrix_using_Floyd_Warshall_algorithm()
        graphInstance.delete_node(idToRemove)
        apspM = graphInstance.get_APSP_Matrix()

        graphChecker = SimpleGraph(modified_nodeDictionary, modified_adjM)
        graphChecker.calculate_APSP_matrix_using_Floyd_Warshall_algorithm()
        checkerAdjM = graphChecker.get_APSP_Matrix()

        self.verifier(apspM, checkerAdjM)