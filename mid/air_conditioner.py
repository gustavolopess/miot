from multiprocessing import Process
from time import sleep
import paho.mqtt.client as mqtt
import argparse

def air_conditioner(device_id):
    objective = 33
    temperature = 33


    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("commands/air_conditioner/" + device_id)

    def on_message(client, userdata, msg):
        nonlocal objective
        print(objective)
        objective = int(msg.payload.decode())

    def on_disconnect(client, userdata, rc):
        print("disconnected")
        

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    
    client.connect("10.0.0.2", 1883, 60)
    client.loop_start()

    while True:
        sleep(1)
        if temperature > objective:
            temperature -=1
        elif temperature < objective:
            temperature += 1
        print('my temperature is ' + str(temperature))
        client.publish("drivers/virtual_air", device_id+"::"+str(temperature))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--size", type=int,
                        help="how many device instances to create", default=1)
    args = parser.parse_args()

    for device_id in range(args.size):
        Process(target=air_conditioner, args=(str(device_id),)).start()