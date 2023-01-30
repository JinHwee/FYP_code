from dev_incremental_approach import *
import math, copy

adjM = [
    [math.inf, 13, 40, math.inf],
    [13, math.inf, 16, math.inf],
    [40, 16, math.inf, 5],
    [math.inf, math.inf, 5, math.inf]
]
adjNewNode = [math.inf, 2, math.inf, math.inf, math.inf]            # new node with one edge added
adjNewNode_Two = [math.inf, 2, math.inf, 3, math.inf]               # new node with two edge added
adjNewNode_Three = [math.inf, 2, 5, 3, math.inf]               # new node with three edge added

copyAdjM = copy.deepcopy(adjM)
apsp_matrix = floyd_warshall(copyAdjM)
print("APSP Matrix:")
for cost in apsp_matrix:
    print('\t', cost)

print('\n\nAdding new node with 1 edge')
print("APSP Matrix:")
copyAdjNewNode = copy.deepcopy(adjNewNode)
copyAPSP_matrix = copy.deepcopy(apsp_matrix)
newMatrix = add_new_node(copyAPSP_matrix, copyAdjNewNode)
for cost in newMatrix:
    print('\t', cost)

checkerAdjM = [
    [math.inf, 13, 40, math.inf, math.inf],
    [13, math.inf, 16, math.inf, 2],
    [40, 16, math.inf, 5, math.inf],
    [math.inf, math.inf, 5, math.inf, math.inf],
    [math.inf, 2, math.inf, math.inf, math.inf] 
]
floyd_warshall_checker(checkerAdjM)

print('\n\nAdding new node with 2 edges')
print("APSP Matrix:")
copyAPSP_matrix = copy.deepcopy(apsp_matrix)
copyAdjNewNode_two = copy.deepcopy(adjNewNode_Two)
results = add_new_node(copyAPSP_matrix, copyAdjNewNode_two)
for cost in results:
    print('\t', cost)

checkerAdjM = [
    [math.inf, 13, 40, math.inf, math.inf],
    [13, math.inf, 16, math.inf, 2],
    [40, 16, math.inf, 5, math.inf],
    [math.inf, math.inf, 5, math.inf, 3],
    [math.inf, 2, math.inf, 3, math.inf] 
]
floyd_warshall_checker(checkerAdjM)

print('\n\nAdding new node with 3 edges')
print("APSP Matrix:")
copyAPSP_matrix = copy.deepcopy(apsp_matrix)
copyAdjNewNode_three = copy.deepcopy(adjNewNode_Three)
results = add_new_node(copyAPSP_matrix, copyAdjNewNode_three)
for cost in results:
    print('\t', cost)

checkerAdjM = [
    [math.inf, 13, 40, math.inf, math.inf],
    [13, math.inf, 16, math.inf, 2],
    [40, 16, math.inf, 5, 5],
    [math.inf, math.inf, 5, math.inf, 3],
    [math.inf, 2, 5, 3, math.inf] 
]
floyd_warshall_checker(checkerAdjM)

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