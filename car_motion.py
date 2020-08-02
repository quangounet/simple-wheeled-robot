#! /usr/bin/env python
import  RPi.GPIO as GPIO
import time

# pins for left motor
PWMA = 18   # PWM signal (setting the left motor speed)
AIN1 = 22   # left forward
AIN2 = 27   # left backward
# pins for right motor
PWMB = 23   # PWM signal (setting the right motor speed)
BIN1 = 25   # right forward
BIN2 = 24   # right backward
        
def car_stop(t_time):
  # stop the car
  L_Motor.ChangeDutyCycle(0)
  GPIO.output(AIN2,False)
  GPIO.output(AIN1,False) 

  R_Motor.ChangeDutyCycle(0)
  GPIO.output(BIN2,False)
  GPIO.output(BIN1,False)
  time.sleep(t_time)
       
def car_motion(lspeed, rspeed, t):
  # command the car to move given left & right motor speed and duration
  if lspeed < 0:
    L_Motor.ChangeDutyCycle(-lspeed)
    GPIO.output(AIN2,True)
    GPIO.output(AIN1,False) 
  else:
    L_Motor.ChangeDutyCycle(lspeed)
    GPIO.output(AIN2,False)
    GPIO.output(AIN1,True) 
  if rspeed < 0:
    R_Motor.ChangeDutyCycle(-rspeed)
    GPIO.output(BIN2,True)
    GPIO.output(BIN1,False)
  else:
    R_Motor.ChangeDutyCycle(rspeed)
    GPIO.output(BIN2,False)
    GPIO.output(BIN1,True)

  time.sleep(t)    

# initialize
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
GPIO.setup(AIN2,GPIO.OUT)
GPIO.setup(AIN1,GPIO.OUT)
GPIO.setup(PWMA,GPIO.OUT)

GPIO.setup(BIN1,GPIO.OUT)
GPIO.setup(BIN2,GPIO.OUT)
GPIO.setup(PWMB,GPIO.OUT)

L_Motor= GPIO.PWM(PWMA,100)
L_Motor.start(0)

R_Motor = GPIO.PWM(PWMB,100)
R_Motor.start(0)

# start motion
try:
  while True:
    car_motion(40, 40, 3)
    car_motion(-40, -40, 3)
    car_stop(10)
except KeyboardInterrupt:
  GPIO.cleanup()

