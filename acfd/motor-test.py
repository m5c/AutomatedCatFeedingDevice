#!/usr/bin/env python
# coding: latin-1
# Ingmar Stapel
# Date: 20170615
# Version Alpha 0.1
# Decision Maker
# original source: github.com/custom/build-robots/Stepper-motor-28BYJ-48-Raspberry-Pi 

from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# Verwendete Pins des ULN2003A auf die Pins des Raspberry Pi
# zugeordnet
motor_pins: list[int] = [1, 2, 3, 4, 14]
# motor_pins[1=21 # motor_pins[1
# motor_pins[2=26 # motor_pins[2
# motor_pins[3=20 # motor_pins[3
# motor_pins[4=19 # motor_pins[4
# - goes to +5V, + goes to GND

# Wartezeit regelt die Geschwindigkeit wie schnell sich der Motor
# dreht.
time = 0.002

# Pins aus Ausgänge definieren
GPIO.setup(motor_pins[1], GPIO.OUT)
GPIO.setup(motor_pins[2], GPIO.OUT)
GPIO.setup(motor_pins[3], GPIO.OUT)
GPIO.setup(motor_pins[4], GPIO.OUT)
# Alle Pins werden initial auf False gesetzt. So dreht sich der 
# Stepper-Motor nicht sofort irgendwie.
GPIO.output(motor_pins[1], False)
GPIO.output(motor_pins[2], False)
GPIO.output(motor_pins[3], False)
GPIO.output(motor_pins[4], False)


# Der Schrittmotoren 28BYJ-48 ist so aufgebaut, das der Motor im
# Inneren 8 Schritte für eine Umdrehung benötigt. Durch die Betriebe
# benätigt es aber 512 x 8 Schritte damit die Achse sich einmal um
# sich selbt also 360° dreht.

# Definition der Schritte 1 - 8 über die Pins motor_pins[1 bis motor_pins[4
# Zwischen jeder Bewegung des Motors wird kurz gewartet damit der
# Motoranker seine Position erreicht.
def Step1():
    GPIO.output(motor_pins[4], True)
    sleep(time)
    GPIO.output(motor_pins[4], False)


def Step2():
    GPIO.output(motor_pins[4], True)
    GPIO.output(motor_pins[3], True)
    sleep(time)
    GPIO.output(motor_pins[4], False)
    GPIO.output(motor_pins[3], False)


def Step3():
    GPIO.output(motor_pins[3], True)
    sleep(time)
    GPIO.output(motor_pins[3], False)


def Step4():
    GPIO.output(motor_pins[2], True)
    GPIO.output(motor_pins[3], True)
    sleep(time)
    GPIO.output(motor_pins[2], False)
    GPIO.output(motor_pins[3], False)


def Step5():
    GPIO.output(motor_pins[2], True)
    sleep(time)
    GPIO.output(motor_pins[2], False)


def Step6():
    GPIO.output(motor_pins[1], True)
    GPIO.output(motor_pins[2], True)
    sleep(time)
    GPIO.output(motor_pins[1], False)
    GPIO.output(motor_pins[2], False)


def Step7():
    GPIO.output(motor_pins[1], True)
    sleep(time)
    GPIO.output(motor_pins[1], False)


def Step8():
    GPIO.output(motor_pins[4], True)
    GPIO.output(motor_pins[1], True)
    sleep(time)
    GPIO.output(motor_pins[4], False)
    GPIO.output(motor_pins[1], False)


# Umdrehung links herum
def left(step):
    for i in range(step):
        # os.system('clear') # verlangsamt die Bewegung des Motors zu sehr.
        Step1()
        Step2()
        Step3()
        Step4()
        Step5()
        Step6()
        Step7()
        Step8()
        print("Step left: ", i)


# Umdrehung rechts herum
def right(step):
    for i in range(step):
        # os.system('clear') # verlangsamt die Bewegung des Motors zu sehr.
        Step8()
        Step7()
        Step6()
        Step5()
        Step4()
        Step3()
        Step2()
        Step1()
        print("Step right: ", i)


def openlid():
    right(170)


def closelid():
    left(170)


openlid()
closelid()

GPIO.cleanup()
