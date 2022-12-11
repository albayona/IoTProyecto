from datetime import datetime

import paho.mqtt.client as mqtt
import json
import ssl
import traceback
from realtimeSensorReadings.views import  get_or_create_measurement, get_or_create_user, create_reading
from django.utils import timezone

# Dirección del bróker MQTT
broker_address = "20.106.79.14"
# Puerto del bróker MQTT
broker_port = 8082
# Tópico a suscribir. '#' se refiere a todos los tópicos.
topic = "#"


def on_message(client, userdata, message):
    try:
        payload = message.payload.decode("utf-8")
        topic = message.topic.split('/')
        print(topic)
        user = topic[0]
        measure = topic[1]
        angle = float(topic[2])
        user_obj = get_or_create_user(user)
        unit = '°'
        measure_obj = get_or_create_measurement(measure, unit)
        print("createreading")
        d = create_reading(angle, measure_obj, datetime.now(), user_obj)
        print(d.time)
            
    except Exception as e:
        print('Ocurrió un error procesando el paquete MQTT', e)
        traceback.print_exc()

def on_connect(client, userdata, flags, rc):
    print("Suscribiendo al tópico: " + topic)
    client.subscribe(topic)
    print("Servicio de recepcion de datos iniciado")

def on_disconnect(client: mqtt.Client, userdata, rc):
    '''
    Función que se ejecuta cuando se desconecta del broker.
    Intenta reconectar al bróker.
    '''
    print("Desconectado con mensaje:" + str(mqtt.connack_string(rc)))
    print("Reconectando...")
    client.reconnect()

def subscribe():

    print("MQTT Start")
    client = mqtt.Client('')
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.username_pw_set("usertest1", "password1")
    client.connect(broker_address, broker_port, 60)
    client.loop_forever()
    print("Time: ", timezone.now())

