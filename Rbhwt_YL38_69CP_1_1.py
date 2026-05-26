# Hardware platform: Pico _, 2, W & 2w
# Author : JC Santamaria 
# Date : 2026 - 5 - 18
# Goal : Read YL-38 7 Yl-69 soil humidity sensor Digital output - basic Hw Test
# Ref : https://www.esploradores.com/dht/
# 1.0 

from os import uname
# Informative block - start
p_keyOhw = "Sensor soil moisture L-38 & YL-69 , DO in GPIO22- continuous power"
p_project = "Test HW basico DHT22"
p_version = "1.1"
p_library = "None"
print(f"uPython version: {uname()[3]} ")
print(f"uC: {uname()[4]} - Key other HW: {p_keyOhw}")
print(f"Program: {p_project} - Version: {p_version}")
print(f"Key Library: {p_library}")

from machine import Pin
from time import sleep

sensorTank = Pin(22, Pin.IN)


while True:
    sleep(2)
    if sensorTank.value() :
        print("Tanque VACIO")
    else:
        print("Tanque LLENO")
        
        
    

        
