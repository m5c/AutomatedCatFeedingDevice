ssh -t schieder@192.168.0.190 'cd Code/AutomatedCatFeedingDevice/; rm -rf acfd; mkdir acfd'
scp -rp acfd schieder@192.168.0.190:/home/schieder/Code/AutomatedCatFeedingDevice/

## Tests
ssh -t schieder@192.168.0.190 'cd Code/AutomatedCatFeedingDevice; python3 acfd/segment-individual-test.py; bash -l'
#ssh -t schieder@192.168.0.190 'cd Code/AutomatedCatFeedingDevice; python3 acfd/motor-test.py; bash -l'
#ssh -t schieder@192.168.0.190 'cd Code/AutomatedCatFeedingDevice; python3 acfd/buttons-test.py; bash -l'

## Main Program
#ssh -t schieder@192.168.0.190 'cd Code/AutomatedCatFeedingDevice/acfd; python3 acfd.py; bash -l'

