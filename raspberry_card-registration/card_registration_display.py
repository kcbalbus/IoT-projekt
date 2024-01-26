from config import *
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

CARD_ACTIVE = 200 
CARD_NEW = 201
CARD_INACTIVE = 403 


def buzz():
    GPIO.output(buzzerPin, False)
    time.sleep(1)
    GPIO.output(buzzerPin, True)


def displayLight(color):
    GPIO.setmode(GPIO.BCM)
    pixels = neopixel.NeoPixel(board.D18, 8, brightness=1.0/32, auto_write=False)

    for i in range(8):
        pixels[i] = color
    pixels.show()


def displayLightOn(response):

    if response==CARD_ACTIVE:
        color = (0, 255, 0)
    elif response==CARD_NEW:
        color = (0, 0, 255)
    elif response== CARD_INACTIVE:
        color = (255, 255, 0)
    else:
        color = (255, 0, 0)

    displayLight(color)


def displayLightOff():
    color = (0, 0, 0)
    displayLight(color)


def display(disp, alert):
    images = Image.new("RGB", (disp.width, disp.height), "BLACK")

    drawAlert(images, alert)

    disp.ShowImage(images, 0, 0)


def drawAlert(images, alert):
    draw = ImageDraw.Draw(images)
    fontParam = ImageFont.truetype('./lib/oled/Font.ttf', 10)

    alert_words = alert.split()
    single_line = ""
    text_position = 0

    for word in alert_words:
        if len(single_line+" "+word)>18:
            draw.text((0, text_position), single_line, font=fontParam, fill="WHITE")
            text_position+=15
            single_line=""
        single_line = single_line + word + " "

    if(len(single_line)>0):
        draw.text((0, text_position), single_line, font=fontParam, fill="WHITE")


def turnOffDevice(disp):
    displayLightOff()
    displayInfoOFF(disp)


def turnOnDevice(disp):
    displayInfoON(disp)


def displayInfoON(disp):
    display(disp, "Card registration")


def displayInfoOFF(disp):
    display(disp, "Device turned off- press green button to start")


def displayScan(disp, response):
    if response==CARD_ACTIVE:
        alert = "Card already registered - active"
    elif response==CARD_NEW:
        alert = "New card registered"
    elif response== CARD_INACTIVE:
        alert = "Card already registered - inactive"
    else:
        alert = "Error"

    display(disp, alert)


def succesDisplay(disp, response):
    displayLightOn(response)
    displayScan(disp, response)
    time.sleep(2)
    displayLightOff()
    displayInfoON(disp)


