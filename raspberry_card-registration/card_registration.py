from config import *
from card_registration_display import *
import time
import RPi.GPIO as GPIO
from config import * # pylint: disable=unused-wildcard-import
from mfrc522 import MFRC522
from datetime import datetime
from sendingPost import sendCardData
import neopixel
import board
from PIL import Image, ImageDraw, ImageFont
import lib.oled.SSD1331 as SSD1331

global disp

def rfidRead(MIFAREReader):
    (status, _) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    if status == MIFAREReader.MI_OK:
        (status, uid) = MIFAREReader.MFRC522_Anticoll()
        if status == MIFAREReader.MI_OK:
            processScan(uid)
            while status == MIFAREReader.MI_OK:
                pass


def processScan(uid):
    (num, dt) = rfidScanInfo(uid)
    buzz()
    printScanInfo(num, dt)
    response = cardRead(num)
    succesDisplay(response)


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
    while True:
        rfidRead(MIFAREReader)


if __name__ == "__main__":
    global disp
    disp = SSD1331.SSD1331()
    disp.Init()
    displayInfo()
    startCardReading()