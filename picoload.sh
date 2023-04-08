cat digit.py 
cp acfd/segment-individual-test.py main.py
rshell --buffer-size=30 -p /dev/tty.usbmodem14201 cp main.py /pyboard
rm main.py
