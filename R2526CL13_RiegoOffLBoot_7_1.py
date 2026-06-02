# Taller Programación y Robótica en CMM BML – 2025-2026 = RIEGO AUTOMATICO Off Line =
# Programa: Montaje #7 Todo el HW -> Fase de inicializacion COMPLETA
# Hardware platform: Pico _ & W / funciona igual sin cambios
# 1. Display SH1106
# Librerias : sh1106.py
# Ref librerias: https://github.com/robert-hh/SH1106
# Fecha JCSP 2026 03
# Licencia : CC BY-NC-SA 4.0
# REf basica https://docs.sunfounder.com/projects/pico-2w-kit/en/latest/pyproject/py_water.html
# Montaje #7 : todo el HW INICIALIZADO incluido motor PWM

from machine import Pin, ADC, I2C, Timer,PWM
from dht import DHT22
from time import sleep, ticks_ms, ticks_diff
import sh1106
from writer import Writer
# Font
import freesans20 as font
from rotary_irq_rp2 import RotaryIRQ

from os import uname
# Informative block - start
p_ucontroler = "Pico W & Pico _"
p_keyOhw = "External pot. on ADC0 - pata + a GPIO21 + displ SH1106 gpio4&5"
p_project = "Riego Autgomatico Inicializacion COMPLETA - Off Line "
p_version = "7.1"
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
# Display is organised in 6 lines for writing: top, 1st, 2nd, 3rd (also for bigsize letter)
# 4rd and Status line
TopLy = 0   # Top line y coor
TopLhy = 9
FstLy = 11
SndLy = 21
TrdLy = 31 
FrdLy = 41 # not used if 2rd use a big letter x20
StatLhy = 54
StatLy = 56
WIDTH_VA = 21
WIDTH_ST = 8
FREQ = 400_000   # Try lowering this value in case of "Errno 5"

# 3 switchs definition
listaPul = ['confirm', 'back', 'push']
CONFIRM = 18
BACK = 19
PUSH = 20

# Define el manejador de interrupciones asociadas a los pulsadores
teclas = [] # guarda las teclas presionadas
last_time = 0 # guarda la ultima marca de tiempo en que se presiono el pulsador
def manejaPulsadores(pin):
    
    global teclas, last_time
    new_time = ticks_ms()
    # Si ha pasado mas de 200ms desde el ultimo evento, temenos un nuevo evento. Evita los REBOTES
    if time.ticks_diff(new_time, last_time) > 400: 
        teclas.append(listaPul[int(str(pin).split(",")[0][8:]) - CONFIRM])
        # Si la interrupcion vien del pulsador 'back' en GPIO19
        # objeto 'pin' devuelve por ejemplo 'Pin(GPIO19, mode=IN)' si lo pasamos a str
        # slip(",") parte por la coma en una lista ['Pin(GPIO19', ' mode=IN)']
        # [0][8:] toma del primero de la lista los caracteres del 8 al final, y lo pasa a int
        # 'Pin(GPIO19'[8:] -> '19'
        # y resta el valor de CONFIRM = 18 , dando 1
        # busca en listaPul[1] => 'back'
        last_time = new_time
        
# los 2 pines del Rotary Encoder, si el incremento es decremento -> invertir
TRA = 16
TRB = 17
# Sensor DHT22 pin
SENSDHT = 14

# Sensor Tank
SENSTPIN = 22

# GPIO para alimentar sensores Tank y humedad suelo
POWERSENS = 21

# Sensor humedad suelo
SOILMOISTADC = 0 # es el ADC0
sensorSoil = ADC(SOILMOISTADC)

MAXVOLT = 3.28
SOILVOLTCONV = MAXVOLT / (65535)

# Motor bomba pin
MOTORPIN = 15

# ------ INICIALIZACIONES --------
# 1.0 pone a parpadear el led interno con periodo de 1 segundo
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

ToplineStr = f"Riego A off-v{p_version}"
display.text(ToplineStr, 0, TopLy, 1)
display.hline(0, TopLhy,128,1)
display.text('OK: Disp...', 0, FstLy, 1)
textobig = "HW Init Run"
Writer.set_textpos(display, TrdLy, 0)  
wri.printstring(textobig)
display.hline(0, StatLhy,128,1)
display.text('Booting...', 0, StatLy, 1)
display.show()


# 1.2 Creacion de pulsadores
 
confPul = Pin(CONFIRM, Pin.IN) # pull up por circuito
backPul = Pin(BACK, Pin.IN) # pull up por circuito
pushPul = Pin(PUSH, Pin.IN) # pull up por circuito

confPul.irq(trigger=Pin.IRQ_FALLING, handler=manejaPulsadores)

backPul.irq(trigger=Pin.IRQ_FALLING, handler=manejaPulsadores)

pushPul.irq(trigger=Pin.IRQ_FALLING, handler=manejaPulsadores)

# 1.3 Rotary encoder
# Creacion  del objeto Rotray encoder con 10 opciones 
re = RotaryIRQ(
    pin_num_clk=TRB,
    pin_num_dt=TRA,
    min_val=0,
    max_val=9, # Rotary encoder 10 posiciones 
    reverse=False,
    incr=1,
    range_mode=RotaryIRQ.RANGE_WRAP,
    # pull_up=True, # si pull up por circuito -> comenta
    half_step=False,
    )

display.fill_rect(0, FstLy, WIDTH, 8, 0)
display.text('OK: Dis/3sw/RE', 0, FstLy, 1)
display.show()

# 1.4 Crea el sensor DHT22 
sensorDHT = DHT22(Pin(SENSDHT))
alimentaSensor = Pin(POWERSENS, Pin.OUT)

sleep(2) # maximun sampling rate in cas eof DHT22
sensorDHT.measure() # order a measure
temp=sensorDHT.temperature () # simple copy of last measure Temp
hum=sensorDHT.humidity() # simple copy of last measure Humidity
print (f"T={temp:02.2f} ºC, H={hum:02.2f} %")
display.fill_rect(0, FstLy, WIDTH, 8, 0)
display.text('OK:Dis/3sw/RE/TH', 0, FstLy, 1)
display.text(f'T={temp:02.1f}C H={hum:02.1f}%', 0, SndLy, 1)
display.show()
    
# 1.5 Crea el motor bomba
motorPwm = PWM(Pin(MOTORPIN))
motorPwm.freq(1000)
motorPwm.duty_u16(0) # stop motor

motorpor100 = 50 # fijamos inicialmente a 50% del regimen del motor cuando arranque
# pasamos a dutty cycle  de 0 a 65_000
motorpor60mil = int(65535 * motorpor100 / 100)

# 1.6 Sensor de humedad de suelo
sensorSoil = ADC(SOILMOISTADC)

# 1.7 Crea el sensor del tanque y GPIO que alimenta los sensores 
sensorTank = Pin(SENSTPIN, Pin.IN)
alimentaSensor = Pin(POWERSENS, Pin.OUT)

# lee valor del sensor del Tanke y del suelo
alimentaSensor.on()
sleep(2)
lastsensorTank = sensorTank.value() # '1' Tank Empty / '0' Tank FULL

lastsensorSoilraw = sensorSoil.read_u16()
alimentaSensor.off()

lastsensorSoilvolt = lastsensorSoilraw * SOILVOLTCONV
print(f"Soil volts = {lastsensorSoilvolt:.2f} voltios | Valor ADC bruto = {lastsensorSoilraw}")
display.fill_rect(0, SndLy, WIDTH, 8, 0)
display.text('motor/Soil/Tank', 0, SndLy, 1)
display.show()

if lastsensorTank :
    print("AVISO: Tanque VACIO")
    display.fill_rect(0, StatLy, WIDTH, 8, 0)
    display.text('Tank EMPTY', 0, StatLy, 1)   
    
else:
    print("Tanque LLENO")
    display.fill_rect(0, StatLy, WIDTH, 8, 0)
    display.text('Tank NO empty', 0, StatLy, 1)

display.fill_rect(0, TrdLy, WIDTH, WIDTH_VA, 0) # borra 3ra linea x21 alto
textobig = "HW Init End"
Writer.set_textpos(display, TrdLy, 0)  
wri.printstring(textobig)
display.show() 

# Si inicializacion es Ok apaga el led interno
iledtim.deinit()
sleep(1)
iled.off()

# ------ FIN DE inicializacion --------


 


