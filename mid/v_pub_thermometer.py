import time
import zmq

context = zmq.Context()

# Socket to receive messages from c1
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:5558")

# Socket to send messages to workers
sender = context.socket(zmq.PUSH)
sender.bind("tcp://*:5559")

while True:
	# this must be on post service on rest
	# s: device_id+">"+str(temperature)
    sender.send(s)
    print("Sending task to " + s) 