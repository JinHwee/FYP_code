import math, copy

def all_pair_shortest_path(matrix):
    # pathCostMatrix [
    #    1   2   ...     n
    # 1 [inf, x, ...     y]
    # 2 [x, inf, ...     z]
    # ]
    # pathCostMatrix[i][j] = pathCostMatrix[row][column]
    previousPathCost = copy.deepcopy(matrix)          # initilisation of matrix
    newPathCost = []

    paths = {}
    counter = 0
    for currentNode in range(len(matrix)):
        for i in range(len(matrix)):
            tmp_matrix = []
            for j in range(len(matrix)):
                if i == j:
                    tmp_matrix.append(0)
                else:
                    presentEdge = previousPathCost[i][j]
                    newCost = previousPathCost[i][currentNode] + previousPathCost[currentNode][j]
                    if counter < len(matrix) ** 2 and presentEdge < math.inf:
                        # stores the direct edges between 2 distinct vertices
                        paths[(i+1, j+1)] = presentEdge
                    counter += 1
                    # key[0] is the source node, key[-1] is the last added node
                    if newCost < math.inf and newCost < presentEdge:
                        allDetectedPaths = [key for key in paths.keys() if key[0] == i+1 and key[-1] == currentNode+1]
                        additionalPaths = [key for key in paths.keys() if key[0] == currentNode+1]
                        for basePath in allDetectedPaths:
                            for pathToBeMerged in additionalPaths:
                                setBasePath = set(basePath)
                                setPathToBeMerged = set(pathToBeMerged)
                                # ensures that only the destination from first set is the common vertex between the 2 sets
                                if len(setBasePath.intersection(setPathToBeMerged)) == 1:
                                    listBasePath = list(basePath)
                                    listPathToBeMerged = list(pathToBeMerged)
                                    listBasePath.extend(listPathToBeMerged[1:])
                                    if tuple(listBasePath) not in paths.keys():
                                        paths[tuple(listBasePath)] = paths.get(tuple(basePath)) + paths.get(tuple(pathToBeMerged))
                    tmp_matrix.append(min(presentEdge, newCost))
            newPathCost.append(tmp_matrix)
        previousPathCost = newPathCost
        newPathCost = []
        
    return previousPathCost, paths

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
        print(cost)