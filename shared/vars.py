from dataTypes.SharedMemory import SharedMemory
from multiprocessing.managers import SharedMemoryManager


from helper.db_helper import DB_INFO, ConnectionPool
import atexit



smm = SharedMemoryManager()
smm.start()

    

# Database Info
db_Info         = smm.SharedMemory(size=32)
db_Conn_Pool    = smm.SharedMemory(size=256)



# Threading, Queues
    
queuesRunning    = {}
dbDeamon         = None

sharedMemoryRefs = [db_Info, db_Conn_Pool]

atexit.register(cleanup)
def cleanup():
    for ref in sharedMemoryRefs:
        ref._mmap
        ref.close()
        ref.unlink()
    smm._finalize_manager()
