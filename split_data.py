import numpy as np
import random
import os
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from matplotlib import pyplot as plt
import torch
import torchvision
import cv2, fnmatch
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array

train_data = torchvision.datasets.ImageFolder('nuimages/train')
all_classes = train_data.classes

def load_dataset(folderName):
    dirPath = os.path.join('./nuimages/train', folderName)
    directorySize = len(fnmatch.filter(os.listdir(dirPath), '*.jpg'))
    image_array = []
    for fileName in os.listdir(dirPath):
        img = cv2.imread(os.path.join(dirPath, fileName))
        img = cv2.resize(img, dsize=(32, 32))
        image_array.append(img)
    trainX = np.asarray(image_array)
    tmp_trainY = [all_classes.index(folderName) for i in range(directorySize)]
    trainY = np.reshape(tmp_trainY, (len(tmp_trainY), 1))

    testDirPath = os.path.join('./nuimages/val', folderName)
    directorySize = len(fnmatch.filter(os.listdir(testDirPath), '*.jpg'))
    test_array = []
    for fileName in os.listdir(testDirPath):
        img = cv2.imread(os.path.join(testDirPath, fileName))
        img = cv2.resize(img, dsize=(32, 32))
        test_array.append(img)

    testX = np.asarray(test_array)
    tmp_testY = [all_classes.index(folderName) for i in range(directorySize)]
    testY = np.reshape(tmp_testY, (len(tmp_testY), 1))

    trainY = to_categorical(trainY)
    testY = to_categorical(testY)
    return trainX, trainY, testX, testY

def prep_pixels(train, test):
    # convert from integers to floats
    train_norm = train.astype('float32')
    test_norm = test.astype('float32')
    # normalize to range 0-1
    train_norm = train_norm / 255.0
    test_norm = test_norm / 255.0
    # return normalized images
    return train_norm, test_norm


def create_clients(image_list, label_list, num_clients=10, initial='clients'):
    random.seed(42)
    # create a list of client names
    client_names = ['{}_{}'.format(initial, i + 1) for i in range(num_clients)]

    # randomize the data
    data = list(zip(image_list, label_list))
    random.shuffle(data)

    # shard data and place at each client
    size = len(data) // num_clients
    shards = [data[i:i + size] for i in range(0, size * num_clients, size)]

    # number of clients must equal number of shards
    assert (len(shards) == len(client_names))

    return {client_names[i]: shards[i] for i in range(len(client_names))}


def batch_data(data_shard, bs=32):
    '''Takes in a clients data shard and create a tfds object off it
    args:
        shard: a data, label constituting a client's data shard
        bs:batch size
    return:
        tfds object'''
    # seperate shard into data and labels lists
    data, label = zip(*data_shard)
    dataset = tf.data.Dataset.from_tensor_slices((list(data), list(label)))
    return dataset.shuffle(len(label)).batch(bs)

def create_and_save_clients(folderName, num_clients=10):
    X_train, y_train, X_test, y_test = load_dataset(folderName)
    X_train, X_test = prep_pixels(X_train, X_test)
    clients = create_clients(X_train, y_train,  num_clients=num_clients, initial='client')

    basepath = os.path.join(os.getcwd(), "all_data")
    os.makedirs(basepath, 0o777, exist_ok=True)
    currentData = len([i for i in list(os.listdir(basepath)) if i != "saved_data_test"])
    # process and batch the training data for each client
    clients_batched = dict()
    for (client_name, data) in clients.items():
        clients_batched[client_name] = batch_data(data)
        # print(type(clients_batched[client_name]), len(clients_batched[client_name]))
        # saving the dataset to disk
        if currentData != 0:
            client_id = int(client_name[client_name.index("_")+1:])
            new_name = client_name[:-1] + str(client_id+currentData)
            client_filename = "saved_data_" + new_name
        else:
            client_filename = "saved_data_" + client_name
        client_path = os.path.join(basepath, client_filename)
        tf.data.experimental.save(clients_batched[client_name], client_path)
    # print(clients_batched)

    # process and batch the test set
    test_batched = tf.data.Dataset.from_tensor_slices((X_test, y_test)).batch(len(y_test))
    # print(type(test_batched), len(test_batched))
    client_filename = "saved_data_test"
    client_path = os.path.join(basepath, client_filename)
    tf.data.experimental.save(test_batched, client_path)

if __name__ == "__main__":
    random.seed(42)
    create_and_save_clients('pedestrian', 3)
    create_and_save_clients('vehicle.truck', 4)