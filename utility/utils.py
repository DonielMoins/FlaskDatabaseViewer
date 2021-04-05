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
    
