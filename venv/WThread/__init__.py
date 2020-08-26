import threading,websockets,Building,Custom
class WThread(threading.Thread):

    _callback = None
    _data = {}

    def __init__(self, callback, data:dict):
        threading.Thread.__init__(self)
        self._callback = callback;
        self._data = data

    def run(self):
        if hasattr(self._callback, '__call__'):
            self._callback(self._data)

