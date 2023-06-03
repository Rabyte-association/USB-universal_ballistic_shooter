import multiprocessing

def increment(queue):
    tmp = 0
    while True:
        tmp += 1
        queue.put(tmp)

def printer(queue):
    while True:
        val = queue.get()
        print(val)

if __name__ == '__main__':
    queue = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=increment, args=(queue,))
    p2 = multiprocessing.Process(target=printer, args=(queue,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()