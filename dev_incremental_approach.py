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
    
    # compute shortest path for newly added node
    nonZeroEdgeCosts = [i for i in adjMatrixNewNode if i > 0 and i != math.inf]
    # if node added has one additional edge, number of non-zero values = 1
    if len(nonZeroEdgeCosts) == 1:
        connectedIndex = adjMatrix[len(adjMatrix)-1].index(nonZeroEdgeCosts[0])
        relevantRow = adjMatrix[connectedIndex]
        for i in range(len(relevantRow)-1):
            newPathCost = relevantRow[i] + relevantRow[len(adjMatrix)-1]
            adjMatrix[i][len(adjMatrix)-1] = newPathCost
            adjMatrix[len(adjMatrix)-1][i] = newPathCost 
    else:
        for cost in nonZeroEdgeCosts:
            connectedIndex = adjMatrix[len(adjMatrix)-1].index(cost)
            relevantRow = adjMatrix[connectedIndex]
            for i in range(len(relevantRow)-1):
                previousCost = adjMatrix[len(adjMatrix)-1][i]
                newPathCost = relevantRow[i] + relevantRow[len(adjMatrix)-1]
                adjMatrix[i][len(adjMatrix)-1] = min(previousCost, newPathCost)
                adjMatrix[len(adjMatrix)-1][i] = min(previousCost, newPathCost)

    return adjMatrix
