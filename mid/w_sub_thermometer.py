import sys
import zmq
# import requests

context = zmq.Context()
v_sub_thermometer = "localhost:5559" # address:port of v_sub_thermometer

# Socket to receive messages from v_sub_thermometer
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://%s" %v_sub_thermometer)

while True:
    s = receiver.recv()
    # save data on DB
    print(s + " " + "Saved.")