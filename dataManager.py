# Store global variables to be used, idk about making them thread safe them yet.
# TODO: thread safe compatibility
import multiprocessing.managers
from mariadb import ConnectionPool
from dataTypes.db import DB_INFO
from dataTypes.multiprocessing import DataCouple

# def setupDBTypes():


def startDataManager(Manager: multiprocessing.managers.SyncManager):
    db_NM               = Manager.Namespace()
    db_accessEvent      = Manager.Event()
    
    # Database Info
    
    db_NM.db_Info         = Manager.Value(type(DB_INFO), DB_INFO())
    db_NM.db_Conn_Pool    = Manager.Value(type(ConnectionPool), None)
    # Threading, Queues, and Processes
    
    # queuesRunning       = manager.Array()
    # retryDeamon         = manager.Value(None)
    # namespaces          = Manager.dict({
    #                                     "db": [db_NM, db_accessEvent], 
    #                                                                     })
    with Manager.Lock():
        
        data = Manager.dict({"db":Manager.Value(DataCouple, DataCouple(db_NM, db_accessEvent))})
        return data
    
        # flaskClass          = Flask(data)
        # flaskApp            = multiprocessing.Process(name="FlaskApp", target=startFlask(data))

from multiprocessing import Process, JoinableQueue
import time

def reader_proc(queue):
    ## Read from the queue; this will be spawned as a separate Process
    while True:
        msg = queue.get()         # Read from the queue and do nothing
        queue.task_done()

def writer(count, queue):
    for ii in range(0, count):
        queue.put(ii)             # Write 'count' numbers into the queue

def startReaderProc():
    for count in [10**4, 10**5, 10**6]:
        jqueue = JoinableQueue() # writer() writes to jqueue from _this_ process
        # reader_proc() reads from jqueue as a different process...
        reader_p = Process(target=reader_proc, args=((jqueue),))
        reader_p.daemon = True
        reader_p.start()     # Launch the reader process
        _start = time.time()
        writer(count, jqueue) # Send a lot of stuff to reader_proc() (in different process)
        jqueue.join()         # Wait for the reader to finish
        print("Sending {0} numbers to JoinableQueue() took {1} seconds".format(count, 
            (time.time() - _start)))
        
# from dataManager import safeNamespace, safeNamespaceProxy


# class safeNamespaceProxy(NamespaceProxy):
#     def __init__(self, *args):
#         super(safeNamespaceProxy, self).__init__(*args)
        

# class safeNamespace(Namespace):
#     def __init__(self, *args):
#         super(safeNamespace, self).__init__(*args)
        


# SyncManager.register('safeNamespace', safeNamespace, safeNamespaceProxy)