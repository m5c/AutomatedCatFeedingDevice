scp modtest/* schieder@192.168.0.156:/home/schieder/Code/AutomatedCatFeedingDevice/modtest/
scp acfd.py schieder@192.168.0.156:/home/schieder/Code/AutomatedCatFeedingDevice/acfd.py
#ssh -t schieder@192.168.0.156 'cd Code/AutomatedCatFeedingDevice/modtest; python3 buttons-test.py; bash -l'
#ssh -t schieder@192.168.0.156 'cd Code/AutomatedCatFeedingDevice/modtest; python3 display-test.py; bash -l'
ssh -t schieder@192.168.0.156 'cd Code/AutomatedCatFeedingDevice/modtest; python3 segment-test.py; bash -l'
#ssh -t schieder@192.168.0.156 'cd Code/AutomatedCatFeedingDevice; python3 acfd.py; bash -l'

