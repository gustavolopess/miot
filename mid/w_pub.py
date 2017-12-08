import time
import zmq
import paho.mqtt.client as mqtt

broker_addr = "localhost" # address of air broker
broker_port = 1883 # port of air broker
rest_push = "localhost:5555"

def on_connect(client, obj, flags, rc):
	print("rc: " + str(rc))

def on_disconnect(client, userdata, rc=0):
	print("DisConnected result code " + str(rc))
	client.loop_stop()

def on_publish(client, obj, mid):
	print("mid: " + str(mid))

# Socket to receive messages from rest
context = zmq.Context()
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://%s" %rest_push)

# Connect and pub. to broker
client = mqtt.Client("w_pub")
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish 
client.connect(broker_addr, broker_port, 60)
client.loop_start()
while True:
    s = receiver.recv() # receive data from REST
    msg = s.decode().split('/')
    if msg[0] == "air":
        client.publish("commands/air_conditioner/"+msg[1], msg[2]) # send data to broker
    elif msg[0] == "thermometer":
        client.publish("devices/termometer/"+msg[1], msg[2]) # send data to broker
    elif msg[0] == "closure":
        client.publish("commands/smart_lock/"+msg[1], msg[2]) # send data to broker
    elif msg[0] == "bulb":
        client.publish("devices/smart_lamp/"+msg[1], msg[2]) # send data to broker