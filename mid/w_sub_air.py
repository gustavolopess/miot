import sys
import zmq
import requests

rest = "127.0.0.1:5000"
value = "air_temperature"

context = zmq.Context()
v_sub_air = "localhost:5558" # address:port of v_sub_air

# Socket to receive messages from v_sub_air
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://%s" %v_sub_air)

while True:
    s = receiver.recv()
    msg = s.decode().split("/")
    aux = msg[2].split("::")
    print(aux)
    dictToSend = {'value': int(aux[1]), 'device_id': float(aux[0])}
    url = str("http://"+rest+"/api/device/register/air/")
    res = requests.post(url, json=dictToSend)
