import math, copy

class SimpleGraph:

    def __init__(self, allNodes) -> None:
        self.INF = math.inf
        self.NodeDictionary = allNodes
        self.APSPMatrix = None

    def calculate_APSP_matrix_using_Floyd_Warshall_algorithm(self, adjM):
        self.APSPMatrix = []
        for i in range(len(adjM)):
            rowValues = []
            for j in range(len(adjM)):
                if i == j:
                    rowValues.append([adjM[i][j], 'Self', list()])
                else:
                    rowValues.append([adjM[i][j], \
                        self.NodeDictionary[i].get_node_objective() == self.NodeDictionary[j].get_node_objective(), \
                        [f'{self.NodeDictionary[i].get_node_id()} -> {self.NodeDictionary[j].get_node_id()}']])
            self.APSPMatrix.append(rowValues)

        for k in range(len(adjM)):
            for i in range(len(adjM)):
                for j in range(len(adjM)):
                    if i == j:
                        self.APSPMatrix[i][j][0] = 0
                    else:
                        oldPathCost = self.APSPMatrix[i][j][0]
                        newPathCost = self.APSPMatrix[i][k][0] + self.APSPMatrix[k][j][0]
                        if newPathCost < oldPathCost:
                            self.APSPMatrix[i][j][0] = newPathCost
                            self.APSPMatrix[i][j][2] = self.APSPMatrix[i][k][2] + self.APSPMatrix[k][j][2]
                        elif newPathCost == oldPathCost:
                            oldPath = self.APSPMatrix[i][j][2]
                            newPath = self.APSPMatrix[i][k][2] + self.APSPMatrix[k][j][2]
                            if len(newPath) < len(oldPath):
                                self.APSPMatrix[i][j][2] = newPath

    # adjMatrix refers to the graph's adjacency matrix, adjMatrixNewNode refers to the newly added node's adjacency matrix.
    def add_new_node(self, newNode, adjMatrixNewNode):
        # update NodeDictionary with new Node
        self.NodeDictionary[len(self.NodeDictionary)] = newNode
        
        modifiedMatrix = []
        lastRowList = []
        for costIndex in range(len(adjMatrixNewNode)):
            if costIndex != len(adjMatrixNewNode) - 1:
                cellValue = [adjMatrixNewNode[costIndex], \
                    newNode.get_node_objective() == self.NodeDictionary[costIndex].get_node_objective(),\
                        [f'{self.NodeDictionary[costIndex].get_node_id()} -> {self.NodeDictionary[len(adjMatrixNewNode)-1].get_node_id()}']]
                lastRowValue = [adjMatrixNewNode[costIndex], \
                    newNode.get_node_objective() == self.NodeDictionary[costIndex].get_node_objective(),\
                        [f'{self.NodeDictionary[len(adjMatrixNewNode)-1].get_node_id()} -> {self.NodeDictionary[costIndex].get_node_id()}']]
                modifiedMatrix.append(cellValue)
            else:
                lastRowValue = [0, 'Self', list()]
                # cellValue = [0, 'Self']
            lastRowList.append(lastRowValue)
        
        for cellIndex in range(len(self.APSPMatrix)):
            self.APSPMatrix[cellIndex].append(modifiedMatrix[cellIndex])
        self.APSPMatrix.append(lastRowList)

        # compute shortest path for newly added node, check which vertex is directly connected to the newly added node
        nonZeroEdgeCosts = [i for i in adjMatrixNewNode if i > 0 and i != math.inf]
        # store the affected nodes for recomputation later on
        affectedNodes = []
        # if node added has one additional edge, number of non-zero values = 1
        if len(nonZeroEdgeCosts) == 1:
            connectedIndex = adjMatrixNewNode.index(nonZeroEdgeCosts[0])
            affectedNodes.append(connectedIndex)
            relevantRow = self.APSPMatrix[connectedIndex]
            for i in range(len(relevantRow)-1):
                if connectedIndex == i:
                    continue
                newPathCost = relevantRow[i][0] + relevantRow[len(self.APSPMatrix)-1][0]
                self.APSPMatrix[i][len(self.APSPMatrix)-1][0] = newPathCost
                self.APSPMatrix[len(self.APSPMatrix)-1][i][0] = newPathCost
                self.APSPMatrix[i][len(self.APSPMatrix)-1][2] = self.APSPMatrix[connectedIndex][i][2] + self.APSPMatrix[connectedIndex][len(self.APSPMatrix)-1][2]
                self.APSPMatrix[len(self.APSPMatrix)-1][i][2] = self.APSPMatrix[i][connectedIndex][2] + self.APSPMatrix[len(self.APSPMatrix)-1][connectedIndex][2]
        else:
            # recompute for new node which has more than 1 edge
            copyAddedNode = copy.deepcopy(adjMatrixNewNode)
            for cost in nonZeroEdgeCosts:
                connectedIndex = copyAddedNode.index(cost)
                copyAddedNode[connectedIndex] = 0           # in case more than 1 edge has the same value, which causes the index to return incorrect index
                affectedNodes.append(connectedIndex)
                relevantRow = self.APSPMatrix[connectedIndex]
                for i in range(len(relevantRow)-1):
                    if connectedIndex == i:
                        continue
                    previousCost = self.APSPMatrix[len(self.APSPMatrix)-1][i][0]
                    newPathCost = relevantRow[i][0] + relevantRow[len(self.APSPMatrix)-1][0]
                    if newPathCost < previousCost:
                        self.APSPMatrix[i][len(self.APSPMatrix)-1][0] = newPathCost
                        self.APSPMatrix[len(self.APSPMatrix)-1][i][0] = newPathCost
                        self.APSPMatrix[i][len(self.APSPMatrix)-1][2] = self.APSPMatrix[i][connectedIndex][2] + self.APSPMatrix[connectedIndex][len(self.APSPMatrix)-1][2]
                        self.APSPMatrix[len(self.APSPMatrix)-1][i][2] = self.APSPMatrix[len(self.APSPMatrix)-1][connectedIndex][2] + self.APSPMatrix[connectedIndex][i][2]
                    elif newPathCost == previousCost:                   # choose the path that has the least number of nodes
                        currentPath = self.APSPMatrix[len(self.APSPMatrix)-1][i][2]
                        newPath = self.APSPMatrix[i][connectedIndex][2] + self.APSPMatrix[connectedIndex][len(self.APSPMatrix)-1][2]
                        if len(newPath) < len(currentPath):
                            self.APSPMatrix[i][len(self.APSPMatrix)-1][2] = self.APSPMatrix[i][connectedIndex][2] + self.APSPMatrix[connectedIndex][len(self.APSPMatrix)-1][2]
                            self.APSPMatrix[len(self.APSPMatrix)-1][i][2] = self.APSPMatrix[len(self.APSPMatrix)-1][connectedIndex][2] + self.APSPMatrix[connectedIndex][i][2]

        colAdded = len(self.APSPMatrix) - 1           # column id is equivalent to row id
        appendedBefore = []
        while len(affectedNodes) != 0:
            affectedNode = affectedNodes.pop(0)
            affectedRow = self.APSPMatrix[affectedNode]
            for index in range(len(affectedRow)):
                if affectedNode == index:
                    continue
                prevPathCost = affectedRow[index][0]
                potentialShorterCost = self.APSPMatrix[index][colAdded][0] + self.APSPMatrix[colAdded][affectedNode][0]
                if potentialShorterCost < prevPathCost:
                    self.APSPMatrix[affectedNode][index][0] = potentialShorterCost
                    self.APSPMatrix[index][affectedNode][0] = potentialShorterCost
                    self.APSPMatrix[affectedNode][index][2] = self.APSPMatrix[affectedNode][colAdded][2] + self.APSPMatrix[colAdded][index][2]
                    self.APSPMatrix[index][affectedNode][2] = self.APSPMatrix[index][colAdded][2] + self.APSPMatrix[colAdded][affectedNode][2]
                    if index not in appendedBefore:
                        affectedNodes.append(index)
                        appendedBefore.append(index)
                elif potentialShorterCost == prevPathCost:                   # choose the path that has the least number of nodes
                        currentPath = affectedRow[index][2]
                        newPath = self.APSPMatrix[index][colAdded][2] + self.APSPMatrix[colAdded][affectedNode][2]
                        if len(newPath) < len(currentPath):
                            self.APSPMatrix[affectedNode][index][2] = self.APSPMatrix[affectedNode][colAdded][2] + self.APSPMatrix[colAdded][index][2]
                            self.APSPMatrix[index][affectedNode][2] = self.APSPMatrix[index][colAdded][2] + self.APSPMatrix[colAdded][affectedNode][2]


    # getter and setter methods
    def get_APSP_Matrix(self):
        return self.APSPMatrix
