from bin._time import Time


class Option:
    """
    A class that is the choices that a voted on, contains an activity, time object, a boolean of chosen, and a list of
    votes that are a pair of users and the vote choice: 1,2,3,4 . . .
    """

    def __init__(self, name, activity, location, tim=Time(), chosen=False, votes={}):
        self._name = name
        self._activity = activity
        self._location = location
        self._time = tim
        self._chosen = chosen
        self._votes = votes

    def __eq__(self, other):
        if self.name == other.name:
            if self.activity == other.activity:
                if self.location == other.location:
                    if self.time == other.time:
                        if self.chosen == other.chosen:
                            if self.votes == other.votes:
                                return True
        return False

    def __ne__(self, other):
        if self.name == other.name:
            if self.activity == other.activity:
                if self.location == other.location:
                    if self.time == other.time:
                        if self.chosen == other.chosen:
                            if self.votes == other.votes:
                                return False
        return True

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def activity(self):
        return self._activity

    @activity.setter
    def activity(self, activity):
        self._activity = activity

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = location

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, tim):
        self._time = tim

    @property
    def chosen(self):
        return self._chosen

    @chosen.setter
    def chosen(self, chosen):
        self._chosen = chosen

    @property
    def votes(self):
        return self._votes

    @votes.setter
    def votes(self, votes):
        self._votes = votes
