from queue import Empty
from sys import displayhook
import time
import RPi.GPIO as GPIO
from config import * 
from mfrc522 import MFRC522
from datetime import datetime
from Modules import buzz, displayLight, blink_fast_twice
from SendingPOST import notifyServerTime, validateCard, sendWeatherData
from LoadingMeteorologicalValues import initDisp, dispValues, readSensors


card_set = set()
last_send = time.time()
displ = initDisp()
executing = True

def buttonPressedCallbackRed(channel):
    global executing 
    executing = False
    global displ
    displ.clear()
    displ.reset()

def buttonPressedCallbackGreen(channel):
    global executing 
    if not executing:
        global displ
        displ = initDisp()
    executing = True
    


def RunStation():
    global executing
    if executing: MIFAREReader = MFRC522()
    while executing:
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
                if validateCard(num):
                    notifyServerTime(num)
                    notify_set(num)
                    print(card_set)
                else:
                    displayLight((255, 0, 0))
                    buzz()
                    displayLight((0, 0, 0))
                while status == MIFAREReader.MI_OK:
                    MIFAREReader = MFRC522()
                    sendDataOnce()
                    (status, _) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)


def notify_set(id):
    if id in card_set:
        card_set.remove(id)
        buzz()
        blink_fast_twice((0, 0, 255))
        if not card_set:
            displ.clear()
    else:
        card_set.add(id)
        buzz()
        blink_fast_twice((0, 255, 0))


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

def main():
    GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=buttonPressedCallbackRed,bouncetime=500)
    GPIO.add_event_detect(buttonGreen, GPIO.FALLING, callback=buttonPressedCallbackGreen,bouncetime=500)
    while True:
        RunStation()
        


if __name__ == "__main__":
    main()
