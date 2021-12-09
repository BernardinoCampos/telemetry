#!/usr/bin/python3

import paho.mqtt.client as paho
import configparser
import platform
import os.path
import subprocess
import sys

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
    elif platform.system()=='FreeBSD':
        p1 = subprocess.run(['sysctl','-a'], stdout=subprocess.PIPE)
        p2 = subprocess.run(['grep','temperature'], stdin=p1.stdout, stdout=subprocess.PIPE)
        p3 = subprocess.run(['grep','"dev.cpu."'], stdin=p2.stdout, stdout=subprocess.PIPE)
        p4 = subprocess.run(['sort','-k2','-r'], stdin=p3.stdout, stdout=subprocess.PIPE)
        p5 = subprocess.run(['head','-1'], stdin=p4.stdout, stdout=subprocess.PIPE)
        p6 = subprocess.run(['cut','-d','" "','-f2'], stdin=p5.stdout, stdout=subprocess.PIPE)
        print(p6.stdout)
    else:
        print("Não foi encontrada forma de pegar a temperatura")

if __name__ == "__main__":
    main()