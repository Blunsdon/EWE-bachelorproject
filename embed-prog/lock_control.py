import RPi.GPIO as GPIO
import time

class lock_control(object):
    signal = 23
    key_code = str(42)

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.signal, GPIO.OUT)
        GPIO.output(self.signal, GPIO.HIGH)

    def validate_key(self, msg):
        if msg == self.key_code:
            bol = True
        else:
            bol = False
        return bol


    def unlock_lock(self):
        GPIO.output(self.signal, GPIO.LOW)
        if GPIO.input(self.signal) == 0:
            bol = True
        else:
            bol = False
        return bol


    def lock_lock(self):
        GPIO.output(self.signal, GPIO.HIGH)
        if GPIO.input(self.signal) == 1:
            bol = True
        else:
            bol = False
        return bol




