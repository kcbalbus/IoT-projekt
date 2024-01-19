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


def show():

    disp = SSD1331.SSD1331()
    # Initialize library.
    disp.Init()
    image1 = Image.new("RGB", (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image1)
    draw.text((0, 0), f"Temp: {round(temp, 1)}", fill="BLACK")
    draw.text((0, 25), f"Humidity: {round(humidity, 1)}", fill="BLACK")
    draw.text((0, 50), f"Pressure: {round(pressure, 1)}", fill="BLACK")

    disp.ShowImage(image1, 0, 0)


def update():
    disp = SSD1331.SSD1331()

    image1 = Image.new("RGB", (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image1)
    draw.text((0, 0), f"Temp: {round(temp, 1)}", fill="BLACK")
    draw.text((0, 25), f"Humidity: {round(humidity, 1)}", fill="BLACK")
    draw.text((0, 50), f"Pressure: {round(pressure, 1)}", fill="BLACK")

    disp.ShowImage(image1, 0, 0)


def readSensors():
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
    show()

    while True:
        get()
        update()
        time.sleep(5)
