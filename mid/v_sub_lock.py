import time
import zmq
import paho.mqtt.client as mqtt

broker_addr = "localhost" # address of lock broker
broker_port = 1883 # port of broker

def on_connect(client, obj, flags, rc):
	print("rc: " + str(rc))

def on_message(client, obj, msg): #on_message(client, userdata, message)
	# print("Sending task to workers " + msg.topic + " " + str(msg.payload))
	msg = str(msg.topic + "/" + str(msg.payload))
	sender.send(msg)

def on_subscribe(client, obj, mid, granted_qos):
	print("Subscribed on broker: " + str(mid) + " " + str(granted_qos))

# Socket to send messages to workers
context = zmq.Context()
sender = context.socket(zmq.PUSH)
sender.bind("tcp://*:5559")

# Connect and subs. to broker
client = mqtt.Client("v_sub_lock")
client.on_message = on_message
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.connect(broker_addr, broker_port, 60)
client.subscribe("drivers/smart_lock", 0)
client.loop_forever()    