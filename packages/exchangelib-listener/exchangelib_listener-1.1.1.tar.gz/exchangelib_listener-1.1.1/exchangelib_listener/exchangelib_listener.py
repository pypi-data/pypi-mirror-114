from exchangelib import Account
from exchangelib.properties import Event

class Listener:
    def __init__(self, account: Account):
        self._account = account
        self.streaming_events_received = self.__EventHandler()
        self.streaming_event_received = self.__EventHandler()
    
    def __get_single_event(self, events, single: Event):
        for event in events:
            if isinstance(event, single):
                self.streaming_event_received()
                return
    
    def __get_streaming_events(self, subscription_id: str, single: Event):
        for notification in self._account.inbox.get_streaming_events(subscription_id):
            if single is None:
                self.streaming_events_received(notification.events)
                continue
            self.__get_single_event(notification.events, single)
            break

    def listen(self, single: Event=None):
        with self._account.inbox.streaming_subscription() as subscription_id:
            while True:
                self.__get_streaming_events(subscription_id, single)
    
    
    class __EventHandler:
        def __init__(self):
            self._functions = []

        def __iadd__(self, func):
            self._functions.append(func)
            return self

        def __isub__(self, func):
            self._functions.remove(func)
            return self

        def __call__(self, *args, **kvargs):
            for func in self._functions:
                func(*args, **kvargs)
