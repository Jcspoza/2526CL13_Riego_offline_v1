# Taller Programación y Robótica en CMM BML – 2025-2026 = RIEGO AUTOMATICO Off Line =
# Programa: Montaje #6 Todo el HW -> Fase de inicializacion
# Hardware platform: Pico _ & W / funciona igual sin cambios
# 1. Display SH1106
# Librerias : sh1106.py
# Ref librerias: https://github.com/robert-hh/SH1106
# Fecha JCSP 2026 03
# Licencia : CC BY-NC-SA 4.0
# REf basica https://docs.sunfounder.com/projects/pico-2w-kit/en/latest/pyproject/py_water.html
# Montaje #6 : todo el HW

from machine import Pin, ADC, I2C, Timer
from dht import DHT22
from time import sleep, ticks_ms, ticks_diff
import sh1106
from writer import Writer
# Font
# import inkfree20 as font
import freesans20 as font

from os import uname
# Informative block - start
p_ucontroler = "Pico W & Pico _"
p_keyOhw = "External pot. on ADC0 - pata + a GPIO21 + displ SH1106 gpio4&5"
p_project = "Riego Autgomatico - Off Line "
p_version = "6.0"
p_library = "SH1106  @robert-hh + writer @peterhinch + dht"
print(f"uPython version: {uname()[3]} ")
print(f"uC: {uname()[4]} - Key other HW: {p_keyOhw}")
print(f"Program: {p_project} - Version: {p_version}")
print(f"Key Library: {p_library}")
# Informative block - end

# 0.0 - Constates y varaibles globales para display
WIDTH =128 
HEIGHT= 64
ADRDISPLAY = 60
TopLy = 0
TopLhy = 9
FstLy = 11
SndLy = 21
TrdLy = 31
StatLhy = 54
StatLy = 56
WIDTH_VA = 21
WIDTH_ST = 8
FREQ = 400_000   # Try lowering this value in case of "Errno 5"

# 0.1 Controla la entrada al bucle principal
AllHWready = False

# 0.2 Almacena los datos de check de HW ( solo el hw que se puede chequear
HWreadydict = {'display': False,
               'dht22' : False,
               'Tank' : False
               }
# ------ INICIO DE CHECKS --------
# 1.1 Check del display
# pone a parpadear el led interno con periodo de 1 segundo
iled = Pin("LED", Pin.OUT)
iledtim = Timer(period=1000, mode=Timer.PERIODIC, callback=lambda t:iled.toggle())

# 1.1.1 Crea bus I2c
i2c = I2C(0, sda = Pin(4), scl = Pin(5), freq = FREQ)
devices = i2c.scan() # this returns a list of devices
device_count = len(devices)
if len(devices) == 0 or ADRDISPLAY not in devices:
    print('ERROR : No i2c device found or Display sh1106 not present')
    iledtim.init(period=250,mode=Timer.PERIODIC, callback=lambda t:iled.toggle())
    while True:
        pass
    
print('OK : i2c device found & Display sh1106 present')
HWreadydict['display'] = True
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

# 1.1.4 mensaje Display Ok en Display
ToplineStr = f"Riego A_off-v{p_version}"
display.text(ToplineStr, 0, TopLy, 1)
display.hline(0, TopLhy,128,1)
display.text('Displ OK .......', 0, FstLy, 1)
textobig = "HW Test Run"
Writer.set_textpos(display, TrdLy, 0)  
wri.printstring(textobig)
display.hline(0, StatLhy,128,1)
display.text('Display Ok', 0, StatLy, 1)
display.show()

# 1.2 Check del Sensor DHT22
sensorDHT = DHT22(Pin(14))

try:
    sleep(2) # maximun sampling rate in cas eof DHT22
    sensorDHT.measure() # order a measure
    temp=sensorDHT.temperature () # simple copy of last measure Temp
    hum=sensorDHT.humidity() # simple copy of last measure Humidity
    print (f"T={temp:02.2f} ºC, H={hum:02.2f} %")
    display.fill_rect(0, FstLy, WIDTH, 8, 0)
    display.text('Disp OK/DHT22 OK', 0, FstLy, 1)
    display.text(f'T={temp:02.1f}C H={hum:02.1f}%', 0, SndLy, 1)
    display.fill_rect(0, StatLy, WIDTH, 8, 0)
    display.text('DHT22 ok', 0, StatLy, 1)
    display.show()
    HWreadydict['dht22'] = True
except OSError as e:
    display.fill_rect(0, StatLy, WIDTH, 8, 0)
    display.text('ERROR DHT22', 0, StatLy, 1)
    display.show()
    print("ERROR DHT22 ="+str(e))
    iledtim.init(period=250,mode=Timer.PERIODIC, callback=lambda t:iled.toggle())

# 1.3 Check del Tanque
sensorTank = Pin(22, Pin.IN)
alimentaSensor = Pin(21, Pin.OUT)
alimentaSensor.on()

sleep(2)
if sensorTank.value() :
    print("ERROR Tanque VACIO")
    HWreadydict['Tank'] = False
    display.fill_rect(0, SndLy, WIDTH, 8, 0)
    display.text('Tank EMPTY', 0, SndLy, 1)
    display.fill_rect(0, StatLy, WIDTH, 8, 0)
    display.text('ERROR TANK', 0, StatLy, 1)
    display.show()
    iledtim.init(period=250,mode=Timer.PERIODIC, callback=lambda t:iled.toggle())
    alimentaSensor.off()
else:
    print("OK Tanque LLENO")
    HWreadydict['Tank'] = True
    display.fill_rect(0, SndLy, WIDTH, 8, 0)
    display.text('Tank OK', 0, SndLy, 1)
    display.fill_rect(0, StatLy, WIDTH, 8, 0)
    alimentaSensor.off()
    
# 1.5 final
AllHWready = HWreadydict['display'] and HWreadydict['dht22'] and HWreadydict['Tank']

if AllHWready:
    textobig = "HW Test OK"
else:
    textobig = "HW Test FAIL"

display.fill_rect(0, TrdLy, WIDTH, WIDTH_VA, 0) # borra
Writer.set_textpos(display, TrdLy, 0)  
wri.printstring(textobig)
display.fill_rect(0, StatLy, WIDTH, 8, 0)
display.text('HW Test End', 0, StatLy, 1)
display.show()

iledtim.deinit()
sleep(1)
iled.off()
# ------ FIN DE CHECKS --------


 


