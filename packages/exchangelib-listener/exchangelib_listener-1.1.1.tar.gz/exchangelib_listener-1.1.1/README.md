Inbox event listener for exchangelib
====================================
This library listens for events in the inbox and raises an event.

## Usage
Create listener:
```python
from exchangelib import DELEGATE, Account, Credentials, Configuration
from exchangelib.properties import NewMailEvent, MovedEvent
from exchangelib_listener import Listener

creds = Credentials(
    username='EMAIL_ADDRESS',
    password='PASSWORD'
)
config = Configuration(
    server='SERVER',
    credentials=creds
)
acct = Account(
    primary_smtp_address='EMAIL_ADDRESS',
    config=config,
    access_type=DELEGATE
)

listener = Listener(acct)
```

Create a method to call when events are raised:
```python
def events_received(events):
    for event in events:
        if isinstance(event, NewMailEvent):
            # Do something
        elif isinstance(event, MovedEvent):
            # Do something

listener.streaming_events_received += events_received
listener.listen()
```

Or receive a single event:
```python
def new_messaged_received():
    # Do something

listener.streaming_event_received += new_messaged_received
listener.listen(NewMailEvent)
```
