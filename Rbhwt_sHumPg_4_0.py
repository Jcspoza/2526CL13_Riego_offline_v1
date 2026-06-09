# Taller Programación y Robótica en CMM BML – 2025 - 2026 - CL11 Sensor Humedad suelo
# Programa: Pruebas de lectura de sensor humadad tipo spakfun - con potenciometro
# Hardware platform: Pico _ & W / funciona igual sin cambios
# Librerias : Ninguna
# Ref librerias: 
# Fecha JCSP 2026 03
# Licencia : CC BY-NC-SA 4.0
# REf basica https://docs.sunfounder.com/projects/pico-2w-kit/en/latest/pyproject/py_water.html
# 1.0 -> 2.0 pin extremo potenciometro a GPIO21 + tiempo high
# 2.0 -> 2.1 mas velocidad lectura, print en misma linea
# 2.1 -> 4.0 Renombra a bhwt: sensor humedad en ADC0 CALIBRADO , alimentado por GPIO + salta linea

from machine import ADC, Pin
from time import sleep

# Informative block - start
p_ucontroler = "Pico W & Pico _"
p_keyOhw = "Soil moisture (sparkfun) on GPIO26 ADC0 - pata + a GPIO21"
p_project = "Basic HW test soil moisture calibrado"
p_version = "4.0"
print(f"Microcontroler: {p_ucontroler} - Key other HW : {p_keyOhw}")
print(f"Program: {p_project} - Version: {p_version}")
# Informative block - end


# 1- Crea el objeto ADC que conecta el pin central
# del potenciometro a adc0 = gpio 26
# Los otros 2 pines a +3.3 y 0 volt respectivamente
# Sensor humedad suelo
SOILMOISTADC = 0 # es el ADC0
# GPIO para alimentar sensores Tank y humedad suelo
POWERSENS = 21

sensorSoil = ADC(SOILMOISTADC)
alimentaSensor = Pin(POWERSENS, Pin.OUT)
SOILRAWMAX = 33000 # resultado de calibracion real, valor con agua con sal
SOILRAWMIN = 700 # resultado de calibracion real, valor sonda al aire

def readSoilhum100():
    Soilraw = sensorSoil.read_u16()
    if Soilraw >= SOILRAWMAX :
        Soilraw = SOILRAWMAX
        
    if Soilraw <= SOILRAWMIN :
        Soilraw = SOILRAWMIN
    # map function
    return int((Soilraw - SOILRAWMIN) / (SOILRAWMAX - SOILRAWMIN) * 100) , Soilraw

TIEMPOHIGH = 0.2
ESPERA = 4

# 2- Bucle de lectura
try:
    while True:
        alimentaSensor.on()
        sleep(TIEMPOHIGH)
        soilMper, soilMraw = readSoilhum100()
        print(f"Humedad Suelo = {soilMper:3d} % | Valor ADC bruto = {soilMraw}")
        alimentaSensor.off()
        sleep(ESPERA)
                
except KeyboardInterrupt:
    alimentaSensor.off()
    print("\nParada de usuario")
    
