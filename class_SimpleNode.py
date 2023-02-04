class SimpleNode:

    def __init__(self, id, data, NodeObjective) -> None:
        self.id = id
        self.data = data
        self.NodeObective = NodeObjective

    def output_information(self):
        print(f'Current id:', self.id, '\nCurrent objective:', self.NodeObective, '\nCurrent data:', self.data, '\n')

    # Getter and Setter Methods
    def get_node_id(self):
        return self.id

    def get_data(self):
        return self.data
    
    def update_data(self, data):
        self.data = data

    def get_node_objective(self):
        return self.NodeObective

    def update_node_objective(self, newNodeObjective):
        self.NodeObective = newNodeObjective