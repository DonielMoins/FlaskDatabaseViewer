from multiprocessing import shared_memory
import multiprocessing
class SharedMemory(shared_memory.SharedMemory):
    def __init__(self, name=None, create=False, size=0):
        
        super().__init__(name=name, create=create, size=size)
        