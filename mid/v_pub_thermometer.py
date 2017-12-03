import time
import zmq

# Socket to send messages to workers
context = zmq.Context()
sender = context.socket(zmq.PUSH)
sender.bind("tcp://*:5559")

while True:
	# this must be on post service on rest
	# s: device_id+">"+str(temperature)
    sender.send(s)
    print "Sending task to workers " + s