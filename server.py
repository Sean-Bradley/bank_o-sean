"""The main Bank O'Sean server.
This is the single source of truth for all balances held at the Bank O'Sean"""
from concurrent import futures
import threading
import time
import uuid
import random
import grpc
import balance_pb2
import balance_pb2_grpc
from safe import Safe

SAFE = Safe()


class Listener(balance_pb2_grpc.BalanceServiceServicer):
    """The listener function implements the rpc call as described in the balance.proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()

    def __str__(self):
        return self.__class__.__name__

    def createBalance(self, request, context):
        amount = SAFE.create_balance(request.id)
        return balance_pb2.Balance(amount=amount)

    def getBalance(self, request, context):
        amount = SAFE.get_balance(request.id)
        return balance_pb2.Balance(amount=amount)

    def adjustBalance(self, request, context):
        amount = SAFE.adjust_balance(request.id, request.amount)
        return balance_pb2.Balance(amount=amount)


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


def create_balances():
    """fill the bank with fake balances that we can read and write to"""

    for _x in range(100):
        balance_id = uuid.uuid4()
        SAFE.create_balance(balance_id)
        SAFE.adjust_balance(balance_id, random.randint(0, 1000))
        print(SAFE.get_balance(balance_id))


if __name__ == "__main__":
    create_balances()
    start_bank()
