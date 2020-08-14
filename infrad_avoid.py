#!/usr/bin/python   
import RPi.GPIO as GPIO  
import time  

# ==========================================================
# Obstacle avoidance with left & right IR sensor
# ==========================================================

# Pin number indication
# IR sensors
SensorRight = 16    # right IR sensor
SensorLeft  = 12    # left IR sensor

# Motors
# pins for left motor
PWMA = 18   # PWM signal (setting the left motor speed)
AIN1 = 22   # left forward
AIN2 = 27   # left backward
# pins for right motor
PWMB = 23   # PWM signal (setting the right motor speed)
BIN1 = 25   # right forward
BIN2 = 24   # right backward

# Button and LED indicator
BtnPin = 19    # functional button to initiate the process
Rpin   = 5     # red LED indicator
Gpin   = 6     # green LED indicator
 
def t_forward(speed, t):
  L_Motor.ChangeDutyCycle(speed)
  GPIO.output(AIN2, False) 
  GPIO.output(AIN1, True)  

  R_Motor.ChangeDutyCycle(speed)
  GPIO.output(BIN2, False) 
  GPIO.output(BIN1, True)  
  time.sleep(t)
        
def t_stop(t):
  L_Motor.ChangeDutyCycle(0)
  GPIO.output(AIN2, False) 
  GPIO.output(AIN1, False)  

  R_Motor.ChangeDutyCycle(0)
  GPIO.output(BIN2, False) 
  GPIO.output(BIN1, False)  
  time.sleep(t)
        
def t_backward(speed, t):
  L_Motor.ChangeDutyCycle(speed)
  GPIO.output(AIN2, True) 
  GPIO.output(AIN1, False)  

  R_Motor.ChangeDutyCycle(speed)
  GPIO.output(BIN2, True) 
  GPIO.output(BIN1, False)  
  time.sleep(t)

def t_left(speed, t):
  L_Motor.ChangeDutyCycle(speed)
  GPIO.output(AIN2, True)
  GPIO.output(AIN1, False) 

  R_Motor.ChangeDutyCycle(speed)
  GPIO.output(BIN2, False)
  GPIO.output(BIN1, True) 
  time.sleep(t)

def t_right(speed, t):
  L_Motor.ChangeDutyCycle(speed)
  GPIO.output(AIN2, False)
  GPIO.output(AIN1, True) 

  R_Motor.ChangeDutyCycle(speed)
  GPIO.output(BIN2, True)
  GPIO.output(BIN1, False) 
  time.sleep(t)

def buttonscan():
  """ Detect whether onboard button is pressed to activate the process
  """
  val = GPIO.input(BtnPin)
  while GPIO.input(BtnPin) == False:
    val = GPIO.input(BtnPin)
  while GPIO.input(BtnPin) == True:   # button pressed - green light on
    time.sleep(0.01)  # introduce time delay to eliminate false detection
    val = GPIO.input(BtnPin)
    if val == True:
      GPIO.output(Gpin,1)
    else:   # button released - green light off
      GPIO.output(Gpin,0)
            
def setup():
  """ Set up input/output declaration for pins
  """
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)         # Number GPIOs by physical location
  # Button and LED
  GPIO.setup(Gpin, GPIO.OUT)     
  GPIO.setup(Rpin, GPIO.OUT)     
  GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set button pin to input, and pull up to high 
  # IR sensors
  GPIO.setup(SensorRight, GPIO.IN)
  GPIO.setup(SensorLeft, GPIO.IN)
  # motors
  # left motors
  GPIO.setup(AIN2, GPIO.OUT)
  GPIO.setup(AIN1, GPIO.OUT)
  GPIO.setup(PWMA, GPIO.OUT)
  # right motors
  GPIO.setup(BIN1, GPIO.OUT)
  GPIO.setup(BIN2, GPIO.OUT)
  GPIO.setup(PWMB, GPIO.OUT)

if __name__ == '__main__':
  setup()
  L_Motor= GPIO.PWM(PWMA, 100)
  L_Motor.start(0)
  R_Motor = GPIO.PWM(PWMB, 100)
  R_Motor.start(0)
  buttonscan()   # must put after motor initialization
  try:
    while True:
      SR_2 = GPIO.input(SensorRight)
      SL_2 = GPIO.input(SensorLeft)
      if SL_2 == True and SR_2 == True:
        print("Move forward")
        t_forward(50, 0)
      elif SL_2 == True and SR_2 == False:
        print ("Turn left")
        t_left(50, 0)
      elif SL_2 == False and SR_2 == True:
        print("Turn right")
        t_right(50, 0)
      else:
        t_stop(0.3)
        t_backward(50, 0.4)
        t_left(50, 0.5)
  except KeyboardInterrupt:  # 'Ctrl+C' to kill the process
      GPIO.cleanup()
