import sys
import zmq
import requests

rest = "127.0.0.1:5000"
value = "turned_on"

context = zmq.Context()
v_sub_lamp = "localhost:5557" # address:port of v_sub_lamp

# Socket to receive messages from v_sub_lamp
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://%s" %v_sub_lamp)

while True:
    s = receiver.recv()
    msg = s.split("/")
    aux = msg[2].split("=")
    dictToSend = {value : aux[1], 'device_id': aux[0]}
    url = str("http://"+rest+"/api/device/register/bulb/")
    res = requests.post(url, json=dictToSend)