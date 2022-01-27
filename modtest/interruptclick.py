#!/usr/bin/python
# See roboticsbacked.com/raspberry-pi-gpio-interrupts-tutorial/
import RPi.GPIO as GPIO
import signal
import sys




# Def handler to be called on ctrl-C event
def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

# Define handler for button press (channel is the GPIO that registered RISING signal)
def button_pressed_callback(channel):
    if channel==taster1:
        print("1")
    if channel==taster2:
        print("2")
    if channel==taster3:
        print("3")
    if channel==taster4:
        print("4")


#Set up GPIO pins and make RISING / FALLING events call butten pressed handler
if __name__ == '__main__':
    # PIN layout
    keypadPower=7
    taster1=9
    taster2=25
    taster3=8
    taster4=11
    

    # Set PIN IO modes
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(keypadPower, GPIO.OUT)
    GPIO.setup(taster1, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(taster2, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(taster3, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(taster4, GPIO.IN, GPIO.PUD_DOWN)
    
    # Power up 3.3V input oin
    GPIO.output(keypadPower, 1)

    # Add handlers
    GPIO.add_event_detect(taster1, GPIO.RISING, callback=button_pressed_callback, bouncetime=100)
    GPIO.add_event_detect(taster2, GPIO.RISING, callback=button_pressed_callback, bouncetime=100)
    GPIO.add_event_detect(taster3, GPIO.RISING, callback=button_pressed_callback, bouncetime=100)
    GPIO.add_event_detect(taster4, GPIO.RISING, callback=button_pressed_callback, bouncetime=100)

    # Add ctrl-c listener
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()



