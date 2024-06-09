import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import pigpio

servo_pin = 23
pin = 4
greenled = 24
whiteled = 25
yellowled = 27
redled = 22
sensor = Adafruit_DHT.DHT22
GPIO.setmode(GPIO.BCM)
GPIO.setup(greenled,GPIO.OUT)
GPIO.setup(whiteled,GPIO.OUT)
GPIO.setup(yellowled,GPIO.OUT)
GPIO.setup(redled,GPIO.OUT)
GPIO.setup(servo_pin,GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)
pi = pigpio.pi()
pi.set_mode(servo_pin,pigpio.OUTPUT)

       
humid,temp = Adafruit_DHT.read_retry(sensor,pin)

tempF = (temp * 1.8) +32

HI = -42.379 + 2.04901523 * tempF + 10.14333127 * humid -0.22475541 * tempF * humid - 0.00683783 * tempF * tempF - 0.05481717 * humid * humid +0.00122874 * tempF * tempF * humid + 0.00085282 * tempF * humid * humid - 0.00000199 * tempF * tempF * humid * humid


if (HI >= 80 and HI < 90):
    pi.set_servo_pulsewidth(servo_pin, 750)
    print('Temperature:{:.1f}C'.format(HI))
    GPIO.output(greenled, GPIO.HIGH)
    time.sleep(1)
elif (HI >= 90 and HI < 103 ):
    pi.set_servo_pulsewidth(servo_pin, 1250)
    print('Temperature:{:.1f}Chum'.format(HI))
    GPIO.output(whiteled, GPIO.LOW)
    time.sleep(1)
elif (HI >= 103 and HI <= 124 ):
    pi.set_servo_pulsewidth(servo_pin, 1750)
    print('Temperature:{:.1f}Chum'.format(HI))
    GPIO.output(yellowled, GPIO.HIGH)
    time.sleep(1)
elif (HI >= 125):
    pi.set_servo_pulsewidth(servo_pin, 2250)
    print('Temperature:{:.1f}Chum'.format(HI))
    GPIO.output(redled, GPIO.HIGH)
    time.sleep(1)
