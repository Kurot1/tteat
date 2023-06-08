import paho.mqtt.client as mqtt
import time
import json
import adafruit_dht
import psutil

for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein':
        proc.kill()
        
dht_device = adafruit_dht.DHT22(4)


MQTT_HOST = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_KEEPALSE_INTERVAL = 60
MQTT_PUB_TOPIC = "mobile/jiyoung/tteat"
client = mqtt.Client()

client.connect(MQTT_HOST,MQTT_PORT,MQTT_KEEPALSE_INTERVAL )
client.loop_start()


try:
    while True:
        try:
            time.sleep(5)
            #dht sensor
            humidity, temperature =80, 30
            distance = {
                "temperation":temperature,
                "humidity": humidity
              }
            value = json.dumps(distance)
            client.publish(MQTT_PUB_TOPIC,value)
            print(value)
        except RuntimeError:
            time.sleep(5)
            continue
except KeyboardInterrupt:
    print("I'm done!!")
finally:
    client.disconnect()
