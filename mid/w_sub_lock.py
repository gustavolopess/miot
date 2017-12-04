import sys
import zmq
# import requests

context = zmq.Context()
v_sub_lock = "localhost:5559" # address:port of v_sub_lock

# Socket to receive messages from v_sub_lock
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://%s" %v_sub_lock)

while True:
    s = receiver.recv()
    # save data on DB
    print(s + " " + "Saved.")