from datetime import datetime
from random import randrange

import paho.mqtt.client as mqtt
import time
import argparse

# Dirección del bróker MQTT
broker_address = "20.106.79.14"
# Puerto del bróker MQTT
broker_port = 8082

client = mqtt.Client("Pub-test")


def send_messages():
    while True:
        r1 = randrange(180)
        r2 = randrange(180)
        message = ""
        topic1 = "usertest1/ankle/" + str(r1)
        res1 = client.publish(topic1, message)
        topic2 = "usertest1/knee/" + str(r2)
        res2 = client.publish(topic2, message)
        log_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(log_date, topic1 + ": " + message)
        print(log_date, topic2 + ": " + message)
        print("\tMsg:", mqtt.connack_string(res1[0]))
        print("\tMsg:", mqtt.connack_string(res2[0]))
        time.sleep(2)


def on_publish(client, userdata, result):
    print("Publish successful!")
    pass


def on_connect(client, userdata, flags, rc):
    print("Connected: ", rc)
    pass


def on_error(client, userdata, rc):
    print("Connection failed!", rc)
    pass


def on_disconnect(client, userdata, rc):
    print("Disconnected!", mqtt.connack_string(rc))
    pass


def on_log(client, userdata, level, buf):
    print("Log: ", buf)
    pass

def publish():
    print("publishing data")
    client.username_pw_set("usertest1", "password1")
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_connect_fail = on_error
    client.on_disconnect = on_disconnect
    client.connect(broker_address, broker_port, 60)


    send_messages()

