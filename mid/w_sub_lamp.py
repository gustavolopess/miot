import sys
import zmq
# import requests

context = zmq.Context()
v_sub_lamp = "localhost:5559" # address:port of v_sub_lamp

# Socket to receive messages from v_sub_lamp
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://%s" %v_sub_lamp)

while True:
    s = receiver.recv()
    # save data on DB
    print(s + " " + "Saved.")