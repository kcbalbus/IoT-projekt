from config import *
from card_registration_display import *
import time
import RPi.GPIO as GPIO
from config import * # pylint: disable=unused-wildcard-import
from mfrc522 import MFRC522
from datetime import datetime
from post_request_card_registration import sendCardData
import neopixel
import board
from PIL import Image, ImageDraw, ImageFont
import lib.oled.SSD1331 as SSD1331

disp = SSD1331.SSD1331()
executing = True
terminate = True
card_read_active = False

def rfidRead(MIFAREReader):
    (status, _) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    if status == MIFAREReader.MI_OK:
        (status, uid) = MIFAREReader.MFRC522_Anticoll()
        if status == MIFAREReader.MI_OK:
            processScan(uid)
            while status == MIFAREReader.MI_OK:
                MIFAREReader = MFRC522()
                (status, _) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)


def processScan(uid):
    global card_read_active
    card_read_active = True
    (num, dt) = rfidScanInfo(uid)
    buzz()
    printScanInfo(num, dt)
    response = postCardRead(num)
    succesDisplay(disp, response)
    card_read_active = False


def buttonGreenPressedCallback(channel):
    global executing  

    if not card_read_active:
        executing = not executing

        if executing:
            turnOnDevice(disp)
        else:
            turnOffDevice(disp)
            
        print(executing)


def buttonRedPressedCallback(channel):
    global terminate 
    global executing
    if not card_read_active:
        executing= False
        terminate = False


def rfidScanInfo(uid):
    dt = datetime.now()
    num = 0
    for i in range(0, len(uid)):
        num += uid[i] << (i * 8)
    return (num, dt)


def printScanInfo(num, dt):
    print(f"Card read UID: {num}")
    print(f"Date and time of scan: {dt}")


def postCardRead(num):
    return sendCardData(num)


def startCardReading():
    print('Place the card close to the reader.')
    MIFAREReader = MFRC522()
    while terminate:
        while executing:
            rfidRead(MIFAREReader)


if __name__ == "__main__":
    disp.Init()
    GPIO.add_event_detect(buttonGreen, GPIO.FALLING, callback=buttonGreenPressedCallback, bouncetime=500)
    GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=buttonRedPressedCallback, bouncetime=500)
    displayInfoON(disp)
    startCardReading()
    disp.clear()