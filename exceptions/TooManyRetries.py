class TooManyRetriesException(Exception):
    """     Raised when when retry method has reached its limit of retries.     """
    
    def __init__(self, limit, message="Retry method has reached its end."):
        self.limit = limit
        self.message = message
        super().__init__(self.message)