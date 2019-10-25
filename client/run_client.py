#!/usr/bin/env python

import measurement_pb2
import os
import time
from mqtt_client import MQTTClient

def create_mqtt_client():
    return MQTTClient(
        os.environ.get('PROJECT_ID'),
        os.environ.get('REGISTRY_ID'),
        os.environ.get('DEVICE_ID'),
        os.environ.get('PRIVATE_KEY_FILE'),
        os.environ.get('REGION'),
        os.environ.get('CA_CERTS'),
        os.environ.get('ALGORITHM'))

def main():
    client = create_mqtt_client()
    client.connect_to_server()
    measurement = measurement_pb2.Measurement()
    measurement.temperature = "23.5"
    measurement.pressure = "0.9869"

    for i in range(5):
        measurement.index = i+1
        client.send_event(measurement.SerializeToString())
        print "Message {} sent.".format(i+1)
        time.sleep(1)

    client.disconnect_from_server()

if __name__ == "__main__":
    main()
