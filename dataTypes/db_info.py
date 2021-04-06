from utility.utils import searchForDict as search


class DB_INFO:
    def __init__(self, info_dict: dict = None, **kwargs):
        if isinstance(info_dict, dict): 
            self.setargs(info_dict)
        elif len(kwargs) != 0:
            if any(isinstance(argument, dict) for argument in kwargs):
                self.setargs(search(kwargs))
        else:
            # If no arguments given, go to defaults.
            self.host = "localhost"
            self.user = "anonymous"
            self.passwd = ""
            self.port = 3306
            self.db_name = "db_name"
            self.pool_name = "pool_name"
            self.pool_size = 10
    
    def setargs(self, kwargs: dict):
        self.host = kwargs["host"]
        self.user = kwargs["user"]
        self.passwd = kwargs["passwd"]
        self.port = kwargs["port"]
        self.db_name = kwargs["db_name"]
        self.pool_name = kwargs["pool_name"]
        self.pool_size = kwargs["pool_size"]