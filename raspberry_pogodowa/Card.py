import time
import RPi.GPIO as GPIO
from config import * # pylint: disable=unused-wildcard-import
from mfrc522 import MFRC522
from datetime import datetime

def buzz():
    GPIO.output(buzzerPin, False)
    time.sleep(1)
    GPIO.output(buzzerPin, True)

def blink():
    GPIO.output(led1, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(led1, GPIO.LOW)

def rfidRead():
    MIFAREReader = MFRC522()
    while True:
        (status, _) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        if status == MIFAREReader.MI_OK:
            (status, uid) = MIFAREReader.MFRC522_Anticoll()
            if status == MIFAREReader.MI_OK:
                dt = datetime.now()
                num = 0
                for i in range(0, len(uid)):
                    num += uid[i] << (i*8)
                print(f"Card read UID: {num}")
                buzz()
                blink()
                print(f"Date and time of scan: {dt}")
                while status == MIFAREReader.MI_OK:
                    MIFAREReader = MFRC522()
                    (status, _) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)



def test():

    print('Place the card close to the reader.')
    rfidRead()


if __name__ == "__main__":
    test()
