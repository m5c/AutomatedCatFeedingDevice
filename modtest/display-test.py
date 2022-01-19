#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import threading, queue

GPIO.setmode(GPIO.BCM)

# GNDs        | SEGs
# x  x  x  Ye | Pu Wh x  Br Gr
# x  Br Re Or | x  Bl Gr Bl

# schema: 
# IO-15 R S-A
# IO-24 R S-B
# IO-18 R S-C
# IO-22 R S-D
# IO-23 R S-E
# IO-17 R S-F
# IO-27 R S-G
# -----------
# IO-02 - S-1
# IO-03 - S-2
# IO-04 - S-3
# IO-14 - S-4

##
q = queue.Queue()

## HELPER THREAD FUNCTION FOR COUNTDOWN
def thread_function(counter):
    print("Thread started.")
    while counter >= 0:
        print(counter)
        q.put(counter)

        # in hour mode, hour counter
        global hours
        if hours:
            # second counter only goes up to 59.
            # leave minutes, apply mod 60 on seconds
            counter = counter - 1
            hour = counter // 100
            minute = (counter % 100)
            if minute > 60:
                minute = 59
            counter = hour * 100 + minute
            time.sleep(60)
            if counter == 100:
                counter = 6000
                hours = False
        else:
            # second counter only goes up to 59.
            # leave minutes, apply mod 60 on seconds
            counter = counter - 1
            minute = counter // 100
            second = (counter % 100)
            if second > 60:
                second = 59
            counter = minute * 100 + second
            time.sleep(1)

    print("Thread finished.")

#     A  B    C  D   E   F   G
seg=[15, 24, 18, 22, 23, 17, 27]
gnd=[2, 3, 4, 14]

# indicates which segments must light up for digits 0-9
digits=[[15, 24, 18, 22, 23, 17], [24, 18], [15, 24, 22, 23, 27], [15, 24, 18, 22, 27], [24, 18, 17, 27], [15, 18, 22, 17, 27], [18, 22, 23, 17, 27], [15, 24, 18], [15, 24, 18, 22, 23, 17, 27], [15, 24, 18, 17, 27]]

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
            digit = counter // pow(10, 3-i) % 10

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

