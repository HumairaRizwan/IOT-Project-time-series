#Importing necessary libraries

import Adafruit_DHT      #Import the sensor module
import RPi.GPIO as GPIO  #Import the Raspberry Pi GPIO Library
import time              #Import the sleep function from the time module
import pigpio            #Import the servo motor module

pin = 4     #GPIO Pin No attached to the sensor

sensor = Adafruit_DHT.DHT22 #Defining the sensor

GPIO.setwarnings(False)  #Ignore warning for now

GPIO.setmode(GPIO.BCM)
GPIO.setup(24,GPIO.OUT) #Pin connected to Green LED
GPIO.setup(25,GPIO.OUT) #Pin connected to White LED
GPIO.setup(27,GPIO.OUT) #Pin connected to Yellow LED
GPIO.setup(22,GPIO.OUT) #Pin connected to Red LED 
GPIO.setup(23,GPIO.OUT) #Pin connected to servo motor
pwm = GPIO.PWM(23, 50)

pwm.start(0)

pi = pigpio.pi()        #Starting the servo motor
pi.set_mode(23,pigpio.OUTPUT)
    
while True:             #Run forever
    humid,temp = Adafruit_DHT.read_retry(sensor,pin) #Reading data from DHT22 sensor

    tempF = (temp * 1.8) +32 #Convertion to F

    #Calculating Heat Index
    HI = -42.379 + 2.04901523 * tempF + 10.14333127 * humid -0.22475541 * tempF * humid - 0.00683783 * tempF * tempF - 0.05481717 * humid * humid +0.00122874 * tempF * tempF * humid + 0.00085282 * tempF * humid * humid - 0.00000199 * tempF * tempF * humid * humid

    #Setting up the outputs
    if (HI >= 80 and HI < 90):
        pi.set_servo_pulsewidth(23, 750)
        print('Heat Index:{:.1f}F'.format(HI))
        GPIO.output(24, GPIO.HIGH)           #Turn ON
        time.sleep(1)                        #Sleep for 1 second
        GPIO.output(24, GPIO.LOW)            #Turn OFF
        time.sleep(1)                        #Sleep for 1 second
    elif (HI >= 90 and HI < 103 ):
        pi.set_servo_pulsewidth(23, 1250)
        print('Heat Index:{:.1f}F'.format(HI))
        GPIO.output(25, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(25, GPIO.LOW)
        time.sleep(1)
    elif (HI >= 103 and HI <= 124 ):
        pi.set_servo_pulsewidth(23, 1750)
        print('Heat Index:{:.1f}F'.format(HI))
        GPIO.output(27, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(27, GPIO.LOW)
        time.sleep(1)
    elif (HI >= 125):
        pi.set_servo_pulsewidth(23, 2250)
        print('Heat Index:{:.1f}F'.format(HI))
        GPIO.output(22, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(22, GPIO.LOW)
        time.sleep(1)
    else :
        pi.stop()
        GPIO.cleanup()
