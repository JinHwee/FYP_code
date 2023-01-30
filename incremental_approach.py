import math, copy

def floyd_warshall_checker(matrix):
    for k in range(len(matrix)):
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if i == j:
                    matrix[i][j] = 0
                else:
                    matrix[i][j] = min(matrix[i][j], matrix[i][k] + matrix[k][j])
    
    print("\nAPSP Matrix Checker:")
    for cost in matrix:
        print('\t', cost)

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

adjM = [
    [math.inf, 13, 40, math.inf],
    [13, math.inf, 16, math.inf],
    [40, 16, math.inf, 5],
    [math.inf, math.inf, 5, math.inf]
]
adjNewNode = [math.inf, 2, math.inf, math.inf, math.inf]            # new node with one edge added
adjNewNode_Two = [math.inf, 2, math.inf, 3, math.inf]               # new node with two edge added
adjNewNode_Three = [math.inf, 2, 5, 3, math.inf]               # new node with three edge added

# copyAdjM = copy.deepcopy(adjM)
# apsp_matrix = floyd_warshall(copyAdjM)
# print("APSP Matrix:")
# for cost in apsp_matrix:
#     print('\t', cost)

# print('\n\nAdding new node with 1 edge')
# print("APSP Matrix:")
# copyAdjNewNode = copy.deepcopy(adjNewNode)
# copyAPSP_matrix = copy.deepcopy(apsp_matrix)
# newMatrix = add_new_node(copyAPSP_matrix, copyAdjNewNode)
# for cost in newMatrix:
#     print('\t', cost)

# checkerAdjM = [
#     [math.inf, 13, 40, math.inf, math.inf],
#     [13, math.inf, 16, math.inf, 2],
#     [40, 16, math.inf, 5, math.inf],
#     [math.inf, math.inf, 5, math.inf, math.inf],
#     [math.inf, 2, math.inf, math.inf, math.inf] 
# ]
# floyd_warshall_checker(checkerAdjM)

# print('\n\nAdding new node with 2 edges')
# print("APSP Matrix:")
# copyAPSP_matrix = copy.deepcopy(apsp_matrix)
# copyAdjNewNode_two = copy.deepcopy(adjNewNode_Two)
# results = add_new_node(copyAPSP_matrix, copyAdjNewNode_two)
# for cost in results:
#     print('\t', cost)

# checkerAdjM = [
#     [math.inf, 13, 40, math.inf, math.inf],
#     [13, math.inf, 16, math.inf, 2],
#     [40, 16, math.inf, 5, math.inf],
#     [math.inf, math.inf, 5, math.inf, 3],
#     [math.inf, 2, math.inf, 3, math.inf] 
# ]
# floyd_warshall_checker(checkerAdjM)

# print('\n\nAdding new node with 3 edges')
# print("APSP Matrix:")
# copyAPSP_matrix = copy.deepcopy(apsp_matrix)
# copyAdjNewNode_three = copy.deepcopy(adjNewNode_Three)
# results = add_new_node(copyAPSP_matrix, copyAdjNewNode_three)
# for cost in results:
#     print('\t', cost)

# checkerAdjM = [
#     [math.inf, 13, 40, math.inf, math.inf],
#     [13, math.inf, 16, math.inf, 2],
#     [40, 16, math.inf, 5, 5],
#     [math.inf, math.inf, 5, math.inf, 3],
#     [math.inf, 2, 5, 3, math.inf] 
# ]
# floyd_warshall_checker(checkerAdjM)

complicatedGraph = [
       [math.inf, 82, 15, math.inf, math.inf, math.inf, math.inf],
       [82,      math.inf,     4,       math.inf,     math.inf,     math.inf, math.inf],
       [15,      4,       math.inf,     95,      math.inf,     36,      32],
       [math.inf,     math.inf,     95,      math.inf,     29,      math.inf, math.inf],
       [math.inf,     math.inf,     math.inf,     29,      math.inf,     18, math.inf],
       [math.inf,     math.inf,     36,      math.inf,     18, math.inf, 95],
       [math.inf,     math.inf,     32,      math.inf,     math.inf, 95, math.inf],
]
newNode = [87,      95,      70,     12,     math.inf,     math.inf,     math.inf,     math.inf]

apsp_matrix = floyd_warshall(complicatedGraph)
copyAPSP = copy.deepcopy(apsp_matrix)
results = add_new_node(copyAPSP, newNode)
print("\nAPSP for initialized graph:")
for cost in apsp_matrix:
    print('\t', cost)
print("\nOne new node added")
for cost in results:
    print('\t', cost)

fullAdjM = [
       [math.inf,     82,      15,      math.inf,     math.inf,     math.inf,     math.inf, 87],
       [82,      math.inf,     4,       math.inf,     math.inf,     math.inf,     math.inf, 95],
       [15,      4,       math.inf,     95,      math.inf,     36,      32, 70],
       [math.inf,     math.inf,     95,      math.inf,     29,      math.inf,     math.inf, 12],
       [math.inf,     math.inf,     math.inf,     29,      math.inf,     18,      math.inf, math.inf],
       [math.inf,     math.inf,     36,      math.inf,     18,      math.inf,     95, math.inf],
       [math.inf,     math.inf,     32,      math.inf,     math.inf,     95,      math.inf, math.inf],
       [87,      95,      70,     12,     math.inf,     math.inf,     math.inf,     math.inf]
]
floyd_warshall_checker(fullAdjM)