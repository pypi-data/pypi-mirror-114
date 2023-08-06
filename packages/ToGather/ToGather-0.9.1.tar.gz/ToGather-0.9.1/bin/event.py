class Event:
    """A class that contains a list of options, a description and is either"""
    "complete or incomplete, completes are in the calendar, both are in the group"

    def __init__(self, name, description, options=[], group="", submitted=[], status=False):
        self._name = name
        self._description = description
        self._options = options
        self._group = group
        self._submitted = submitted
        self._status = status

    def __eq__(self, other):
        if self.name == other.name:
            if self.description == other.description:
                if self.options == other.options:
                    if self.group == other.group:
                        if self.submitted == other.submitted:
                            if self.status == other.status:
                                return True
        return False

    def __ne__(self, other):
        if self.name == other.name:
            if self.description == other.description:
                if self.options == other.options:
                    if self.group == other.group:
                        if self.submitted == other.submitted:
                            if self.status == other.status:
                                return False
        return True

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, options):
        self._options = options

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, group):
        self._group = group

    @property
    def submitted(self):
        return self._submitted

    @submitted.setter
    def submitted(self, submitted):
        self._submitted = submitted

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

