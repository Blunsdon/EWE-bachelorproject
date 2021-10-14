import RPi.GPIO as GPIO
import time

signal = 23
key_code = 42


def validate_key(msg):
    if msg == key_code:
        bol = True
    else:
        bol = False
    return bol


def unlock_lock():
    GPIO.output(signal, GPIO.LOW)
    if GPIO.input(signal) == 0:
        bol = True
    else:
        bol = False
    return bol


def lock_lock():
    GPIO.output(signal, GPIO.HIGH)
    if GPIO.input(signal) == 1:
        bol = True
    else:
        bol = False
    return bol




