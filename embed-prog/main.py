from lock_control import *
import time
import RPi.GPIO as GPIO


def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(signal, GPIO.OUT)
    GPIO.output(signal, GPIO.HIGH)
    msg = 42
    time.sleep(3)
    if validate_key(msg):
        "Great open lock"
        print("Key is valid lock is now unlocked")
        if unlock_lock():
            "The lock is now unlocked for 30 sec"
            time.sleep(5)
            if lock_lock():
                print("The lock is now locked")
                "Great lock is locked"
            else:
                "lock failed"
        else:
            "lock failed to unlock"
    else:
        "disconnect BT"
        print("Key is no good")

    GPIO.cleanup()


if __name__ == "__main__":
    main()
