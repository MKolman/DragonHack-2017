import time
import requests
from random import randint

import RPi.GPIO as GPIO

from kot_conversion import convert
GPIO.setmode(GPIO.BOARD)

PWM_FREQ = 512
LEFT_FORWARD_PIN = 11
LEFT_BACKWARD_PIN = 12
RIGHT_FORWARD_PIN = 15
RIGHT_BACKWARD_PIN = 16
ALL_PINS = [LEFT_FORWARD_PIN, LEFT_BACKWARD_PIN, RIGHT_FORWARD_PIN, RIGHT_BACKWARD_PIN]

class Wheel(object):
    def __init__(self, front, back):
        # front and back are pin numbers
        # Save both pins
        GPIO.setup(front, GPIO.OUT)
        self.front = GPIO.PWM(front, PWM_FREQ)
        self.front.start(0)
        GPIO.setup(back, GPIO.OUT)
        self.back = GPIO.PWM(back, PWM_FREQ)
        self.back.start(0)

    def go(self, value):
        print('value', value)
        if value < 0:
            self.front.ChangeDutyCycle(0)
            self.back.ChangeDutyCycle(-value)
        else:
            self.front.ChangeDutyCycle(value)
            self.back.ChangeDutyCycle(0)

    def stop(self):
        self.front.ChangeDutyCycle(0)
        self.back.ChangeDutyCycle(0)


class Car(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def move(self, left, right):
        self.left.go(left)
        self.right.go(right)


try:
    pp3 = Car(Wheel(LEFT_FORWARD_PIN, LEFT_BACKWARD_PIN),
              Wheel(RIGHT_FORWARD_PIN, RIGHT_BACKWARD_PIN))
    while True:
        r = requests.get("http://193.2.179.248:5000/direction")
        # tmp = r.text.strip().split()
        r, deg = map(int, r.text.split())
        left, right = convert(deg, r)
        pp3.move(left, right)
        time.sleep(0.25)
finally:
    GPIO.cleanup()
