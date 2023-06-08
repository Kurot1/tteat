import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import json
import time
import psutil

for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein':
        proc.kill()
        
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

buzzer = 12


LED = 23
TRIG = 19
ECHO = 13

GPIO.setup(buzzer, GPIO.OUT)

print("start")

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.setup(LED,GPIO.OUT)




MQTT_HOST = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_KEEPALSE_INTERVAL = 60
MQTT_PUB_TOPIC = "mobile/jiyoung/tteat"
client = mqtt.Client()

client.connect(MQTT_HOST,MQTT_PORT,MQTT_KEEPALSE_INTERVAL )
client.loop_start()




try:
    p = GPIO.PWM(buzzer, 262)
    while True:
        #거리 감지 
        GPIO.output(TRIG, False)
        time.sleep(0.5)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0 :
            pulse_start = time.time()

        while GPIO.input(ECHO) == 1 :
            pulse_end = time.time()
            
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17000
        distance = round(distance, 2)

        print("거리 : ", distance, "cm")
        #물건이 범위 밖에 있을때
        if distance >= 30:
            print("물건이 범위 밖에 있습니다")
            GPIO.output(LED, GPIO.HIGH)
            p.start(50)
            time.sleep(1)
            p.stop()
            
            try:
                sensing = {"distance":distance}
                value = json.dumps(sensing)
                client.publish(MQTT_PUB_TOPIC,value)
                print(value)
            except RuntimeError:
                time.sleep(5)
                continue
          #물건이 범위 안에 있을때 
        else:
            print("물건이 범위 안에 있습니다")
            GPIO.output(LED, GPIO.LOW)
            time.sleep(1)
            try:
                safe = {"distance":distance}
                value = json.dumps(safe)
                client.publish(MQTT_PUB_TOPIC,value)
                print(value)
            except RuntimeError:
                time.sleep(5)
                continue
            
           
            
            
           
except KeyboardInterrupt:
    print("종료합니다!!")
finally:
    GPIO.cleanup()
    client.disconnect()
   

