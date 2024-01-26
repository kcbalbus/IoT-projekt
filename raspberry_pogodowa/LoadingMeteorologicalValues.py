#!/usr/bin/env python3

import w1thermsensor
import time
import board
import os
from PIL import Image, ImageDraw, ImageFont
import lib.oled.SSD1331 as SSD1331
import neopixel
import busio
import adafruit_bme280.advanced as adafruit_bme280
from config import *


global temp
global humidity
global pressure
global altitude


def show(disp):

    
    # Initialize library.
    disp.Init()
    image1 = Image.new("RGB", (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image1)

    fontParam = ImageFont.truetype('./lib/oled/Font.ttf', 8)

    image_temperature = Image.open('./temperature.png')
    image_temperature = image_temperature.resize((15, 10))
    image_humidity = Image.open('./humidity.png')
    image_humidity = image_humidity.resize((15, 10))
    image_pressure = Image.open('./pressure.png')
    image_pressure = image_pressure.resize((15, 10))

    image1.paste(image_temperature, (0, 0))
    draw.text((17, 0), f"Temperature: {round(temp, 1)}", font=fontParam, fill="BLACK")
    image1.paste(image_humidity, (0, 25))
    draw.text((17, 25), f"Humidity: {round(humidity, 1)}", font=fontParam, fill="BLACK")
    image1.paste(image_pressure, (0, 50))
    draw.text((17, 50), f"Pressure: {round(pressure, 1)}", font=fontParam, fill="BLACK")

    disp.ShowImage(image1, 0, 0)


def update(disp):
    
    image1 = Image.new("RGB", (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image1)
    fontParam = ImageFont.truetype('./lib/oled/Font.ttf', 8)
    
    image_temperature = Image.open('./temperature.png')
    image_temperature = image_temperature.resize((15, 10))
    image_humidity = Image.open('./humidity.png')
    image_humidity = image_humidity.resize((15, 10))
    image_pressure = Image.open('./pressure.png')
    image_pressure = image_pressure.resize((15, 10))

    image1.paste(image_temperature, (0, 0))
    draw.text((17, 0), f"Temperature: {round(temp, 1)}", font=fontParam, fill="BLACK")
    image1.paste(image_humidity, (0, 25))
    draw.text((17, 25), f"Humidity: {round(humidity, 1)}", font=fontParam, fill="BLACK")
    image1.paste(image_pressure, (0, 50))
    draw.text((17, 50), f"Pressure: {round(pressure, 1)}", font=fontParam, fill="BLACK")

    disp.ShowImage(image1, 0, 0)


def initDisp():
    displ = SSD1331.SSD1331()
    displ.Init()
    return displ

def dispValues(Temp, Humidity, Pressure, displ):

    image1 = Image.new("RGB", (displ.width, displ.height), "WHITE")
    draw = ImageDraw.Draw(image1)
    fontParam = ImageFont.truetype('./lib/oled/Font.ttf', 8)
    
    image_temperature = Image.open('./temperature.png')
    image_temperature = image_temperature.resize((15, 10))
    image_humidity = Image.open('./humidity.png')
    image_humidity = image_humidity.resize((15, 10))
    image_pressure = Image.open('./pressure.png')
    image_pressure = image_pressure.resize((15, 10))

    image1.paste(image_temperature, (0, 0))
    draw.text((17, 0), f"Temperature: {round(Temp, 1)}", font=fontParam, fill="BLACK")
    image1.paste(image_humidity, (0, 25))
    draw.text((17, 25), f"Humidity: {round(Humidity, 1)}", font=fontParam, fill="BLACK")
    image1.paste(image_pressure, (0, 50))
    draw.text((17, 50), f"Pressure: {round(Pressure, 1)}", font=fontParam, fill="BLACK")

    displ.ShowImage(image1, 0, 0)

    

def readSensors():
    i2c = busio.I2C(board.SCL, board.SDA)
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)

    bme280.overscan_pressure = adafruit_bme280.OVERSCAN_X16
    bme280.overscan_humidity = adafruit_bme280.OVERSCAN_X1
    bme280.overscan_temperature = adafruit_bme280.OVERSCAN_X2

    temp = bme280.temperature
    humidity = bme280.humidity
    pressure = bme280.pressure

    return (temp, humidity, pressure)


def get():
    global temp
    global humidity
    global pressure
    global altitude

    bme280.overscan_pressure = adafruit_bme280.OVERSCAN_X16
    bme280.overscan_humidity = adafruit_bme280.OVERSCAN_X1
    bme280.overscan_temperature = adafruit_bme280.OVERSCAN_X2

    temp = bme280.temperature
    humidity = bme280.humidity
    pressure = bme280.pressure
    altitude = bme280.altitude


    print('\nBME280:')
    print(f'Temperature: {bme280.temperature:0.1f} '+chr(176)+'C')
    print(f'Humidity: {bme280.humidity:0.1f} %')
    print(f'Pressure: {bme280.pressure:0.1f} hPa')
    print(f'Altitude: {bme280.altitude:0.2f} meters')


if __name__ == "__main__":
    i2c = busio.I2C(board.SCL, board.SDA)
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)

    bme280.sea_level_pressure = 1013.25
    bme280.standby_period = adafruit_bme280.STANDBY_TC_500
    bme280.iir_filter = adafruit_bme280.IIR_FILTER_X16

    get()
    disp = SSD1331.SSD1331()

    show(disp)

    while True:
        get()
        update(disp)
        time.sleep(5)
