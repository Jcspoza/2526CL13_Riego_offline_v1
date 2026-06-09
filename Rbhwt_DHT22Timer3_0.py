# Hardware platform: Pico _, 2, W & 2w
# Author : JC Santamaria 
# Date : 2026 - 6 -4
# Goal : Read DHT22 sensor T and H by timer
# Ref : https://www.esploradores.com/dht/

from os import uname
# Informative block - start
p_keyOhw = "DHT22 data GPIO14 + pull-up 4.7k"
p_project = "Test HW basico DHT22 - Timer"
p_version = "3.0"
p_library = "dht  included in uPy rp2"
print(f"uPython version: {uname()[3]} ")
print(f"uC: {uname()[4]} - Key other HW: {p_keyOhw}")
print(f"Program: {p_project} - Version: {p_version}")
print(f"Key Library: {p_library}")

from dht import DHT22
from machine import Pin, Timer
from time import sleep

sensorDHT = DHT22(Pin(14))
DEBUG = True
lStatus = {"ATem" : None,
           "AHum" : None}

def readDHT(timer):
    
    global lStatus
    sensorDHT.measure()
    lStatus["ATem"] = sensorDHT.temperature() # simple copy of last measure Temp
    lStatus["AHum"] = sensorDHT.humidity() # simple copy of last measure Humidity
    if DEBUG:
        print (f"T={lStatus['ATem']:02.2f} ºC, H={lStatus['AHum']:02.2f} %")
    
DHTtim = Timer(period=2000, mode=Timer.PERIODIC, callback=readDHT)

cuenta = 0
while True:
    try:
        print('Hago cosas #',cuenta)
        cuenta += 1
        sleep(1) # sleep 1sec
        
    except OSError as e:
        print("Failed reception error="+str(e))
        
    except KeyboardInterrupt:
        print("Exit by keyboard")
        break

# Deshago el timer
DHTtim.deinit()

print("Finished.")     
