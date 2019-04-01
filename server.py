from concurrent import futures
import threading
import time
import grpc
import balance_pb2
import balance_pb2_grpc
import random
import uuid


class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        self.safe = {}


class Safe(Borg):
    def __init__(self, name=None):
        Borg.__init__(self)
        if name is not None:
            self.name = name

    def __str__(self):
        return "Safe(%s)" % self.name

    def add_account(self, id):
        self.safe[id] = {"balance": 0}

    def get_balance(self, id):
        return self.safe[id]

    def adjust_balance(self, id, amount):
        self.safe[id] = {"balance": amount}
        return self.safe[id]


class Listener(balance_pb2_grpc.BalanceServiceServicer):
    """The listener function implements the rpc call as described in the balance.proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()

    def __str__(self):
        return self.__class__.__name__

    def getBalance(self, request, context):
        return balance_pb2.Balance(amount=123)

    def adjustBalance(self, request, context):
        return balance_pb2.Balance(amount=456)


def start_bank():
    """The main bank balance service.
    This opens the socket, and listens for incoming grpc conformant packets"""

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    balance_pb2_grpc.add_BalanceServiceServicer_to_server(Listener(), server)
    server.add_insecure_port("[::]:9999")
    server.start()
    try:
        while True:
            print("Bank O'Sean Running : threadcount %i" % (threading.active_count()))
            time.sleep(10)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        server.stop(0)


def create_bank():
    """fill the bank with fake accounts that we can read and write to"""
    SAFE = Safe()
    for x in range(100):
        id = uuid.uuid4()
        SAFE.add_account(id)
        SAFE.adjust_balance(id, random.randint(0,1000))
        print(SAFE.get_balance(id))


if __name__ == "__main__":
    create_bank()
    start_bank()
