import time
from random import randint

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)


class Wheel(object):
    def __init__(self, front, back):
        # Save both pins
        self.front = front
        self.back = back
        # Set them as output
        GPIO.setup(front, GPIO.OUT)
        GPIO.setup(back, GPIO.OUT)
        # Stop the wheels
        GPIO.output(front, False)
        GPIO.output(back, False)

    def forw(self):
        GPIO.output(self.front, True)
        GPIO.output(self.back, False)

    def backw(self):
        GPIO.output(self.front, False)
        GPIO.output(self.back, True)

    def stop(self):
        GPIO.output(self.front, False)
        GPIO.output(self.back, False)


class Car(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def move(self, direction):
        if direction == 0:
            self.stop()
        elif direction == 1:
            self.drive()
        elif direction == 2:
            self.reverse()
        elif direction == 3:
            self.turn_left()
        elif direction == 4:
            self.turn_right()

    def turn_left(self):
        self.right.forw()
        self.left.backw()

    def turn_right(self):
        self.left.forw()
        self.right.backw()

    def stop(self):
        self.left.stop()
        self.right.stop()

    def drive(self):
        self.left.forw()
        self.right.forw()

    def reverse(self):
        self.left.backw()
        self.right.backw()


try:
    pp3 = Car(Wheel(11, 12), Wheel(15, 16))
    for i in range(100):
        pp3.move(randint(0, 4))
        time.sleep(1)
finally:
    GPIO.cleanup()
