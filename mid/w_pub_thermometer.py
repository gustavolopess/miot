import time
import zmq
import paho.mqtt.client as mqtt

broker_addr = "localhost" # address of broker
broker_port = 1883 # port of broker
v_pub_thermometer = "localhost:5559" # address:port of v_pub_thermometer

def on_connect(client, obj, flags, rc):
	print("rc: " + str(rc))

def on_disconnect(client, userdata, rc=0):
	print("DisConnected result code " + str(rc))
	client.loop_stop()

def on_publish(client, obj, mid):
	print("mid: " + str(mid))

# Socket to receive messages from v_pub_thermometer
context = zmq.Context()
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://%s" %v_pub_thermometer)

# Connect and pub. to broker
client = mqtt.Client("w_pub_thermometer")
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish 
client.connect(broker_addr, broker_port, 60)
client.loop_start()
while True:
    s = receiver.recv() # receive data from REST (v_pub_thermometer)
    # s is: id>number
	client.publish("devices/termometer/", s)  #s: device_id+">"+str(temperature)
