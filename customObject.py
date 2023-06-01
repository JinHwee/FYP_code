from time import sleep
from random import randint

class CustomObject():

    # initialized when vertex receives a model in the ith iteration
    def __init__(self, sourceNode, MLModel) -> None:
        print("\nInitialized one CustomObject!\n")
        self.sourceNode = sourceNode    # information available to the vertex at the ith iteration
        self.MLModel = MLModel          # information available to the vertex at the ith iteration
        self.destinationNode = None # to be added in the next iteration, i+1
        self.trainingFlag = None    # to be added in the next iteration, i+1

    # updates the object in the (i+1)th round with more information that is not available in the ith round
    def update_object(self, destinationNode, trainingFlag):
        self.destinationNode = destinationNode
        self.trainingFlag = trainingFlag
        print(f"\nSource: {self.sourceNode}, Destination: {self.destinationNode}")
        
    def retrieveInformation_ith(self):
        return self.sourceNode

    def return_all_4_values(self):
        return all((self.sourceNode, self.MLModel, self.destinationNode, self.trainingFlag))

    def return_for_no_training(self):
        return all((self.sourceNode, self.MLModel, self.destinationNode))

    def print_object_details(self):
        print(f"\nCurrent object instance has the following details")
        print(f"Source node: {self.sourceNode}")
        print(f"Destination node: {self.destinationNode}")
        print(f"Model saved: {self.MLModel}")
        print(f"Training flag: {self.trainingFlag}\n")
