import time
import atexit
import sys
import termios
import contextlib
import threading
#import imutils
import RPi.GPIO as GPIO

# Import the PCA9685 module.
import Adafruit_PCA9685

# 모터 컨트롤
class ServoMotor():
    """
    Class used for turret control.
    """    
    # 30 ~ 150
    # freq(10) 기준  0 ~ 180도 -> 200 ~ 690 pulse 

    def __init__(self):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pan_min = 363  # 60도
        self.pan_max = 526  # 120도
        self.servo_mean = 445 # 90도 
        self.tilt_min = 282 # 0도
        self.tilt_max = 608 # 150도 
        self.tiltpulse = self.servo_mean
        self.panpulse = self.servo_mean
        self.pwm.set_pwm_freq(10)
    
    # 왼쪽으로 회전
    def left(self):
        self.panpulse += 8
        self.pwm.set_pwm(0, 0, self.panpulse)
        time.sleep(0.001)
        print("left")
        print(self.panpulse)
        if self.panpulse > self.pan_max:
            self.panpulse = self.pan_max
    
    # 오른쪽으로 회전 
    def right(self):
        self.panpulse -= 8
        self.pwm.set_pwm(0, 0, self.panpulse)
        time.sleep(0.001)
        print("right")
        print(self.panpulse)
        if self.panpulse < self.pan_min:
            self.panpulse = self.pan_min
    
    # 정지
    def stop(self):
        self.pwm.set_pwm(0, 0, 0)
        time.sleep(0.005)
        print("stop")
    
    # 위로 회전
    def up(self):
        self.tiltpulse -= 6
        self.pwm.set_pwm(1, 0, self.tiltpulse)
        time.sleep(0.001)
        print("up")
        print(self.tiltpulse)
        if self.tiltpulse < self.tilt_min:
            self.tiltpulse = self.tilt_min
    # 아래로 회전
    def down(self):
        self.tiltpulse += 6
        self.pwm.set_pwm(1, 0, self.tiltpulse)
        time.sleep(0.001)
        print("down")
        print(self.tiltpulse)
        if self.tiltpulse > self.tilt_max:
            self.tiltpulse = self.tilt_max
    
    # 원점으로 이동
    def reset(self):
        self.tiltpulse = self.servo_mean
        self.panpulse = self.servo_mean
        self.pwm.set_pwm(1, 0, self.tiltpulse)
        self.pwm.set_pwm(0, 0, self.panpulse)

    # 정해진 신호에 따라 해당 방향으로 이동
    def set_pulse(self, L_or_R, tilt):
        if L_or_R == 'L':
            self.panpulse = self.pan_max
            self.tiltpulse = int(tilt)
        elif L_or_R == 'R':
            self.panpulse = self.pan_min
            self.tiltpulse = int(tilt)
        else:
            self.reset()
            return

        self.pwm.set_pwm(1, 0, self.tiltpulse)
        self.pwm.set_pwm(0, 0, self.panpulse)

    def get_panpulse(self):
        return self.panpulse
    
    def get_tiltpulse(self):
        return self.panpulse
     
    





