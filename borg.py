"""The Borg Style Sigleton Pattern"""


class Borg:
    """The Borg Style Sigleton Pattern"""

    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        self.safe = {}

    def __str__(self):
        return self.__class__.__name__

    def length(self):
        """Get how many keys stored in the safe dictionary"""
        return len(self.safe)
