# Hardware platform: Pico W
# Author : JC Santamaria 
# Date : 2023 - 6 -15
# Goal : Read DHT22 sensor T and H - basic Hw Test
# Ref : 

from dht import DHT22
from machine import Pin
from time import sleep

sensorDHT = DHT22(Pin(14))

while (True):
    try:
        sleep (1) # maximun sampling rate in cas eof DHT22
        sensorDHT.measure() # order a measure
        temp=sensorDHT.temperature () # simple copy of last measure Temp
        hum=sensorDHT.humidity() # simple copy of last measure Humidity
        print ("T={:02.2f} ºC, H={:02.2f} %".format (temp,hum))
    except OSError as e:
        print("Failed reception error="+str(e))

        
