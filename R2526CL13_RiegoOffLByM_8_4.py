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
# 7.1 -> 7.2 tanque a texto grueso + status salir / seguir
# Montaje #8 : detector del tanque vacio por flotador en GPIO01
# 8.2 entrar y salir de bucle principal
# 8.3 visualizacion del display con funcion unica + opciones se ejecutan vacias pero Ok
# 8.4 se eliminan comentario decodigo antiguo de display

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
p_keyOhw = "Soils sesnsor on ADC0 - pata + a GPIO21 + displ SH1106 gpio4&5"
p_project = "Riego Automatico (flotador) Inicializacion y Main - Off Line "
p_version = "8.4"
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
FrdLy = 41
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
    if ticks_diff(new_time, last_time) > 400: 
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
# SENSTPIN = 22 # sensor resistivo del tanque
TANKPIN = 1

# GPIO para alimentar sensores Tank y humedad suelo
POWERSENS = 21

# Sensor humedad suelo
SOILMOISTADC = 0 # es el ADC0
sensorSoil = ADC(SOILMOISTADC)

MAXVOLT = 3.28
SOILVOLTCONV = MAXVOLT / (65535)

# Motor bomba pin
MOTORPIN = 15

# Control de bucle principal
NotExit = True

# Definicion de menus Acciones

def showAirTH():
    return 'DONE AirTH'

def showSoilVolt():
    return 'DONE SoilV'

def showSoilHum():
    return 'DONE SoilH'

def checkTank():
    return 'DONE cTank'

def checkMotor():
    return 'DONE cMoto'

def doNothing():
    return 'DONE Noth'

MENU = [[showAirTH, 'Air ºC Hum'],
        [showSoilVolt,'Soil Volts'],
        [showSoilHum, 'Soil Hum'],
        [checkTank, 'Check Tank'],
        [checkMotor, 'Check Motor'],
        [doNothing, 'Do nothing'],
        [doNothing, 'Do nothing'],
        [doNothing, 'Do nothing'],
        [doNothing, 'Do nothing'],
        [doNothing, 'Do nothing']]

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

# 1.1.4 Funciones de Dibujo del display
ToplineStr = f"Riego A off-v{p_version}" # No se cambiara en todo el programa

def ShowDisp3LinB(l1, l2, l3b, ls, Erase = True, Show = True):
    """ funcion generica de display """
    if Erase:
        display.fill(0)
        
    display.text(ToplineStr, 0, TopLy, 1)
    display.hline(0, TopLhy,128,1)
    display.fill_rect(0, FstLy, WIDTH, 8, 0)
    display.text(l1, 0, FstLy, 1)
    display.fill_rect(0, SndLy, WIDTH, 8, 0)
    display.text(l2, 0, SndLy, 1)
    
    display.fill_rect(0, TrdLy, WIDTH, WIDTH_VA, 0) # borra 3ra linea x21 alto
    Writer.set_textpos(display, TrdLy, 0)  
    wri.printstring(l3b)
    display.hline(0, StatLhy,128,1)
    display.text(ls, 0, StatLy, 1)
    
    if Show:
        display.show()

# END display functions ----------------    
ShowDisp3LinB('OK: Disp...', '', 'HW Init Run', 'Booting...')

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
    max_val=(len(MENU)-1), # Rotary encoder 10 posiciones 
    reverse=False,
    incr=1,
    range_mode=RotaryIRQ.RANGE_WRAP,
    # pull_up=True, # si pull up por circuito -> comenta
    half_step=False,
    )

ShowDisp3LinB('OK: Dis/3sw/RE', '', 'HW Init Run', 'Booting...')

# 1.4 Crea el sensor DHT22 
sensorDHT = DHT22(Pin(SENSDHT))
alimentaSensor = Pin(POWERSENS, Pin.OUT)

sleep(2) # maximun sampling rate in cas eof DHT22
sensorDHT.measure() # order a measure
temp=sensorDHT.temperature () # simple copy of last measure Temp
hum=sensorDHT.humidity() # simple copy of last measure Humidity
print (f"T={temp:02.2f} ºC, H={hum:02.2f} %")

ShowDisp3LinB('OK: Dis/3sw/RE', f'T={temp:02.1f}C H={hum:02.1f}%', 'HW Init Run', 'Booting...')
    
# 1.5 Crea el motor bomba
motorPwm = PWM(Pin(MOTORPIN))
motorPwm.freq(1000)
motorPwm.duty_u16(0) # stop motor

motorpor100 = 50 # fijamos inicialmente a 50% del regimen del motor cuando arranque
# pasamos a dutty cycle  de 0 a 65_000
motorpor60mil = int(65535 * motorpor100 / 100)

# 1.6 Sensor de humedad de suelo y GPIO que alimenta los sensores 
sensorSoil = ADC(SOILMOISTADC)
alimentaSensor = Pin(POWERSENS, Pin.OUT)

# 1.7 Crea el sensor del tanque 
sensorTank = Pin(TANKPIN, Pin.IN)

# lee valor del sensor del Tanque y del suelo
alimentaSensor.on()
sleep(2)
lastsensorTank = not sensorTank.value() # sensor flotador logica '1' : lleno
# float sensor logic '1' = tank FULL

lastsensorSoilraw = sensorSoil.read_u16()
alimentaSensor.off()

lastsensorSoilvolt = lastsensorSoilraw * SOILVOLTCONV
print(f"Soil volts = {lastsensorSoilvolt:.2f} voltios | Valor ADC bruto = {lastsensorSoilraw}")

ShowDisp3LinB('OK: Dis/3sw/RE', 'motor/Soil/Tank', 'HW Init Run', 'Booting...')

if lastsensorTank :
    print("AVISO: Tanque VACIO / Tank EMPTY")
    tankStatus = 'Tank EMPTY'   
else:
    print("Tanque LLENO / Tank FULL")
    tankStatus = 'Tank FULL'

ShowDisp3LinB('OK: Dis/3sw/RE', 'motor/Soil/Tank', tankStatus, 'Booting...')

iledtim.deinit()
sleep(1)
iled.off()
# ------- Fin de incializacion --------

ShowDisp3LinB('OK: Dis/3sw/RE', 'motor/Soil/Tank', tankStatus, 'Exit BACK/go CON')

# paso al bucle principal o salir
while not('back' in teclas) and not('confirm' in teclas):
    pass

if teclas != [] and teclas[0] == 'back':
    NotExit = False
    teclas = []
    
if teclas != [] and teclas[0] == 'confirm':
    NotExit = True
    teclas = []
    

# 3- BUCLE PRINCIPAL --> solo 1 capa de menu
while NotExit:
    option = re.value()
    optionStr = MENU[option][1] # lee la opcion del menu en texto para humanos
    print('Menu option = ', optionStr, end='\r')
    ShowDisp3LinB('Rotate menu', 'Go press CON but', optionStr, 'Go CON/Stop BACK')
    
    if teclas != [] and teclas[0] == 'back':
        NotExit = False # hace que salga del bucle principal en la siguiente vuelta
        teclas = []
    
    if teclas != [] and teclas[0] == 'confirm':
        teclas = []
        print('Going Menu option = ', optionStr)
        # simula opcion menu screen
        orden = MENU[option][0] # las funcione sPython son objetos
        returnOrden = orden() # ejecuta al orden correspondiente del menu
        ShowDisp3LinB('Done Option', '', returnOrden, 'return menu BACK')
        
        while not('back' in teclas):
            pass
        teclas = []     

# Sale del bucle principal
alimentaSensor.off()
motorPwm.duty_u16(0) # stop motor
print("Parada de usuario por tecla BACK")
ShowDisp3LinB('See you', 'next time', 'Exit done', 'Stop by button B')

