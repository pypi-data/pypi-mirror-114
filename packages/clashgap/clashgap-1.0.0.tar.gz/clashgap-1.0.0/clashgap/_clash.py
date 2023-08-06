from ._gap import gap as gap_of
from ._fill import fill as fill_of

class Clash:
    def __init__(self, clash):
        self._gap = gap_of(clash)

    def gap(self):
        return self._gap

    def fill(self):
        return fill_of(self._gap)

    def __str__(self):
        return str(self._gap)

    def __repr__(self):
        return str(self._gap)
