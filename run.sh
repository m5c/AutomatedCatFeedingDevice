ssh -t schieder@192.168.0.156 'cd Code/AutomatedCatFeedingDevice/; rm -rf acfd; mkdir acfd'
scp -rp acfd schieder@192.168.0.156:/home/schieder/Code/AutomatedCatFeedingDevice/

## Tests
#ssh -t schieder@192.168.0.156 'cd Code/AutomatedCatFeedingDevice/acfd; python3 modules/button-test.py; bash -l'
#ssh -t schieder@192.168.0.156 'cd Code/AutomatedCatFeedingDevice/acfd; python3 modules/motor-test.py; bash -l'
ssh -t schieder@192.168.0.156 'cd Code/AutomatedCatFeedingDevice; python3 acfd/segment-individual-test.py; bash -l'
#ssh -t schieder@192.168.0.156 'cd Code/AutomatedCatFeedingDevice/acfd; python3 modules/display-test.py; bash -l'

## Main Program
#ssh -t schieder@192.168.0.156 'cd Code/AutomatedCatFeedingDevice/acfd; python3 acfd.py; bash -l'

