# Waiting time between stepper motor steps.
step_time = 0.002

# STEPPER MOTOR PINS (and modes)
# ULN2003 "-" goes to +5V pin, ULN2003 "+" goes to GND pin.
# ULN2003 mappings to GPIO pins:
IN1 = 21
IN2 = 26
IN3 = 20
IN4 = 19
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
# Initialize all pins with false, to prevent random movement at program start.
GPIO.output(IN1, False)
GPIO.output(IN2, False)
GPIO.output(IN3, False)
GPIO.output(IN4, False)


# Define stepper motor sequential step functions
def step_1():
    GPIO.output(IN4, True)
    sleep(steptime)
    GPIO.output(IN4, False)


def step_2():
    GPIO.output(IN4, True)
    GPIO.output(IN3, True)
    sleep(steptime)
    GPIO.output(IN4, False)
    GPIO.output(IN3, False)


def step_3():
    GPIO.output(IN3, True)
    sleep(steptime)
    GPIO.output(IN3, False)


def step_4():
    GPIO.output(IN2, True)
    GPIO.output(IN3, True)
    sleep(steptime)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)


def step_5():
    GPIO.output(IN2, True)
    sleep(steptime)
    GPIO.output(IN2, False)


def step_6():
    GPIO.output(IN1, True)
    GPIO.output(IN2, True)
    sleep(steptime)
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)


def step_7():
    GPIO.output(IN1, True)
    sleep(steptime)
    GPIO.output(IN1, False)


def step_8():
    GPIO.output(IN4, True)
    GPIO.output(IN1, True)
    sleep(steptime)
    GPIO.output(IN4, False)
    GPIO.output(IN1, False)


# Rotate counter-clockwise
def left(step):
    for i in range(step):
        step_1()
        step_2()
        step_3()
        step_4()
        step_5()
        step_6()
        step_7()
        step_8()


# Rotate clock-wise
def right(step):
    for i in range(step):
        step_8()
        step_7()
        step_6()
        step_5()
        step_4()
        step_3()
        step_2()
        step_1()


# custom function to open lid (perfect angle)
def open_lid():
    right(170)


# custom function to close lid (perfect angle)
def close_lid():
    left(170)