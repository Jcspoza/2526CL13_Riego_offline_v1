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
# 5.0 -> lectura con timer

from machine import ADC, Pin, Timer
from time import sleep, ticks_ms, ticks_diff

# Informative block - start
p_ucontroler = "Pico W & Pico _"
p_keyOhw = "Soil moisture (sparkfun) on GPIO26 ADC0 - pata + a GPIO21"
p_project = "Basic HW test soil moisture calibrado  Lectura por temporizador"
p_version = "5.0"
print(f"Microcontroler: {p_ucontroler} - Key other HW : {p_keyOhw}")
print(f"Program: {p_project} - Version: {p_version}")
# Informative block - end

# 1- Crea el objeto sensor soil que lee por ADC
# el valor de la humedad del suelo
# Sensor humedad suelo
SOILMOISTADC = 0 # es el ADC0
# GPIO para alimentar sensores Tank y humedad suelo
POWERSENS = 21

sensorSoil = ADC(SOILMOISTADC)
alimentaSensor = Pin(POWERSENS, Pin.OUT)
SOILRAWMAX = 33000 # resultado de calibracion real, valor con agua con sal
SOILRAWMIN = 700 # resultado de calibracion real, valor sonda al aire

flagReadSoilH = False
SartTimeonHigh = ticks_ms()

def readSoilhum100():
    Soilraw = sensorSoil.read_u16()
    if Soilraw >= SOILRAWMAX :
        Soilraw = SOILRAWMAX
        
    if Soilraw <= SOILRAWMIN :
        Soilraw = SOILRAWMIN
    # map function
    return int((Soilraw - SOILRAWMIN) / (SOILRAWMAX - SOILRAWMIN) * 100) , Soilraw

def TimetoSoilH(Timer):
    global flagReadSoilH, SartTimeonHigh, alimentaSensor
    flagReadSoilH = True
    SartTimeonHigh = ticks_ms()
    alimentaSensor.on()

TIEMPOHIGH = 200 # milisec
ESPERA = 4000

SoilHtim = Timer(period=ESPERA, mode=Timer.PERIODIC, callback=TimetoSoilH)
# 2- Bucle de lectura

cuenta = 0
try:
    while True: # Bucle principal
        now = ticks_ms()
        if flagReadSoilH and ticks_diff(now, SartTimeonHigh ) > TIEMPOHIGH:
            flagReadSoilH = False
            print(now, SartTimeonHigh)
            SartTimeonHigh = now
            soilMper, soilMraw = readSoilhum100()
            alimentaSensor.off()
            print(f"Humedad Suelo = {soilMper:3d} % | Valor ADC bruto = {soilMraw} | {alimentaSensor.value()}")            
        
        print('Hago cosas #',cuenta)
        cuenta += 1
        sleep(1) # sleep 1sec
                
except KeyboardInterrupt:
    alimentaSensor.off()
    print("\nParada de usuario")
    
