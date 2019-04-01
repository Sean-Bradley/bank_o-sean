"""The Bank O'Sean Safe where all the balances are stored"""
from borg import Borg


class Safe(Borg):
    """The Safe Class. This uses the Borg Singleton style pattern"""

    def __init__(self, name=None):
        Borg.__init__(self)
        if name is not None:
            self.name = name

    def __str__(self):
        return "Safe(%s)" % self.name

    def create_balance(self, balance_id):
        """Create a new balance recrod and it s key is the balance_id.
        Returns existing balance, if balance_id already exists"""
        self.safe[balance_id] = {"balance": 0}
        return self.safe[balance_id]

    def get_balance(self, balance_id):
        """Get a balance by balance_id"""
        return self.safe[balance_id]

    def adjust_balance(self, balance_id, amount):
        "Adjust a balance by balance_id"
        self.safe[balance_id] = {"balance": amount}
        return self.safe[balance_id]
