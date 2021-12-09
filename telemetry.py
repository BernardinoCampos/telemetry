import paho.mqtt.client as paho
import configparser
import platform

def main():
    config = configparser.ConfigParser()
    config.read('/etc/telemetry/telemetry.ini')
    broker = config['default']['broker'];

    mqtt = paho.Client("telemetry")

    mqtt.username_pw_set(username=config['default']['user'], password=config['default']['passwd'])
    mqtt.connect(config['default']['broker'],config['default']['port'])

    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        temperature = int(f.read())/1000
        topic = config['default']['rootTopic']+"/temperature"
        topic.replace('{HOSTNAME}',platform.node())
        mqtt.publish(topic,temperature)

if __name__ == "__main__":
    main()