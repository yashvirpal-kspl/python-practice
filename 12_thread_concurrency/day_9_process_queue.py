from multiprocessing import Process, Queue
import time


def prepare_chai(queue):
    queue.put("Masala chai is ready")
  
if __name__ == "__main__":
    start = time.time()
    queue = Queue()
    processes = Process(target=prepare_chai, args = (queue,))

    processes.start()
    processes.join() 


    end = time.time()

    print(queue.get())
    print(f"Time taken: {end - start:.2f} seconds")
    