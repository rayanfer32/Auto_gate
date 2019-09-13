import picamera,time 
from openalpr import Alpr
import time 
import os
import requests
import RPi.GPIO as GPIO

#pwmPin = 18 # Broadcom pin 18 (P1 pin 12)
#butPin = 17 # Broadcom pin 17 (P1 pin 11)
gatemotor = 23 # Broadcom pin 23 (P1 pin 16)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(gatemotor, GPIO.OUT) # LED pin set as output

alpr = Alpr("in", "/etc/openalpr/openalpr.conf", "openalpr/runtime_data/")
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

def check(car_no):
    if car_no in open('residents.txt').read():
        print(">>>>>")
        return "resident"
    else:
        print("!!!")
        return "visitor"

def open_gate():
    #open gate
    GPIO.output(gatemotor, GPIO.HIGH)
    print("////////////OPEN//////////////")
    time.sleep(8)
    print("\\\\\\\\\\\\\CLOSE\\\\\\\\\\\\")
    GPIO.output(gatemotor, GPIO.LOW)

def start_recog():
    alpr.set_top_n(20)
    alpr.set_default_region("in") 
    results = alpr.recognize_file("/home/pi/carplate.jpg")
    print("recognizing")
    cur_car = "visitor"
    i = 0
    for plate in results['results']:
        i += 1
        print("Plate #%d" % i)
        print("   %12s %12s" % ("Plate", "Confidence"))
        print
        for candidate in plate['candidates']:
            prefix = "-"
            if candidate['matches_template']:
                prefix = "*"
                
            
            print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))
            
            cur_car = check(candidate['plate'])
            if(cur_car == "resident"):
                break
    return cur_car


while 1:
    #using webcam
    os.system('fswebcam -r 320x240 -S 30 --jpeg 50 --save /home/pi/carplate.jpg')

    #recognize the file from local
    car = start_recog()
    print("This is "+car+" Car")
    if(car == "resident"):
        open_gate()
    
    
