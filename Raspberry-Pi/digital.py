import RPi.GPIO as GPIO
import time

class Digital_Controller:
    def __init__(self, pinnum):
        self.pinnum = pinnum
        GPIO.setwarnings (False)
        GPIO.setup(self.pinnum, GPIO.OUT,initial = GPIO.LOW)
    
    def on(self):
        GPIO.output(self.pinnum, GPIO.HIGH)
    
    def off(self):
        GPIO.output(self.pinnum, GPIO.LOW)

