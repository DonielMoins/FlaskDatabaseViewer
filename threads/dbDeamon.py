from threading import Thread
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

def dbVerificationDeamon(this: Thread):
    while True:
        this.getName()