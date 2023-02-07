import math, argparse, json, os
from class_SimpleGraph import *
from class_SimpleNode import *

INF = math.inf

G0 = [
    [INF, 82, 15, INF, INF, INF, INF],
    [82, INF, 4, INF, INF, INF, INF],
    [15, 4, INF, 95, INF, 36, 32],
    [INF, INF, 95, INF, 29, INF, INF],
    [INF, INF, INF, 29, INF, 18, INF, ],
    [INF, INF, 36, INF, 18, INF, 95],
    [INF, INF, 32, INF, INF, 95, INF]
]
nodeDictionary0 = {
    0: SimpleNode(0, None, 1.1),
    2: SimpleNode(2, None, 1.1),
    3: SimpleNode(3, None, 1.1),

    1: SimpleNode(1, None, 2.1),
    4: SimpleNode(4, None, 2.1),
    5: SimpleNode(5, None, 2.1),
    6: SimpleNode(6, None, 2.1)
}
adjMNode0 = [41, 78, INF, INF, INF, INF, INF, INF]

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
nodeDictionary1 = {}
adjMNode1 = [1, 9, 1, 4, 2, 6, 7, 8, 1, 9, 1, INF]

G2 = [
    [INF, 11, 21, 18, 18, 20], 
    [11, INF, 33, 41, 36, 17], 
    [21, 33, INF, 15, 24, 42], 
    [18, 41, 15, INF, 23, 36], 
    [18, 36, 24, 23, INF, 36], 
    [20, 17, 42, 36, 36, INF], 
]
nodeDictionary2 = {}
adjMNode2 = [5, 5, 8, 4, 8, 10, INF]

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
nodeDictionary3 = {}
adjMNode3 = [2, 10, 3, 10, 3, 8, 8, 5, INF]

def generate_paths(graphID, nodeToBeAdded, src, dest):
    if graphID == 0:
        adjM = G0
        nodeDictionary = nodeDictionary0
        if nodeToBeAdded:
            newNode = SimpleNode(len(adjM), None, '<To be allocated>')
            newNodeAdjM = adjMNode0
    elif graphID == 1:
        adjM = G1
        nodeDictionary = nodeDictionary1
        if nodeToBeAdded:
            newNode = SimpleNode(len(adjM), None, '<To be allocated>')
            newNodeAdjM = adjMNode1
    elif graphID == 2:
        adjM = G2
        nodeDictionary = nodeDictionary2
        if nodeToBeAdded:
            newNode = SimpleNode(len(adjM), None, '<To be allocated>')
            newNodeAdjM = adjMNode2
    else:
        adjM = G3
        nodeDictionary = nodeDictionary3
        if nodeToBeAdded:
            newNode = SimpleNode(len(adjM), None, '<To be allocated>')
            newNodeAdjM = adjMNode3
    
    graphInstance = SimpleGraph(nodeDictionary)
    graphInstance.calculate_APSP_matrix_using_Floyd_Warshall_algorithm(adjM)
    apsp_matrix = graphInstance.get_APSP_Matrix()

    if nodeToBeAdded:
        graphInstance.add_new_node(newNode, newNodeAdjM)
    
    order = []
    orderStrings = apsp_matrix[src][dest][2]
    for string in orderStrings:
        tmp_list = string.split(' -> ')
        for id in tmp_list:
            if int(id) not in order:
                order.append(int(id))

    train = []
    for id in order:
        if id == dest:
            continue
        train.append(nodeDictionary[int(id)].get_node_objective() == nodeDictionary[dest].get_node_objective())

    order_json = {}
    order = [i+1 for i in order]
    for ind, item in enumerate(order):
        try:
            order_json[str(ind+1)] = {"from": str(int(item)),
                                    "train": bool(train[ind]),
                                    "to": str(order[ind+1])
                                    }
        except IndexError as e:
            # Last item does not have a "to" node
            None

    if not any(train):
        try:
            os.remove("./peer/comm_template.json")
        except:
            "File removed"
    else:
        with open("./peer/comm_template.json", "w") as outfile:
            json.dump(order_json, outfile)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('graphID', type=int)
    parser.add_argument("-addNewNode", action='store_true')
    parser.add_argument("-src", type=int)
    parser.add_argument("-dest", type=int)
    args = parser.parse_args()
    generate_paths(args.graphID, args.addNewNode, args.src, args.dest)

