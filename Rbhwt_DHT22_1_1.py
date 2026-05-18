# Hardware platform: Pico _, 2, W & 2w
# Author : JC Santamaria 
# Date : 2023 - 6 -15
# Goal : Read DHT22 sensor T and H - basic Hw Test
# Ref : https://www.esploradores.com/dht/

from os import uname
# Informative block - start
p_keyOhw = "DHT22 data GPIO14 + pull-up 4.7k"
p_project = "Test HW basico DHT22"
p_version = "1.1"
p_library = "dht  included in uPy rp2"
print(f"uPython version: {uname()[3]} ")
print(f"uC: {uname()[4]} - Key other HW: {p_keyOhw}")
print(f"Program: {p_project} - Version: {p_version}")
print(f"Key Library: {p_library}")

from dht import DHT22
from machine import Pin
from time import sleep

sensorDHT = DHT22(Pin(14))

while (True):
    try:
        sleep (2) # maximun sampling rate in case of DHT22
        sensorDHT.measure() # order a measure
        temp=sensorDHT.temperature () # simple copy of last measure Temp
        hum=sensorDHT.humidity() # simple copy of last measure Humidity
        print (f"T={temp:02.2f} ºC, H={hum:02.2f} %")
    except OSError as e:
        print("Failed reception error="+str(e))

        
