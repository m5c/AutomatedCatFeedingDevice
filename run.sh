rm acfd.zip
ssh schieder@192.168.0.191 'cd Code/AutomatedCatFeedingDevice/; rm -rf acfd'
zip -r acfd.zip acfd
scp acfd.zip schieder@192.168.0.191:/home/schieder/Code/AutomatedCatFeedingDevice
ssh schieder@192.168.0.191 'cd Code/AutomatedCatFeedingDevice; unzip acfd.zip'

## Tests
ssh -t schieder@192.168.0.191 'cd Code/AutomatedCatFeedingDevice; python3 acfd/display_test.py; bash -l'
#ssh schieder@192.168.0.191 'cd Code/AutomatedCatFeedingDevice; python3 acfd/segment_individual_test.py'
#ssh schieder@192.168.0.191 'cd Code/AutomatedCatFeedingDevice; python3 acfd/motor_test.py'
#ssh schieder@192.168.0.191 'cd Code/AutomatedCatFeedingDevice; python3 acfd/buttons_test.py; bash -l'

## Main Program
#ssh schieder@192.168.0.191 'cd Code/AutomatedCatFeedingDevice/acfd; python3 acfd.py; bash -l'

