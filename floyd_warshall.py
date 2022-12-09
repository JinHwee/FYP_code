import math

def all_pair_shortest_path(matrix):
    # pathCostMatrix [
    #    1   2   ...     n
    # 1 [inf, x, ...     y]
    # 2 [x, inf, ...     z]
    # ]
    # pathCostMatrix[i][j] = pathCostMatrix[row][column]
    previousPathCost = matrix          # initilisation of matrix
    newPathCost = []

    for currentNode in range(len(matrix)):
        for i in range(len(matrix)):
            tmp_matrix = []
            for j in range(len(matrix)):
                if i == j:
                    tmp_matrix.append(0)
                else:
                    presentEdge = previousPathCost[i][j]
                    newCost = previousPathCost[i][currentNode] + previousPathCost[currentNode][j]
                    tmp_matrix.append(min(presentEdge, newCost))
            newPathCost.append(tmp_matrix)
        previousPathCost = newPathCost
        newPathCost = []
    
    return previousPathCost