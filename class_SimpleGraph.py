import math, copy, re

class SimpleGraph:

    def __init__(self, allNodes, adjM) -> None:
        self.INF = math.inf
        self.NodeDictionary = allNodes
        self.originalAdjM = adjM
        self.APSPMatrix = None

    def calculate_APSP_matrix_using_Floyd_Warshall_algorithm(self):
        self.APSPMatrix = []
        for i in range(len(self.originalAdjM)):
            rowValues = []
            for j in range(len(self.originalAdjM)):
                if i == j:
                    rowValues.append([self.originalAdjM[i][j], 'Self', list()])
                else:
                    rowValues.append([self.originalAdjM[i][j], \
                        self.NodeDictionary[i].get_node_objective() == self.NodeDictionary[j].get_node_objective(), \
                        [f'{self.NodeDictionary[i].get_node_id()} -> {self.NodeDictionary[j].get_node_id()}']])
            self.APSPMatrix.append(rowValues)

        for k in range(len(self.originalAdjM)):
            for i in range(len(self.originalAdjM)):
                for j in range(len(self.originalAdjM)):
                    if i == j:
                        self.APSPMatrix[i][j][0] = 0
                    else:
                        oldPathCost = self.APSPMatrix[i][j][0]
                        newPathCost = self.APSPMatrix[i][k][0] + self.APSPMatrix[k][j][0]
                        edges = self.APSPMatrix[i][k][2] + self.APSPMatrix[k][j][2]
                        wrongPath = False
                        for edge in edges:
                            tmp = edge.split(' -> ')
                            stringFormat = re.compile(f'^{tmp[0]} -> {tmp[1]}$|^{tmp[1]} -> {tmp[0]}$')
                            results = list(filter(stringFormat.match, edges))
                            if len(results) > 1:
                                wrongPath = True
                                break
                        if wrongPath:
                            continue
                        if newPathCost < oldPathCost:
                            self.APSPMatrix[i][j][0] = newPathCost
                            self.APSPMatrix[i][j][2] = self.APSPMatrix[i][k][2] + self.APSPMatrix[k][j][2]
                        elif newPathCost == oldPathCost:
                            oldPath = self.APSPMatrix[i][j][2]
                            newPath = self.APSPMatrix[i][k][2] + self.APSPMatrix[k][j][2]
                            if newPath == oldPath:
                                continue
                            elif len(newPath) < len(oldPath):
                                self.APSPMatrix[i][j][2] = newPath
                            elif len(newPath) == len(oldPath):
                                nodesOnNewPath = []
                                nodesOnOldPath = []
                                for id in range(len(newPath)):
                                    nodesOnNewPath += newPath[id].split(' -> ')
                                    nodesOnOldPath += oldPath[id].split(' -> ')
                                nodesOnNewPath = [int(i) for i in set(nodesOnNewPath)]
                                nodesOnOldPath = [int(i) for i in set(nodesOnOldPath)]
                                newCount, oldCount = 0, 0
                                for id in range(len(nodesOnNewPath)):
                                    if nodesOnNewPath[id] != i:
                                        if self.APSPMatrix[i][id][1]:
                                            newCount += 1
                                    if nodesOnOldPath[id] != i:
                                        if self.APSPMatrix[i][id][1]:
                                            oldCount += 1
                                if oldCount < newCount:
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
            lastRowList.append(lastRowValue)
        
        for cellIndex in range(len(self.APSPMatrix)):
            self.originalAdjM[cellIndex].append(adjMatrixNewNode[cellIndex])
            self.originalAdjM[cellIndex].append(adjMatrixNewNode[cellIndex])
            self.APSPMatrix[cellIndex].append(modifiedMatrix[cellIndex])
        self.APSPMatrix.append(lastRowList)
        self.originalAdjM.append(adjMatrixNewNode)

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
                        elif len(newPath) == len(currentPath):
                            nodesOnNewPath = []
                            nodesOnOldPath = []
                            for id in range(len(newPath)):
                                nodesOnNewPath += newPath[id].split(' -> ')
                                nodesOnOldPath += currentPath[id].split(' -> ')
                            nodesOnNewPath = [int(i) for i in set(nodesOnNewPath)]
                            nodesOnOldPath = [int(i) for i in set(nodesOnOldPath)]
                            newCount, oldCount = 0, 0
                            for id in range(len(nodesOnNewPath)):
                                if nodesOnNewPath[id] != i:
                                    if self.APSPMatrix[i][id][1]:
                                        newCount += 1
                                if nodesOnOldPath[id] != i:
                                    if self.APSPMatrix[i][id][1]:
                                        oldCount += 1
                            if oldCount < newCount:
                                self.APSPMatrix[i][len(self.APSPMatrix)-1][2] = newPath
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
                        elif len(newPath) == len(currentPath):
                            nodesOnNewPath = []
                            nodesOnOldPath = []
                            for id in range(len(newPath)):
                                nodesOnNewPath += newPath[id].split(' -> ')
                                nodesOnOldPath += currentPath[id].split(' -> ')
                            nodesOnNewPath = [int(i) for i in set(nodesOnNewPath)]
                            nodesOnOldPath = [int(i) for i in set(nodesOnOldPath)]
                            newCount, oldCount = 0, 0
                            # for id in range(len(nodesOnNewPath)):
                            # print(currentPath, newPath)
                            if nodesOnNewPath[id] != index:
                                if self.APSPMatrix[index][id][1]:
                                    newCount += 1
                            if nodesOnOldPath[id] != index:
                                if self.APSPMatrix[index][id][1]:
                                    oldCount += 1
                            if oldCount < newCount:
                                self.APSPMatrix[index][affectedNode][2] = newPath
                                self.APSPMatrix[affectedNode][index][2] = self.APSPMatrix[affectedNode][colAdded][2] + self.APSPMatrix[colAdded][index][2]

    def delete_node(self, nodeID):
        # update self.NodeDictionary to reflect latest number of nodes
        allKeys = list(self.NodeDictionary.keys())
        tmpDict = {}
        id = 0
        toRemove = None
        idAffected = None
        maxValue = len(allKeys)
        if nodeID == maxValue - 1:
            toRemove = nodeID
            idAffected = nodeID
        else:
            while id < maxValue - 1:
                if self.NodeDictionary[allKeys[id]].get_node_id() == nodeID:
                    idAffected = self.NodeDictionary[allKeys[id]].get_node_id()
                    toRemove = id
                    allKeys.pop(id)
                else:
                    tmpDict[id] = self.NodeDictionary[allKeys[id]]
                    id += 1
            self.NodeDictionary = tmpDict
            del tmpDict

        # update APSP matrix
        del self.APSPMatrix[toRemove]
        del self.originalAdjM[toRemove]

        for rowID in range(len(self.originalAdjM)):
            del self.originalAdjM[rowID][toRemove]
            del self.APSPMatrix[rowID][toRemove]
            
        mappingMatrix = []
        limitCounter = 0
        stringSearch = f'[0-9]+ -> {idAffected}|{idAffected} -> [0-9]+'
        for rowID in range(len(self.APSPMatrix)):
            tmp_row = []
            for colID in range(len(self.APSPMatrix)):
                toModify = False
                for string in self.APSPMatrix[rowID][colID][2]:
                    if re.search(stringSearch, string):
                        limitCounter += 1
                        toModify = True
                        self.APSPMatrix[rowID][colID][0] = self.originalAdjM[rowID][colID]
                        self.APSPMatrix[rowID][colID][2] = [f'{self.NodeDictionary[rowID].get_node_id()} -> {self.NodeDictionary[colID].get_node_id()}']
                        break
                tmp_row.append(toModify)
            mappingMatrix.append(tmp_row)

        sizeOfMatrix = len(self.originalAdjM)
        if limitCounter < sizeOfMatrix ** 2 - sizeOfMatrix and limitCounter > 0:
            for additionalNodeID in range(sizeOfMatrix):
                for i in range(sizeOfMatrix):
                    for j in range(sizeOfMatrix):
                        if mappingMatrix[i][j]:
                            oldPathCost = self.APSPMatrix[i][j][0]
                            newPathCost = self.APSPMatrix[i][additionalNodeID][0] + self.APSPMatrix[additionalNodeID][j][0]
                            if newPathCost < oldPathCost:
                                self.APSPMatrix[i][j][0] = newPathCost
                                self.APSPMatrix[i][j][2] = self.APSPMatrix[i][additionalNodeID][2] + self.APSPMatrix[additionalNodeID][j][2]
                            elif newPathCost == oldPathCost:
                                oldPath = self.APSPMatrix[i][j][2]
                                newPath = self.APSPMatrix[i][additionalNodeID][2] + self.APSPMatrix[additionalNodeID][j][2]
                                if newPath == oldPath:
                                    continue
                                elif len(newPath) < len(oldPath):
                                    self.APSPMatrix[i][j][2] = newPath
                                elif len(newPath) == len(oldPath):
                                    nodesOnNewPath = []
                                    nodesOnOldPath = []
                                    for id in range(len(newPath)):
                                        nodesOnNewPath += newPath[id].split(' -> ')
                                        nodesOnOldPath += oldPath[id].split(' -> ')
                                    nodesOnNewPath = [int(i) for i in set(nodesOnNewPath)]
                                    nodesOnOldPath = [int(i) for i in set(nodesOnOldPath)]
                                    if len(nodesOnNewPath) == len(nodesOnOldPath):
                                        newCount, oldCount = 0, 0
                                        for id in range(len(nodesOnNewPath)):
                                            if nodesOnNewPath[id] != i:
                                                if self.APSPMatrix[i][id][1]:
                                                    newCount += 1
                                            if nodesOnOldPath[id] != i:
                                                if self.APSPMatrix[i][id][1]:
                                                    oldCount += 1
                                        if oldCount < newCount:
                                            self.APSPMatrix[i][j][2] = newPath

        elif limitCounter == sizeOfMatrix ** 2 - sizeOfMatrix:
            self.calculate_APSP_matrix_using_Floyd_Warshall_algorithm()

    # getter and setter methods
    def get_APSP_Matrix(self):
        return self.APSPMatrix

    def update_node_objective(self, id, newObjective):
        self.NodeDictionary[id].update_node_objective(newObjective)
        for index in range(len(self.APSPMatrix)):
            if index == id:
                continue
            cellValue = self.NodeDictionary[index].get_node_objective() == self.NodeDictionary[id].get_node_objective()
            self.APSPMatrix[index][id][1] = cellValue
            self.APSPMatrix[id][index][1] = cellValue