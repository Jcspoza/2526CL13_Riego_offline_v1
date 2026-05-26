# Taller Programación y Robótica en CMM BML – 2024-2025
# Programa: hw test de motor controlado por Transistor NPN y por PWM
# Hardware platform: Pico _ & W / funciona igual sin cambios
# Librerias : Ninguna
# Ref librerias: 
# Fecha JCSP 2026 03
# Licencia : CC BY-NC-SA 4.0
# REf basica https://dmccreary.github.io/learning-micropython/basics/04-fade-in-and-out/


from machine import Pin, PWM
from utime import sleep

# Informative block - start
p_ucontroler = "Pico _ & W"
p_keyOhw = "Motor + NPN emisor comun en GPIO15 PWM"
p_project = "HWBT Motor - PWM dutty input 0 a 100- 1000Hz"
p_version = "1.0"
print(f"Microcontroler: {p_ucontroler} - Key other HW : {p_keyOhw}")
print(f"Program: {p_project} - Version: {p_version}")
# Informative block - end

# Motor bomba pin
MOTORPIN = 15

# 1.5 Crea el motor bomba
motorPwm = PWM(Pin(MOTORPIN))
motorPwm.freq(1000)
motorPwm.duty_u16(0) # stop motor

motorpor100 = 50 # fijamos inicialmente a 50% del regimen del motor cuando arranque
# pasamos a dutty cycle  de 0 a 65_000
motorpor60mil = int(65535 * motorpor100 / 100)

try: # try fuera del bucle porque quiero que se dentenga y no reanude
    while (True):
        motorPwm.duty_u16(motorpor60mil)
        motorpor100 = int(input("Porcentaje (0 a 100)= "))
        while motorpor100 < 0 or motorpor100 > 100:
            print('Error en la introduccion de porcentaje')
            motorpor100 = int(input("Porcentaje (0 a 100)= "))
            
        motorpor60mil = int(65535 * motorpor100 / 100)
        
except KeyboardInterrupt:
    motorPwm.duty_u16(0)
    motorPwm.deinit()
        
