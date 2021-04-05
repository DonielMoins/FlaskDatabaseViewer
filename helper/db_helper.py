import config
import mariadb
from mariadb import ConnectionPool
from dataTypes.db_info import DB_INFO

# from utility.utils.

# Gives you a fresh connection
            

def GetConnection(db_Info: DB_INFO, connection_pool: ConnectionPool):
    try:
        # Does pool respond/exist?
        if connection_pool:
            return connection_pool.get_connection()
        else:
            # Creating pool
            connection_pool = MakeConnectionPool(db_Info)
            print("Creating Connection Pool!")
            if connection_pool:
                return GetConnection(db_Info, connection_pool)
            else:
                try:
                    # Let it throw the error
                    GetConnection(db_Info, connection_pool)
                except Exception as e:
                    if config.verbose:
                        print("Connection:", e)
                    else:
                        print(
                            "Connection: Cannot create connection! Check if pool is dead")
    except mariadb.PoolError as e:
        # Check if DB has died since last query.
        if issubclass(e, AttributeError) and "cursor" in str(e):
            print("Connection to MariaDB service dead, resetting pool.")
            
            
            connection_pool = MakeConnectionPool(db_Info)
            if connection_pool:
                conn = GetConnection(db_Info, connection_pool)
                print("Checking if connection is pingable")
                if conn.ping():
                    return conn
            else:
                print()

        print(f"Error opening connection from pool: {e}")
    except Exception as e:
        print(e)


def MakeConnectionPool(db_info: DB_INFO) -> mariadb.ConnectionPool:
    try:
        db_conn_pool = mariadb.ConnectionPool(
            user=db_info.user,
            password=db_info.passwd,
            host=db_info.host,
            port=db_info.port,
            pool_name=db_info.pool_name,
            pool_size=db_info.pool_size
        )
        return db_conn_pool
    except mariadb.OperationalError as e:
        if "Access denied" in str(e):
            raise mariadb.Error()
    except mariadb.Error as e:
        print(f"Making Connection Pool failed with error: \n{e}\n type: {type(e)}")

# Unused
def checkConn(self):
    sq = "SELECT NOW()"
    try:
        self.cur.execute(sq)
    except mariadb.Error as e:
        if e.errno == 2006:
            return self.connect()
        else:
            print("No connection with database.")
            return False
