from dataTypes.db_info import DB_INFO
from mariadb import ConnectionPool
from helper.db_helper import MakeConnectionPool


class VarsClass:

    def __init__(self, db_Info: DB_INFO = DB_INFO(),
                 connectionPool: ConnectionPool = None):
        self.db_Info = db_Info
        self.connectionPool = connectionPool \
            if isinstance(connectionPool, ConnectionPool) \
            else MakeConnectionPool(self.db_Info)




# sharedMemoryRefs = [db_Info, db_Conn_Pool]

# def setupVars():
#     pass



# def cleanup():
#     for ref in sharedMemoryRefs:
#         ref._mmap
#         ref.close()
#         ref.unlink()
#     smm._finalize_manager()
# atexit.register(cleanup)
