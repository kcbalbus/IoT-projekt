from config import *
import w1thermsensor
import time
import os
import neopixel
import board
import busio
import adafruit_bme280.advanced as adafruit_bme280
from PIL import Image, ImageDraw, ImageFont
import lib.oled.SSD1331 as SSD1331
from datetime import datetime
import time
from tkinter.tix import DirTree
import RPi.GPIO as GPIO
from mfrc522 import MFRC522
from datetime import datetime
#import paho.mqtt.client as mqtt
import tkinter

terminal_id = "T0"
broker = "localhost"
#client = mqtt.Client()

def bme280_config():
    i2c = busio.I2C(board.SCL, board.SDA)
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)
    bme280.sea_level_pressure = 1013.25
    bme280.standby_period = adafruit_bme280.STANDBY_TC_500
    bme280.iir_filter = adafruit_bme280.IIR_FILTER_X16
    return bme280

def bme280_read(bme):
    bme.overscan_pressure = adafruit_bme280.OVERSCAN_X16
    bme.overscan_humidity = adafruit_bme280.OVERSCAN_X1
    bme.overscan_temperature = adafruit_bme280.OVERSCAN_X2
    print(bme.temperature)
    print(bme.humidity)
    print(bme.pressure)
    return {"temperature" : round(bme.temperature, 2), "humidity" : round(bme.humidity, 2), "pressure" : round(bme.pressure, 2)}

def display_measures(parameters, disp):
    images = Image.new("RGB", (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(images)
    fontParam = ImageFont.truetype('./lib/oled/Font.ttf', 8)

    image_temperature = Image.open('./temperature.png')
    image_temperature = image_temperature.resize((15, 10))
    image_humidity = Image.open('./humidity.png')
    image_humidity = image_humidity.resize((15, 10))
    image_pressure = Image.open('./pressure.png')
    image_pressure = image_pressure.resize((15, 10))

    images.paste(image_temperature, (0, 0))
    draw.text((17,0), f'Temperature: {parameters["temperature"]}', font=fontParam, fill="BLACK")

    images.paste(image_humidity, (0, 25))
    draw.text((17,25), f'Humidity: {parameters["humidity"]}', font=fontParam, fill="BLACK")

    images.paste(image_pressure, (0, 50))
    draw.text((17,50), f'Pressure: {parameters["pressure"]}', font=fontParam, fill="BLACK")

    disp.ShowImage(images, 0, 0)

def display_info(disp):
    images = Image.new("RGB", (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(images)
    fontParam = ImageFont.truetype('./lib/oled/Font.ttf', 10)

    draw.text((0,0), 'Please scan your', font=fontParam, fill="BLACK")
    draw.text((0,15), 'card to start', font=fontParam, fill="BLACK")


    disp.ShowImage(images, 0, 0)

def display_green_light():
    GPIO.setmode(GPIO.BCM)
    pixels = neopixel.NeoPixel(board.D18, 8, brightness=1.0/32, auto_write=False)

    for i in range(8):
        pixels[i] = (0, 255, 0)
    pixels.show()
    time.sleep(1)
    pixels.fill((0, 0, 0))
    pixels.show()


def buzzer_state(state):
    GPIO.output(buzzerPin, not state)

def buzzer():
    buzzer_state(True)
    time.sleep(1)
    buzzer_state(False)


def rfidRead(MIFAREReader):
    dt = datetime.now()
    
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    if status == MIFAREReader.MI_OK:
        (status, uid) = MIFAREReader.MFRC522_Anticoll()
        if status == MIFAREReader.MI_OK:
            num = 0
            for i in range(0, len(uid)):
                num += uid[i] << (i*8)
            
            print(f"UID: {num} Date: {dt}") 
            buzzer()
            
            return str(num)
    
    return ""


#def call_measure(station_id, measures, dt):
 #   client.publish("test/bme280", str(station_id) + " - " + str(measures['temperature']) + " - "  + str(measures['hummidity']) + " - " + str(measures['pressure']) + " - " + str(dt))

#def connect_to_broker():
 #   client.connect(broker)
  #  call_measure("Client connected", datetime.now())

#def disconnect_from_broker():
 #   call_measure("Client disconnected", datetime.now())
  #  client.disconnect()



if __name__ == "__main__":
    MIFAREReader = MFRC522()
    bme1 = bme280_config()
    disp = SSD1331.SSD1331()
    disp.Init()
    user = ""

    display_info(disp)

    while(user == ""):
        user = rfidRead(MIFAREReader)
        

    parameters= bme280_read(bme1)
    last_scan = datetime.timestamp(datetime.now())

    while(True):
        dt = datetime.now()

        if(datetime.timestamp(dt)-last_scan>5.0):
            last_scan=datetime.timestamp(dt)
            display_green_light()
            parameters = bme280_read(bme1)

        display_measures(parameters, disp)
    
    disp.clear()    