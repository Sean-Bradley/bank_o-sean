"""The Python implememntation of seans grpc client"""
import os
import time
import uuid
import random
import grpc
import balance_pb2
import balance_pb2_grpc

# def run():
#     "The run method, that sends gRPC conformant messsages to the server"
#     #counter = 0
#     #pid = os.getpid()
#     with grpc.insecure_channel("localhost:9999") as channel:
#         stub = balance_pb2_grpc.BalanceServiceStub(channel)
#         while True:
#             try:
#                 #start = time.time()
#                 #response = stub.ping(pingpong_pb2.Ping(count=counter))
#                 # counter = response.count
#                 # if counter % 1000 == 0:
#                 #     print(
#                 #         "%.4f : resp=%s : procid=%i"
#                 #         % (time.time() - start, response.count, pid)
#                 #     )
#                     # counter = 0
#                 #time.sleep(0.001)
#             except KeyboardInterrupt:
#                 print("KeyboardInterrupt")
#                 channel.unsubscribe(close)
#                 exit()


def close(channel):
    "Close the channel"
    channel.close()


def registerBalances():
    with grpc.insecure_channel("localhost:9999") as channel:
        bank_O_Sean = balance_pb2_grpc.BalanceServiceStub(channel)
        for _x in range(10000):
            balance_id = str(uuid.uuid4())
            bank_O_Sean.createBalance(balance_pb2.Id(id=balance_id))
            response = bank_O_Sean.adjustBalance(
                balance_pb2.BalanceAdjustment(id=balance_id, amount=random.randint(0, 1000))
            )
            #print("bal = " + str(response.amount))
        print("done")

if __name__ == "__main__":
    registerBalances()
    # run()
