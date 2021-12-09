#!/usr/bin/python3

import paho.mqtt.client as paho
import configparser
import platform
import os.path
import subprocess
import sys

def main():

    print (platform.system())

    if not os.path.isfile('/etc/telemetry/telemetry.ini'):
        print("Config file /etc/telemetry/telemetry.ini not found")
        sys.exit(-1)

    config = configparser.ConfigParser()
    config.read('/etc/telemetry/telemetry.ini')
    broker = config['default']['broker'];

    mqtt = paho.Client("telemetry")

    mqtt.username_pw_set(username=config['default']['user'], password=config['default']['passwd'])
    mqtt.connect(config['default']['broker'],int(config['default']['port']))

    if os.path.isfile('/sys/class/thermal/thermal_zone1/temp'):
        print("Opcao 1")
        with open('/sys/class/thermal/thermal_zone1/temp') as f:
            temperature = int(f.read())/1000
            topic = config['default']['rootTopic']+"/temperature"
            mqtt.publish(topic.replace('{HOSTNAME}',platform.node()),temperature)
    elif os.path.isfile('/sys/class/thermal/thermal_zone0/temp'):
        print("Opcao 2")
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            temperature = int(f.read())/1000
            topic = config['default']['rootTopic']+"/temperature"
            mqtt.publish(topic.replace('{HOSTNAME}',platform.node()),temperature)
    else:
        print("Não foi encontrada forma de pegar a temperatura")

if __name__ == "__main__":
    main()