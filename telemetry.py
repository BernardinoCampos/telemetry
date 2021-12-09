#!/usr/bin/python3

import paho.mqtt.client as paho
import configparser
import platform

def main():
    config = configparser.ConfigParser()
    config.read('/etc/telemetry/telemetry.ini')
    broker = config['default']['broker'];

    mqtt = paho.Client("telemetry")

    mqtt.username_pw_set(username=config['default']['user'], password=config['default']['passwd'])
    mqtt.connect(config['default']['broker'],int(config['default']['port']))

    with open('/sys/class/thermal/sys/class/therma/thermal_zone0/temp') as f:
        temperature = int(f.read())/1000
        topic = config['default']['rootTopic']+"/temperature"
        mqtt.publish(topic.replace('{HOSTNAME}',platform.node()),temperature)

if __name__ == "__main__":
    main()