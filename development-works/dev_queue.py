from time import sleep
from multiprocessing import Queue
from threading import Thread, Lock
from random import randint

data_queue = Queue()

idle_state = True
idle_state_lock = Lock()

def main_function():
    global idle_state, idle_state_lock
    while True:
        idle_state_lock.acquire()
        checker = randint(0, 101)
        idle_state = False if checker < 50 else True
        result = retrieving_data()
        # sleep(3)
        for i in range(10):
            print("A")
        idle_state_lock.release()
        # sleep(3)
        if result != "ERROR":
            print("\n\t\tThe current data passed to the function is %d\n" % result)

def adding_data():
    global idle_state, idle_state_lock
    while True:
        data = randint(1, 101)
        print(f"Adding {data} to queue")
        data_queue.put(data)
        sleep(4)

def adding_data2():
    global idle_state, idle_state_lock
    while True:
        data = randint(1, 101)
        print(f"Adding {data} to queue")
        data_queue.put(data)
        sleep(5)

def retrieving_data():
    while True:
        if not data_queue.empty():
            data = data_queue.get()
            print(f"Current data removed: {data}")
            return data
        else:
            print("\n\t\tThere is nothing to be removed for now... exiting...!\n")
            return "ERROR"

if __name__ == "__main__":
    queue_thread = Thread(target=adding_data)
    queue_thread2 = Thread(target=adding_data2)
    scheduler_thread = Thread(target=main_function)

    queue_thread.start()
    queue_thread2.start()
    scheduler_thread.start()
