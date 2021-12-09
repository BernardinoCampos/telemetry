#!/usr/bin/python3

import paho.mqtt.client as paho
import configparser
import platform
import os.path
import subprocess

def main():
    config = configparser.ConfigParser()
    config.read('/etc/telemetry/telemetry.ini')
    broker = config['default']['broker'];

    mqtt = paho.Client("telemetry")

    mqtt.username_pw_set(username=config['default']['user'], password=config['default']['passwd'])
    mqtt.connect(config['default']['broker'],int(config['default']['port']))

    if os.path.isfile('/sys/class/thermal/thermal_zone0/temp'):
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            temperature = int(f.read())/1000
            topic = config['default']['rootTopic']+"/temperature"
            mqtt.publish(topic.replace('{HOSTNAME}',platform.node()),temperature)
    elif os.path.isfile('/usr/bin/sensors'):
        result = subprocess.run(['/usr/bin/sensors'], stdout=subprocess.PIPE)
        print(result.stdout)

if __name__ == "__main__":
    main()