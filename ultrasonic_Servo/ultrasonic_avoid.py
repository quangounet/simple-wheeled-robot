#!/usr/bin/env python
from Adafruit_PWM_Servo_Driver import PWM
import RPi.GPIO as GPIO
import time

# ==========================================================
# Obstacle avoidance with ultrasonic sensor
# ==========================================================
# ! Make sure to enable I2C on the Raspberry Pi!

# Pin number indication
# pins for left motor
PWMA = 18     # PWM signal (setting the left motor speed)
AIN1 = 22     # left forward
AIN2 = 27     # left backward
# pins for right motor
PWMB = 23     # PWM signal (setting the right motor speed)
BIN1 = 25     # right forward
BIN2 = 24     # right backward

# Button and LED indicator
BtnPin = 19    # functional button to initiate the process
Rpin   = 5     # red LED indicator
Gpin   = 6     # green LED indicator

# Ultrasonic
TRIG = 20      # triggering signal
ECHO = 21      # echo signal

FREQ = 50      # set PWM frequency to 50Hz

# Initialize PWM using the default address
pwm = PWM(0x40, debug = False)

def angle2pulse(angle):
  """ servo head angle to PWM pulse width (us) conversion
  """
  pulse = angle / 90.0 + 0.5
  pulse = max(pulse, 0.5)   # min limit 0.5 -- 0 degree
  pulse = min(pulse, 2.5)   # max limit 2.5 -- 180 degree
  return pulse*1000

def setServoPulse(channel, angle):
  """ Turn the servo head to desired orientation
  """
  pulse = angle2pulse(angle)
  pulseLength = 1.0 / FREQ * 10**6             # us
  print("%d us per period" % pulseLength)
  pulseLength /= 4096.0                     # 12-bit resolution
  print("%d us per bit" % pulseLength)
  pulse /= pulseLength
  print("pulse: %f  " % (pulse))
  pwm.setPWM(channel, 0, int(pulse))

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
  """ Detect whether onboard button is pressed to activate the process.
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
  # Ultrasonic
  GPIO.setup(TRIG, GPIO.OUT)
  GPIO.setup(ECHO, GPIO.IN)
  # Button and LED
  GPIO.setup(Gpin, GPIO.OUT)     
  GPIO.setup(Rpin, GPIO.OUT)     
  GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set button pin to input, and pull up to high 
  # motors
  # left motors
  GPIO.setup(AIN2, GPIO.OUT)
  GPIO.setup(AIN1, GPIO.OUT)
  GPIO.setup(PWMA, GPIO.OUT)
  # right motors
  GPIO.setup(BIN1, GPIO.OUT)
  GPIO.setup(BIN2, GPIO.OUT)
  GPIO.setup(PWMB, GPIO.OUT)
  pwm.setPWMFreq(FREQ) 
        
def distance():
  """ Calculate distance to obstacle (cm)
  """
  GPIO.output(TRIG, 0)
  time.sleep(0.000002)
  # Send a triggering signal (~10us)
  GPIO.output(TRIG, 1)    
  time.sleep(0.00001)
  GPIO.output(TRIG, 0)
  # Wait until echo signal received
  while GPIO.input(ECHO) == 0:
    a = 0
  # Echo signal received
  time1 = time.time()
  while GPIO.input(ECHO) == 1:
    a = 1
  time2 = time.time()
  dt = time2 - time1
  return dt * 340 / 2 * 100

def front_detection():
  """ front obstacle detection: 90 degree
  """
  setServoPulse(0, 90)
  time.sleep(0.5)
  dis_f = distance()
  return dis_f

def left_detection():
  """ left obstacle detection: 175 degree
  """
  setServoPulse(0, 175)
  time.sleep(0.5)
  dis_l = distance()
  return dis_l
        
def right_detection():
  """ right obstacle detection: 5 degree
  """
  setServoPulse(0, 5)
  time.sleep(0.5)
  dis_r = distance()
  return dis_r
     
def move():
  """ Move car around and avoid obstacle
  """
  while True:
    dis1 = front_detection()
    if (dis1 < 40) == True:
      t_stop(0.2)
      t_backward(50, 0.5)
      t_stop(0.2)
      dis2 = left_detection()
      dis3 = right_detection()
      if (dis2 < 40) == True and (dis3 < 40) == True:
        t_backward(50, 1)
        t_left(50, 0.3)
      elif (dis2 > dis3) == True:
        t_left(50, 0.3)
        t_stop(0.1)
      else:
        t_right(50, 0.3)
        t_stop(0.1)
    else:
      t_forward(50, 0)

if __name__ == "__main__":
  setup()
  L_Motor= GPIO.PWM(PWMA, 100)
  L_Motor.start(0)
  R_Motor = GPIO.PWM(PWMB, 100)
  R_Motor.start(0)
  buttonscan()
  try:
    move()
  except KeyboardInterrupt:   # press "Ctrl+C" to kill the process
    GPIO.cleanup()
