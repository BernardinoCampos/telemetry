import paho.mqtt.client as paho
import configparser
import platform

def main():
    config = configparser.ConfigParser()
    config.read('/etc/telemetry/telemetry.ini')
    broker = config['DEFAULT']['broker'];

    mqtt = paho.Client("telemetry")

    mqtt.username_pw_set(username=config['DEFAULT']['user'], password=config['DEFAULT']['passwd'])
    mqtt.connect(config['DEFAULT']['broker'],config['DEFAULT']['port'])

    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        temperature = int(f.read())/1000
        topic = config['DEFAULT']['rootTopic']+"/temperature"
        topic.replace('{HOSTNAME}',platform.node())
        mqtt.publish(topic,temperature)

if __name__ == "__main__":
    main()