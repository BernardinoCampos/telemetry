#!/usr/bin/python3

import paho.mqtt.client as paho
import configparser
import platform
import os.path
import subprocess
import sys
import re
from datetime import datetime, timezone

def main():

    if not os.path.isfile('/etc/telemetry/telemetry.ini'):
        print("Config file /etc/telemetry/telemetry.ini not found")
        sys.exit(-1)

    config = configparser.ConfigParser()
    config.read('/etc/telemetry/telemetry.ini')
    broker = config['default']['broker'];

    mqtt = paho.Client("telemetry")

    mqtt.username_pw_set(username=config['default']['user'], password=config['default']['passwd'])
    mqtt.connect(config['default']['broker'],int(config['default']['port']))

    topicTemp = config['default']['rootTopic'] + "/temperature"
    topicLastSeen = config['default']['rootTopic'] + "/last_seen"

    if os.path.isfile('/sys/class/thermal/thermal_zone1/temp'):
        print("Opcao 1")
        with open('/sys/class/thermal/thermal_zone1/temp') as f:
            temperature = int(f.read())/1000
            mqtt.publish(topicTemp.replace('{HOSTNAME}',platform.node()),temperature)
    elif os.path.isfile('/sys/class/thermal/thermal_zone0/temp'):
        print("Opcao 2")
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            temperature = int(f.read())/1000
            mqtt.publish(topicTemp.replace('{HOSTNAME}',platform.node()),temperature)
    elif platform.system()=='FreeBSD':
        command = subprocess.check_output("sysctl -a | grep temperature | grep 'dev.cpu.' | sort -k2 -r | head -1 | cut -d' ' -f 2",shell=True)
        m = re.match('[.0-9]+', command.decode())
        mqtt.publish(topicTemp.replace('{HOSTNAME}', platform.node()), float(m.group(0)))
    else:
        print("Não foi encontrada forma de pegar a temperatura")


    mqtt.publish(topicLastSeen.replace('{HOSTNAME}', platform.node()), datetime.now(tz=timezone.utc).isoformat())

if __name__ == "__main__":
    main()