import math, copy

def combine_adjM(adjM, newNode):
    for rowIndex in range(len(adjM)):
        adjM[rowIndex].append(newNode[rowIndex])
    adjM.append(newNode)
    return adjM

def floyd_warshall(matrix):
    for k in range(len(matrix)):
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if i == j:
                    matrix[i][j] = 0
                else:
                    matrix[i][j] = min(matrix[i][j], matrix[i][k] + matrix[k][j])

    return matrix

# adjMatrix refers to the graph's adjacency matrix, adjMatrixNewNode refers to the newly added node's adjacency matrix.
def add_new_node(adjMatrix, adjMatrixNewNode):
    # update the adjMatrix to include new Node
    index = 0
    for row in adjMatrix:
        row.append(adjMatrixNewNode[index])
        index += 1
    adjMatrix.append(adjMatrixNewNode)
    adjMatrix[len(adjMatrix)-1][len(adjMatrix)-1] = 0       # value to self set to 0, modifies both arrays
    
    # compute shortest path for newly added node, check which vertex is directly connected to the newly added node
    nonZeroEdgeCosts = [i for i in adjMatrixNewNode if i > 0 and i != math.inf]
    # store the affected nodes for recomputation later on
    affectedNodes = []
    # if node added has one additional edge, number of non-zero values = 1
    if len(nonZeroEdgeCosts) == 1:
        connectedIndex = adjMatrix[len(adjMatrix)-1].index(nonZeroEdgeCosts[0])
        affectedNodes.append(connectedIndex)
        relevantRow = adjMatrix[connectedIndex]
        for i in range(len(relevantRow)-1):
            newPathCost = relevantRow[i] + relevantRow[len(adjMatrix)-1]
            adjMatrix[i][len(adjMatrix)-1] = newPathCost
            adjMatrix[len(adjMatrix)-1][i] = newPathCost 
    else:
        # recompute for new node which has more than 1 edge
        copyAddedNode = copy.deepcopy(adjMatrix[len(adjMatrix)-1])
        for cost in nonZeroEdgeCosts:
            connectedIndex = copyAddedNode.index(cost)
            copyAddedNode[connectedIndex] = 0           # in case more than 1 edge has the same value, which causes the index to return incorrect index
            affectedNodes.append(connectedIndex)
            relevantRow = adjMatrix[connectedIndex]
            for i in range(len(relevantRow)-1):
                if connectedIndex == i:
                    continue
                previousCost = adjMatrix[len(adjMatrix)-1][i]
                newPathCost = relevantRow[i] + relevantRow[len(adjMatrix)-1]
                if newPathCost < previousCost:
                    adjMatrix[i][len(adjMatrix)-1] = newPathCost
                    adjMatrix[len(adjMatrix)-1][i] = newPathCost
    
    colAdded = len(adjMatrix) - 1           # column id is equivalent to row id
    appendedBefore = []
    while len(affectedNodes) != 0:
        affectedNode = affectedNodes.pop(0)
        affectedRow = adjMatrix[affectedNode]
        for index in range(len(affectedRow)):
            prevPathCost = affectedRow[index]
            potentialShorterCost = adjMatrix[index][colAdded] + adjMatrix[colAdded][affectedNode]
            if potentialShorterCost < prevPathCost:
                adjMatrix[affectedNode][index] = potentialShorterCost
                adjMatrix[index][affectedNode] = potentialShorterCost
                if index not in appendedBefore:
                    affectedNodes.append(index)
                    appendedBefore.append(index)

    return adjMatrix
