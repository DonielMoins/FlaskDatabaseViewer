from config import retryTimeout, connectionRetries, maxConcurrentQueues
from threading import *
import threading
from exceptions.TooManyRetries import TooManyRetriesException

from queue import Queue, Empty, Full

# Search for Dictionary in list of arguments
def searchForDict(*kwargs):
    if any(isinstance(argument, dict) for argument in kwargs):
        # for x in kwargs if
        argumentsDict = (arg for arg in kwargs if isinstance(arg, dict))
        searchForDict(next(argumentsDict))

# Debug function
def listDicRec(lev = 0, data = None):
    print("\n") 
    if data.values() is not None:
        for i in data:    
            if isinstance(i, list):
                print((lev*"\t") + i+":",),
                listDicRec(lev+1, i)
            else:
                print((lev*"\t"),f"{i}:\t{data[i]}")
    print("\n")           
    print("DONE")
    
# Need to manage how many tried and howmany retry Queues are running
# TODO: Set up process that manages db using a process with threads to talk in between
def retry(method, retries=connectionRetries, timeout=retryTimeout, *args=None, **kwargs=None):
    return None
    
    
# def startRetry(namespaces, accessEvents, method, retries=connectionRetries, timeout=retryTimeout, *args=None, **kwargs=None):
#     if isinstance(gVars.retryDeamon, None):
#         multiprocessing.Value()    
    

# def retrySpawn(method, retries=connectionRetries, timeout=retryTimeout, *args=None, **kwargs=None):
#     que = Queue(retries)
#     lock = Lock()
    
#     # with lock:
#     #     for times in range(retries):
#     #         timer = ReturnTimer(timeout, method, args.append(que), kwargs)
#     #         que.put_nowait(timer) 
        
#     #     while not que.empty:
#     #         try:
#     #             return que.get_nowait()
#     #         except Empty:
#     #             break
#     # raise TooManyRetriesException(retries)

# def retryDeamon():
#     while len(gVars.queuesRunning) < maxConcurrentQueues:
#         pass