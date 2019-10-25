#!/usr/bin/env python

# Copyright 2018 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import paho.mqtt.client as mqtt
import utilities
import ssl
import time
import json

def error_str(rc):
    return '{}: {}'.format(rc, mqtt.error_string(rc))

def on_disconnect(unused_client, unused_userdata, rc):
    print('on_disconnect', error_str(rc))

class MQTTClient(object):
    mqtt_bridge_hostname = 'mqtt.googleapis.com'
    mqtt_bridge_port = 8883
    connected = False

    def __init__(self, project_id, registry_id, device_id, private_key_file, cloud_region, ca_certs, algorithm):
        self.topic = '/devices/{}/events'.format(device_id)
        self.device_id = device_id
        self.client = mqtt.Client(
            client_id=('projects/{}/locations/{}/registries/{}/devices/{}'
                   .format(
                           project_id,
                           cloud_region,
                           registry_id,
                           device_id)))
        self.client.username_pw_set(
            username='unused',
            password=utilities.create_jwt(
                project_id, private_key_file, algorithm))
        self.client.tls_set(ca_certs=ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)
        self.client.on_disconnect = on_disconnect

    def connect_to_server(self):
        self.client.connect(self.mqtt_bridge_hostname, self.mqtt_bridge_port)
        self.connected = True

    def disconnect_from_server(self):
        self.client.disconnect()
        self.connected = False

    def send_event(self, msg):
        self.client.loop()
        msgInfo = self.client.publish(self.topic, msg, qos=1)
