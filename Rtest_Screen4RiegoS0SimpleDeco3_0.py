# Taller Programación y Robótica en CMM BML – 2025-2026 = RIEGO AUTOMATICO Off Line =
# Hardware platform: Pico _, 2, W & 2w
# Author : JC Santamaria 
# Date : 2026 - 6 -4
# Goal : SH1106 display screen test -
# Display SH1106
# Librerias : sh1106.py
# Ref librerias: https://github.com/robert-hh/SH1106
# 1.0 -> 2.0 mejora de pantallas y cuenta timpos de ejecucion
# 2.0 -> 3.0 cuenta tiempos con funcion decorador

from machine import Pin, ADC, I2C, Timer,PWM
from dht import DHT22
from time import sleep, ticks_ms, ticks_diff
import sh1106
from writer import Writer
# Font
import freesans20 as font
from rotary_irq_rp2 import RotaryIRQ

# Informative block - start
from os import uname
p_ucontroler = "Pico W & Pico _"
p_keyOhw = "displ SH1106 gpio4&5"
p_project = "Test de pantallas de riego-Visual simple-Tiempo con Decorador"
p_version = "3.0"
p_library = "SH1106  @robert-hh + writer @peterhinch"
print(f"uPython version: {uname()[3]} ")
print(f"uC: {uname()[4]} - Key other HW: {p_keyOhw}")
print(f"Program: {p_project} - Version: {p_version}")
print(f"Key Library: {p_library}")
# Informative block - end

# 0.0 - Constates y varaibles globales para display
WIDTH =128 
HEIGHT= 64
ADRDISPLAY = 60
# Display is organised in 6 lines for writing: top, 1st, 2nd, 3rd (also for bigsize letter)
# 4rd and Status line
TopLy = 0   # Top line y coor
TopLhy = 9
FstLy = 11
SndLy = 21
TrdLy = 31 
FrdLy = 41
StatLhy = 54
StatLy = 56
WIDTH_VA = 21
WIDTH_ST = 8
FREQ = 400_000   # Try lowering this value in case of "Errno 5"

# ------ INICIALIZACIONES --------
# pone a parpadear el led interno con periodo de 1 segundo
iled = Pin("LED", Pin.OUT)
iledtim = Timer(period=1000, mode=Timer.PERIODIC, callback=lambda t:iled.toggle())

# 1.1 INICIALIZACION del display
# 1.1.1 Crea bus I2c
i2c = I2C(0, sda = Pin(4), scl = Pin(5), freq = FREQ)

# 1.1.2 Creacion del objeto display
display = sh1106.SH1106_I2C(WIDTH,
                            HEIGHT,
                            i2c,
                            res = None,
                            addr = ADRDISPLAY,
                            rotate = 0) # valores 0, 90, 180, 270
display.sleep(False)

display.fill(0)

# 1.1.3- Crea el objeto wri para letra de mas tamaño
wri = Writer(display, font, verbose = False) # verbose = False to suppress console output

# Decorador para medir tiempos
import time

def timeit(func):
    def wrapper(*args, **kwargs):
        start = ticks_ms()
        result = func(*args, **kwargs)
        delta = ticks_diff(time.ticks_ms(), start)
        print(f"Function '{func.__name__}' took {delta} ms")
        return result
    return wrapper


# 1.1.4 Funciones de Dibujo del display + Decorador
@timeit
def ShowDispL3B(lt, l1, l2, l3b, ls, Erase = True, Show = True):
    """ funcion generica de display 3 lineas centrales 3ra fuente x20"""
    if Erase:
        display.fill(0)
        
        
    display.fill_rect(0, TopLy, WIDTH, 8, 0)    
    display.text(lt, 0, TopLy, 1)    
    display.hline(0, TopLhy,128,1)
    
    display.fill_rect(0, FstLy, WIDTH, 8, 0)    
    display.text(l1, 0, FstLy, 1)
    
    display.fill_rect(0, SndLy, WIDTH, 8, 0)
    display.text(l2, 0, SndLy, 1)
    
    display.fill_rect(0, TrdLy, WIDTH, WIDTH_VA, 0) # borra 3ra linea x21 alto
    Writer.set_textpos(display, TrdLy, 0)  
    wri.printstring(l3b)
    
    display.hline(0, StatLhy,128,1)
    display.fill_rect(0, StatLy, WIDTH, 8, 0)
    display.text(ls, 0, StatLy, 1)
    
    if Show:
        display.show()

# END display functions ----------------
Topline = f"S0.Init HW -v{p_version}"
ShowDispL3B(Topline, 'OK: Disp...', '', 'HW Init Run', 'Init progress')
sleep(1)

ShowDispL3B(Topline, 'OK: Dis/3sw', '', 'HW Init Run', 'Init %..')
sleep(1)

ShowDispL3B(Topline, 'OK: Dis/3sw/Pump', '', 'HW Init Run', 'Init %....')
sleep(1)

ShowDispL3B(Topline, 'OK: Dis/3sw/Pump', 'RE/', 'HW Init Run', 'Init %......')
sleep(1)

ShowDispL3B(Topline, 'OK: Dis/3sw/Pump', 'RE/SHum', 'HW Init Run', 'Init %........')
sleep(1)

# ShowDispL3B(Topline,'OK:Dis/3sw/Pump', 'RE/SHum/Tank NOK', 'FILL TANK' , 'HW INIT Fail')
ShowDispL3B(Topline,'OK:Dis/3sw/Pump', 'RE/SHum/Tank OK', 'press CON->' , 'HW INIT END')


iledtim.deinit()
sleep(1)
iled.off()