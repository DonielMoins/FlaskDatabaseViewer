# SET DB INFO HERE
db_settings = dict({"host": "localhost",
               "user": "root",
               "passwd": "",
               "port": 3306,
               "db_name": "test",
               "pool_name": "FlaskDatabaseviewer",
               "pool_size": 10})

verbose = bool(True)

connectionRetries = int(10) # Do not set too high so Flask doesnt crash.
retryTimeout = float(10.00) # Time in seconds.
maxConcurrentQueues = int(10) 
