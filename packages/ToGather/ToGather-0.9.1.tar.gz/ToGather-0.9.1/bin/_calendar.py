class GroupCalendar:
    """A class that contains a list of completed events, this belongs to a group"""

    def __init__(self, name, events=[]):
        self._events = events
        self._name = name

    def __eq__(self, other):
        if self.name == other.name:
            if self.events == other.events:
                return True
        return False

    def __ne__(self, other):
        if self.name == other.name:
            if self.events == other.events:
                return False
        return True

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def events(self):
        return self._events

    @events.setter
    def events(self, events):
        self._events = events
