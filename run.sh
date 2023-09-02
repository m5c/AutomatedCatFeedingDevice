rm acfd.zip
ssh schieder@192.168.0.191 'cd Code/AutomatedCatFeedingDevice/; rm -rf acfd'
zip -r acfd.zip acfd
scp acfd.zip schieder@192.168.0.191:/home/schieder/Code/AutomatedCatFeedingDevice
ssh schieder@192.168.0.191 'cd Code/AutomatedCatFeedingDevice; unzip acfd.zip'

## Main Program
# Commented out here. Is started via /etc/rc.local
ssh -t schieder@192.168.0.191 'cd Code/AutomatedCatFeedingDevice; python3 -m acfd.automated_cat_feeding_device'

