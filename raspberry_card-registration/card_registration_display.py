from config import *
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

    match response:
        case 200:
            color = (0, 255, 0)
        case 201:
            color = (0, 0, 255)
        case 401:
            color = (255, 255, 0)
        case _:
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
            draw.text((text_position,0), single_line, font=fontParam, fill="WHITE")
            text_position+=15
            single_line=""
        single_line = single_line + word + " "

    if(len(single_line)>0):
        draw.text((text_position, 0), single_line, font=fontParam, fill="WHITE")


def displayInfo(disp):
    display(disp, "Register new card")


def displayScan(disp, response):
    match response:
        case 200:
            alert = "Card active"
        case 201:
            alert = "New card"
        case  401:
            alert = "Card inactive"
        case _:
            alert = "Error"

    display(disp, alert)

def succesDisplay(disp, response):
    displayLightOn(response)
    displayScan(disp, response)
    time.sleep(3)
    displayLightOff()
    displayInfo(disp)


