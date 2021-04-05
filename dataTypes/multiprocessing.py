from multiprocessing.synchronize import Event
from multiprocessing.managers import Namespace, SyncManager, NamespaceProxy, DictProxy

class DataCouple:
    def __init__(self, namespace: Namespace, event: Event):
        self.namespace = namespace
        self.event = event
        # super(DataCouple, self).__init__(namespace, event)
    
    