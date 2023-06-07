import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from time import sleep
from subprocess import call
from subprocess import datetime
import json
import time
import psutil

btn_pin = 24
shutdown_sec =2
GPIO.setmode(GPIO.BOARD)
GPIO.setup(btn_pin, GPIO.IN)

press_time = None

def button_state_changed(pin):
    global press_time
    if GPIO.input(pin) ==0:
        if press_time is None:
            press_time = detetime.now()
    else:
        if press_time is not None:
            elapsed = (datetime.now() 

 
  