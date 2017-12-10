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
    print(s)
    msg = s.decode().split("/")
    aux = msg[2].split("::")
    dictToSend = {'value': aux[1]}
    url = str("http://"+rest+"/api/device/change/state/air/{}/".format(aux[0]))
    res = requests.post(url, json=dictToSend)