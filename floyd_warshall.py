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
                        allKeys = [key for key in paths.keys() if key[0] == i+1 and key[-1] == currentNode+1]
                        # print(allKeys)
                        # for tup in allKeys:
                        #     prevValue = paths.get(tup)
                        #     print(f'{tup}: {prevValue}')
                        #     listTup = list(tup)
                        #     listTup.append(j+1)
                        #     addedValue = paths.get((currentNode+1, j+1), previousPathCost[currentNode][j])
                        #     print(f'{listTup}: {prevValue + addedValue}')
                        #     paths[tuple(listTup)] =  prevValue + addedValue
                        allNewPaths = [key for key in paths.keys() if key[0] == currentNode+1]
                        for tup in allKeys:
                            for nested_tup in allNewPaths:
                                set_tup = set(tup)
                                set_nested = set(nested_tup)
                                if len(set_tup.intersection(set_nested)) == 1:
                                    listtup = list(tup)
                                    listnested = list(nested_tup)
                                    listtup.extend(listnested[1:])
                                    if tuple(listtup) not in paths.keys():
                                        paths[tuple(listtup)] = paths.get(tuple(tup)) + paths.get(tuple(nested_tup))
                    tmp_matrix.append(min(presentEdge, newCost))
            newPathCost.append(tmp_matrix)
        previousPathCost = newPathCost
        newPathCost = []

    # subset difference of 1 node to be added if source and destination node the same

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