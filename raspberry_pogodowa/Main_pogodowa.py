from queue import Empty
from sys import displayhook
import time
import RPi.GPIO as GPIO
from config import * 
from mfrc522 import MFRC522
from datetime import datetime
from Card import buzz
from SendingPOST import notifyServerTime, validateCard, sendWeatherData
from LoadingMeteorologicalValues import initDisp, dispValues, readSensors


card_set = set()
last_send = time.time()
global displ
displ = initDisp()

def ScanCard():
    MIFAREReader = MFRC522()
    while True:
        sendDataOnce()
        (status, _) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        if status == MIFAREReader.MI_OK:
            (status, uid) = MIFAREReader.MFRC522_Anticoll()
            if status == MIFAREReader.MI_OK:
                dt = datetime.now()
                num = 0
                for i in range(0, len(uid)):
                    num += uid[i] << (i*8)
                print(f"Card read UID: {num}")
                print(f"Date and time of scan: {dt}")
                buzz()
                if validateCard(num):
                    notifyServerTime(num)
                    notify_set(num)
                    print(card_set)
                while status == MIFAREReader.MI_OK:
                    MIFAREReader = MFRC522()
                    sendDataOnce()
                    (status, _) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)


def notify_set(id):
    if id in card_set:
        card_set.remove(id)
    else:        
        card_set.add(id)


def sendDataOnce():
    global last_send
    curr_time = time.time()
    if card_set and (curr_time - last_send > 10):
        last_send = curr_time
        sendWeatherData()
        showWeatherData()


def showWeatherData():

    (tem, hum, press) = readSensors()
    dispValues(tem, hum, press, displ)


if __name__ == "__main__":
    ScanCard()
