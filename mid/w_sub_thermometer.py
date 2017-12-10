import sys
import zmq
import requests

rest = "127.0.0.1:5000"
value = "temperature"

context = zmq.Context()
v_sub_thermometer = "localhost:5556" # address:port of v_sub_thermometer

# Socket to receive messages from v_sub_thermometer
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://%s" %v_sub_thermometer)

while True:
    s = receiver.recv() 
    msg = s.decode().split("/")
    aux = msg[2].split(">")
    dictToSend = {'value': float(aux[1]), 'device_id': int(aux[0])}
    url = str("http://"+rest+"/api/device/register/thermometer/")
    res = requests.post(url, json=dictToSend)