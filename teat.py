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
button = 24
TRIG = 19
ECHO = 13

GPIO.setup(buzzer, GPIO.OUT)

print("start")

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.setup(LED,GPIO.OUT)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def my_callback(channel):
    print("버튼이 눌렸습니다")
    
GPIO.add_event_detect(button, GPIO.RISING, callback=my_callback)

try:
    p = GPIO.PWM(buzzer, 262)
    num = 1
    while True:
        #버튼 감지
        value = GPIO.input(button)
        print(value)
        time.sleep(1)
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
        
        if distance >= 30:
            print("물건이 범위 밖에 있습니다")
            GPIO.output(LED, GPIO.HIGH)
            p.start(50)
            time.sleep(1)
            p.stop()
        else:
            print("물건이 범위 안에 있습니다")
            GPIO.output(LED, GPIO.LOW)
            time.sleep(1)
            
            
        

    
    
        

        
except KeyboardInterrupt:
    print("종료합니다!!")
finally:
    GPIO.cleanup()
   

