import os, time
import zmq
import zmq_helper
import json, joblib
import ast
import training, inference
from customObject import CustomObject
from multiprocessing import Queue, Process
from threading import Lock, Thread

class Node:
    """A peer-to-peer node that can act as client or server at each round"""

    def __init__(self, context, node_id, peers):

        self.idle_status = True         # True if vertex is idle, False if otherwise
        self.status_lock = Lock()       # Mutex lock to prevent race conditions
        self.model_queue = Queue()      # Queue to hold/store models when vertex receives a new model 
        self.ready_queue = Queue()      # Queue that holds model that are ready for training or sending
        self.terminate_thread = False

        self.context = context
        self.node_id = node_id
        self.peers = peers
        self.log_prefix = "[" + str(node_id).upper() + "] "
        self.in_connection = None
        self.out_connection = {}
        self.local_model = None  # local model
        self.local_history = None
        self.initialize_node()

    def initialize_node(self):
        """Creates one zmq.ROUTER socket as incoming connection and n number
        of zmq.DEALER sockets as outgoing connections as per adjacency matrix"""
        self.local_history = []
        self.in_connection = zmq_helper.act_as_server(self.context, self.node_id)
        if len(self.peers) > 0:
            for server_id in self.peers :
                self.out_connection[server_id] = zmq_helper.act_as_client(self.context, server_id, self.node_id)

    def print_node_details(self):
        print("*" * 60)
        print("%s Node ID = %s" % (self.log_prefix, self.node_id))
        print("%s Peer IDs = %s %s" % (self.log_prefix, type(self.peers), self.peers))
        print("%s Context = %s" % (self.log_prefix, self.context))
        print("%s Incoming Connection = %s" % (self.log_prefix, self.in_connection))
        print("%s Outgoing Connections = %s" % (self.log_prefix, self.out_connection))
        print("%s History = %s" % (self.log_prefix, self.local_history))
        print("*" * 60)

    def save_model(self):
        model_filename = "/usr/thisdocker/dataset/" + str(self.node_id) + ".pkl"
        joblib.dump(self.local_model, model_filename)

    def load_prev_model(self):
        model_filename = "/usr/thisdocker/dataset/" + str(self.node_id) + ".pkl"
        self.local_model = joblib.load(model_filename)

    # might have to modify this portion of code to reflect sending model without train flag; because if no training occurs, then 
    # local model will not store that particular model
    def send_model(self, to_node, to_be_send=None):
        try:
            if to_be_send is None:
                zmq_helper.send_zipped_pickle(self.out_connection[to_node], self.local_model)
            else:
                # self.local_model = to_be_send
                zmq_helper.send_zipped_pickle(self.out_connection[to_node], to_be_send)
            # self.out_connection[to_node].send_string(self.local_model)
        except Exception as e:
            print("%sERROR establishing socket for to-node" % self.log_prefix)

    def receive_model(self, sourceNode):

        # while not self.status_lock.acquire(timeout=1):
        #     pass
        from_node = self.in_connection.recv(0)  # Reads identity

        # if self.idle_status:
        #     self.local_model = zmq_helper.recv_zipped_pickle(self.in_connection)  # Reads model object
        #     self.idle_status = False
        #     # self.local_model = self.in_connection.recv_string()
        # else:
        model = zmq_helper.recv_zipped_pickle(self.in_connection)
        createdObject = CustomObject(sourceNode, model)
        self.model_queue.put(createdObject)
        print(f"After receiving model, length of model queue: {self.model_queue.qsize()}")
        # self.status_lock.release()
        time.sleep(5)
        return from_node

    def training_step(self, step):
        # local model training
        build_flag = True if step == 1 else False
        self.local_model = training.local_training(self.node_id, self.local_model, build_flag)
        # self.local_model = {"from": self.node_id}  # for debugging
        # self.save_model()

    def inference_step(self):
        inference.eval_on_test_set(self.local_model)
        while not self.status_lock.acquire(timeout=1):
            pass
        self.idle_status = True
        self.status_lock.release()

    # need to refactor for double queue implementation
    def last_round_training(self, iteration):
        print("Last round training...")
        for _ in range(self.model_queue.qsize()):
            object = self.model_queue.get()
            self.local_model = object.MLModel
            self.training_step(iteration)
            self.inference_step()
    
    def terminating_thread(self):
        self.terminate_thread = True

    # need to revamp for double queue implementation
    def parallel_thread(self):
        while True:
            for _ in range(self.ready_queue.qsize()):
                object = self.ready_queue.get()
                valid = object.return_all_4_values()
                no_training_valid = object.return_for_no_training()

                while not self.status_lock.acquire(timeout=2):
                    pass
                idleState = self.idle_status
                self.status_lock.release()

                print("From parallel thread...")
                # object.print_object_details()
                if valid and idleState and object.trainingFlag:
                    while not self.status_lock.acquire(timeout=2):
                        pass
                    self.idle_status = False
                    self.status_lock.release()
                    training_start = time.process_time()
                    self.local_model = object.MLModel
                    self.training_step(2)
                    self.inference_step()
                    # print("%sTime : Training Step = %s" % (self.log_prefix, str(time.process_time() - training_start)))

                    print("%sSending model from %s to %s" % (self.log_prefix, self.node_id, object.destinationNode))
                    self.send_model(object.destinationNode)
                # if training flag is set to false, meaning no training will be done. This meant that the model must be sent to the destination node instead of putting back into the queue
                elif no_training_valid and self.idle_status and not object.trainingFlag:
                    print("%sSending model from %s to %s" % (self.log_prefix, self.node_id, object.destinationNode))
                    self.send_model(object.destinationNode, object.MLModel)
                else:
                    self.ready_queue.put(object)
                    print(f"Adding back to queue; The current size of the ready queue: {self.ready_queue.qsize()}")

def main():
    """main function"""
    context = zmq.Context()  # We should only have 1 context which creates any number of sockets
    node_id = os.environ["ORIGIN"]
    peers_list = ast.literal_eval(os.environ["PEERS"])
    this_node = Node(context, node_id, peers_list)

    allocationThread = Thread(target=this_node.parallel_thread)
    allocationThread.start()

    # Read comm template config file
    comm_template = json.load(open('comm_template.json'))
    total_rounds = len(comm_template.keys())

    for i in range(1, total_rounds + 2):
        if i == total_rounds+1:
            # last round training must be modified.
            print(f"Current size of model queue = {this_node.model_queue.qsize()}")
            print(f"Current size of ready queue = {this_node.ready_queue.qsize()}")
            for list_item_id in range(len(comm_template[str(total_rounds)])):
                if this_node.node_id == "node"+str(comm_template[str(total_rounds)][list_item_id]["to"]):
                    # Last node training
                    # if training_flag:
                    # this_node.training_step(i)
                    # # Global accuracy
                    # this_node.inference_step()
                    print("This is the last round, commencing last round training...")
                    this_node.last_round_training(i)
        else :
            for list_item_id in range(len(comm_template[str(i)])):
                i_minus_1 = comm_template[str(i-1)][list_item_id] if i > 1 else None
                i_minus_1_source = "node" + str(i_minus_1['from']) if i_minus_1 is not None else None
                ith_round = comm_template[str(i)][list_item_id]
                training_flag = bool(ith_round['train'])
                from_node = "node" + str(ith_round["from"])
                to_node = "node" + str(ith_round["to"])

                if node_id == from_node:
                    if i == 1:
                        training_start = time.process_time()
                        this_node.training_step(i)
                        print("%sTime : Training Step = %s" % (this_node.log_prefix, str(time.process_time() - training_start)))
                        print("%sSending iteration %s from %s to %s" % (this_node.log_prefix, str(i), from_node, to_node))
                        this_node.send_model(to_node)
                        # sleep(2)
                    else:
                        # adding a 5 seconds sleep timer to factor in possibility that the queue is not updated immediately, but with delay
                        # sleep(2)
                        queue_size = this_node.model_queue.qsize()
                        # sleep(2)
                        # This node is dealer and receiving node is router
#                        for id in range(this_node.model_queue.qsize()):
#                            object = this_node.model_queue.get()
#                            sourceNode = object.retrieveInformation_ith()
#                            print(f"Checking... {sourceNode}, {i_minus_1_source}")
#                            if sourceNode == i_minus_1_source:
#                                object.update_object(to_node, training_flag)
#                                object.print_object_details()
#                            this_node.model_queue.put(object)
                            # if updated:
                            #     this_node.local_model = identifiedObject.MLModel

                        # after each iteration, the model should be already in the storage queue, waiting to be processed
                        updated = False
                        for _ in range(queue_size):
                            object = this_node.model_queue.get()
                            sourceNode = object.retrieveInformation_ith()
                            if sourceNode == i_minus_1_source:
                                print("The current object has been updated!\n")
                                updated = True
                                object.update_object(to_node, training_flag)

                            if updated:
                                print("Updating the ready queue")
                                updated = False
                                this_node.ready_queue.put(object)
                            else:
                                print("No updates; adding back to the model queue")
                                this_node.model_queue.put(object)
                            object.print_object_details()
                    
                elif node_id == to_node:
                    # This node is router and sending node is dealer
                    rcvd_from = this_node.receive_model(from_node)
                    # print("%sReceived object %s at iteration %s" % (this_node.log_prefix, str(this_node.local_model), str(i)))
                    this_node.save_model()

                    # Logging iteration and prev_node for audit
                    this_node.local_history.append({"iteration":i, "prev_node":rcvd_from.decode("utf-8")})

    # this_node.terminating_thread()
    # allocationThread.join()

if __name__ == "__main__":
    main()
