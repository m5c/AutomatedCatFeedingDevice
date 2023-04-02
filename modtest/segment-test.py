import queue
import threading
import time

import RPi.GPIO as GPIO

from modtest.segment import Segment

GPIO.setmode(GPIO.BCM)


#                 A   B   C  D    E   F   G
seg: list[int] = [s.value for s in Segment]
digit: list[int] = [2, 3, 4, 14]

# indicates which segments must light up for digits 0-9
numbers: list[list[int]] = [[15, 24, 18, 22, 23, 17], [24, 18], [15, 24, 22, 23, 27], [15, 24, 18, 22, 27],
          [24, 18, 17, 27], [15, 18, 22, 17, 27], [18, 22, 23, 17, 27], [15, 24, 18],
          [15, 24, 18, 22, 23, 17, 27], [15, 24, 18, 17, 27]]

## INIT
# reset dot segement output
GPIO.setup(10, GPIO.OUT, initial=0)

# reset GPIO pins for all segments to 0. (off)
for s in range(len(seg)):
    GPIO.setup(seg[s], GPIO.OUT, initial=0)

# reset GPIO pins for all digits to 1. (not selected)
for s in range(len(gnd)):
    GPIO.setup(gnd[s], GPIO.OUT, initial=1)

## COUNT DOWN THREAD (MUST NOT BLOCK)
# starts with 1h 1 minute
counter = 101
hours = True
t = threading.Thread(target=thread_function, args=(counter,))
t.start()

## MAIN CONTROL
print('CTRL-C to terminate')
try:
    while (counter > 0):

        # update counter if changed
        if not q.empty():
            counter = q.get()

        # i is the digit iterator
        for i in range(len(gnd)):

            # activate digit i
            GPIO.output(gnd[i], 0)

            # compute what to display on that digit
            digit = counter // pow(10, 3 - i) % 10

            # Light up all segments that correspond to number "i"
            for seg in range(len(digits[digit])):
                GPIO.output(digits[digit][seg], 1)

            # Light up dot separator if curret digit is second position
            if i == 1:
                GPIO.output(10, 1)

            time.sleep(0.005)

            # switch digit off again
            GPIO.output(gnd[i], 1)

            # Switch dot separator off again
            GPIO.output(10, 0)

            # reset all segments that were lit up
            for seg in range(len(digits[digit])):
                GPIO.output(digits[digit][seg], 0)

except KeyboardInterrupt:
    GPIO.cleanup()

