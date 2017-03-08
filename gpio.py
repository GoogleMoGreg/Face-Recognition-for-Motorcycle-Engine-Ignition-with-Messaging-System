import RPi.GPIO as GPIO
import time


pinRed = 20
pinGreen = 21
pinYellow = 12
pinFlashlight = 23
GPIO.setmode(GPIO.BCM)       
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pinRed,GPIO.OUT)
GPIO.setup(pinGreen,GPIO.OUT)
GPIO.setup(pinYellow,GPIO.OUT)
GPIO.setup(pinFlashlight,GPIO.OUT)

def RED_ON():
    GPIO.output(pinRed,GPIO.HIGH)
    time.sleep(0.05)
    return

def RED_OFF():
    time.sleep(0.05)
    GPIO.output(pinRed,GPIO.LOW)
    return

def GREEN_ON():
    GPIO.output(pinGreen,GPIO.HIGH)
    #time.sleep(0.051)
    return

def GREEN_OFF():
    #time.sleep(0.051)
    GPIO.output(pinGreen,GPIO.LOW)
    return

def SWITCH():
    button = 16
    GPIO.setup(button,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
    if (GPIO.input(button)):
         button = 'ON'
    else:
        button = 'OFF'

    return button
    
def FADE_YELLOW():

    p = GPIO.PWM(pinYellow,50)
    p.start(0)

    for i in range (50):
        p.ChangeDutyCycle(i)
        time.sleep(0.01)
    for i in range (50):
        p.ChangeDutyCycle(50-i)
        time.sleep(0.01)
    return

def YELLOW_ON():
    GPIO.output(pinYellow,GPIO.HIGH)
    time.sleep(0.05)
    return

def YELLOW_OFF():
    time.sleep(0.05)
    GPIO.output(pinYellow,GPIO.LOW)
    return 
    
def FLASHLIGHT_ON():
    GPIO.output(pinFlashlight,GPIO.HIGH)
    time.sleep(0.05)
    return

def FLASHLIGHT_OFF():
    GPIO.output(pinFlashlight,GPIO.LOW)
    time.sleep(0.05)
    return

def MASTER_SWITCH():
    button = 24
    GPIO.setup(button,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
    if (GPIO.input(button)):
         switch_state = 'ON'
    else:
        switch_state = 'OFF'

    return switch_state

def ENGINE_SWITCH():
    button = 19
    GPIO.setup(button,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
    if (GPIO.input(button)):
         switch_state = 'ON'
    else:
        switch_state = 'OFF'
    return switch_state

