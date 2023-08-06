from torchelper.events.event import Event
from torchelper.events.receiver import Receiver
from threading import Lock

lock = Lock()
__event_map__ = {}

class EventCenter:
    def __init__(self):
        pass
    
    @staticmethod
    def register(evt_type:str, rcver:Receiver):
        lock.acquire()
        global __event_map__
        rcvers = __event_map__.get(evt_type, set())
        rcvers.add(rcver)
        __event_map__[evt_type] = rcvers
        lock.release()

    @staticmethod
    def __on_event(event:Event):
        lock.acquire()
        global __event_map__
        rcvers = __event_map__.get(event.evt_type, set())
        for rcver in rcvers:
            rcver.on_event(event)
        lock.release()

    @staticmethod
    def broadcast(event:Event):
        EventCenter.__on_event(event)
