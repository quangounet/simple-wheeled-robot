#! /usr/bin/env python
import  RPi.GPIO as GPIO
import time

PWMA = 18
AIN1   =  22
AIN2   =  27

PWMB = 23
BIN1   = 25
BIN2  =  24

def t_up(speed,t_time):
  L_Motor.ChangeDutyCycle(speed)
  GPIO.output(AIN2,False)
  GPIO.output(AIN1,True) 

  R_Motor.ChangeDutyCycle(speed)
  GPIO.output(BIN2,False)
  GPIO.output(BIN1,True) 
  time.sleep(t_time)
        
def t_stop(t_time):
  L_Motor.ChangeDutyCycle(0)
  GPIO.output(AIN2,False)
  GPIO.output(AIN1,False) 

  R_Motor.ChangeDutyCycle(0)
  GPIO.output(BIN2,False)
  GPIO.output(BIN1,False)
  time.sleep(t_time)
        
def t_down(speed,t_time):
  L_Motor.ChangeDutyCycle(speed)
  GPIO.output(AIN2,True)
  GPIO.output(AIN1,False) 

  R_Motor.ChangeDutyCycle(speed)
  GPIO.output(BIN2,True)
  GPIO.output(BIN1,False)
  time.sleep(t_time)

def t_left(speed,t_time):
  L_Motor.ChangeDutyCycle(speed)
  GPIO.output(AIN2,True)
  GPIO.output(AIN1,False) 

  R_Motor.ChangeDutyCycle(speed)
  GPIO.output(BIN2,False)
  GPIO.output(BIN1,True) 
  time.sleep(t_time)

def t_right(speed,t_time):
  L_Motor.ChangeDutyCycle(speed)
  GPIO.output(AIN2,False)
  GPIO.output(AIN1,True) 

  R_Motor.ChangeDutyCycle(speed)
  GPIO.output(BIN2,True)
  GPIO.output(BIN1,False) 
  time.sleep(t_time)    
  
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

try:
  while True:
    t_up(50,3)
    t_down(50,3)
    t_left(50,3)
    t_right(50,3)
    t_stop(10)
except KeyboardInterrupt:
  GPIO.cleanup()

