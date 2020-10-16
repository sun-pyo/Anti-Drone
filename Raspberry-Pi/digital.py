import RPi.GPIO as GPIO
import time

class Digital_Controller:
    def __init__(self, pinnum):
        self.pinnum = pinnum
        GPIO.setwarnings (False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pinnum, GPIO.OUT,initial = GPIO.LOW)
    
    def output_high(self)
        GPIO.output(self.pinnum, GPIO.HIGH)
    
    def output_low(self)
        GPIO.output(self.pinnum, GPIO.LOW)

