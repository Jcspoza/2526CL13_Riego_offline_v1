# Taller Programación y Robótica en CMM BML – 2024 -2025 - Clase 10
# Programa: Show graphic commnads I2C sh1106 by Rotrary Encoder and 3 switch
# Hardware platform: Pico _ & W / funciona igual sin cambios
# Librerias : sh1106.py
# Ref librerias: https://github.com/robert-hh/SH1106
# Fecha JCSP 2023 03 09
# Licencia : CC BY-NC-SA 4.0
# Add Learning topics : Design a program to mange a menu + use functions as objets
# Ref: https://www.coderdojotc.org/micropython/displays/graph/03-basic-drawing/
# Ref 2 : https://www.esploradores.com/oledsh_ssd1306/
# Ref 3 : https://docs.micropython.org/en/latest/library/framebuf.html
#
# Partiremos del show grafico versión 1.0 haciendo los siguientes cambios,
# que incorporaremos de forma progresiva chequeando que funcionen:# 
# 1. Quitamos las esperas temporizadas --> se espera a pulsar un botón   
# 2. El menú de opciones se mostrara con el rotary encoder ( modo wrap)   
# ver 3.0 Evolucionaremos el menu a letra mas grande

from os import uname
# Informative block - start
p_keyOhw = "SH1106 I2C en GPIO4&5=SDA0 & SCL0 400khz + RE GPIO16/17 + 3switch 18,19 20"
p_project = "Graphic commands show carrusel -with RE & e switchs"
p_version = "3.0"
p_library = "SH1106  @robert-hh"
print(f"uPython version: {uname()[3]} ")
print(f"uC: {uname()[4]} - Key other HW: {p_keyOhw}")
print(f"Program: {p_project} - Version: {p_version}")
print(f"Key Library: {p_library}")

from machine import Pin, I2C
import sh1106
import array # necesario para coor de poligonos 
import time
from rotary_irq_rp2 import RotaryIRQ
from writer import Writer
# Font
import inkfree20 as font

# 0.0 - Constates y varaibles globales
WIDTH =128 
HEIGHT= 64
FREQ = 400_000   # Try lowering this value in case of "Errno 5"


# 0.1- los 2 pines del Rotary Encoder, si el incremento es decremento -> invertir
TRA = 16
TRB = 17

# 0. 1 Definition de los 3 switchs
listaPul = ['confirm', 'back', 'push']

CONFIRM = 18
BACK = 19
PUSH = 20
confPul = Pin(CONFIRM, Pin.IN) # pull up por circuito
backPul = Pin(BACK, Pin.IN) # pull up por circuito
pushPul = Pin(PUSH, Pin.IN) # pull up por circuito

# 0.3 Configura interrupciones asociadas a los pulsadores
teclas = [] # guarda las teclas presionadas
last_time = 0 # guarda la ultima marca de tiempo en que se presiono el pulsador

def manejaPulsadores(pin):
    
    global teclas, last_time
    new_time = time.ticks_ms()
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
        
confPul.irq(trigger=Pin.IRQ_FALLING, handler=manejaPulsadores)

backPul.irq(trigger=Pin.IRQ_FALLING, handler=manejaPulsadores)

pushPul.irq(trigger=Pin.IRQ_FALLING, handler=manejaPulsadores)


def show_rect():
    """Display in oledsh a rectangule 20 x 16"""
    oledsh.rect(WIDTH//2 - 10, HEIGHT//2 - 8, 20, 16, 1) # x0, y0, size hor, size vert , color
    return "Rectangulo 20x16"

def show_Frect():
    """Display in oledsh a filled rectangule 20 x 16"""
    oledsh.fill_rect(WIDTH//2 - 10, HEIGHT//2 - 8, 20, 16, 1) # x0, y0, size hor, size vert , color
    return "Rect Lleno 20x16"

def show_invert():
    """Invert Display """
    oledsh.fill_rect(WIDTH//2 - 10, HEIGHT//2 - 8, 20, 16, 1) # x0, y0, size hor, size vert , color
    oledsh.invert(1)
    return "Invierte oledsh"

def show_normal():
    """Invert Display """
    oledsh.fill_rect(WIDTH//2 - 10, HEIGHT//2 - 8, 20, 16, 1) # x0, y0, size hor, size vert , color
    oledsh.invert(0)
    return "Normal oledsh"
    
def show_circ():
    """Display in oledsh a circule r= 20"""
    oledsh.ellipse(WIDTH//2, HEIGHT//2, 20, 20, 1) # x0, y0, radius, color
    return "Circulo r=30"

def show_ellipse():
    """Display in oledsh an ellipse rx= 40, ry=20"""
    oledsh.ellipse(WIDTH//2, HEIGHT//2, 40, 20, 1) # x0, y0, radius X, radius Y, color
    return "Ellipse (40,20)"

def show_QFellipse():
    """Display in oledsh a 1/4 ellipse rx= 40, ry=20"""
    oledsh.ellipse(WIDTH//2, HEIGHT//2, 40, 20, 1, True, 10) # x0, y0, radius X, radius Y, color, filled
    # last param is quarter ellipse indicator 1bit last 4
    # 0001 top right
    # 0010 top left
    # 0100 bottom left
    # 1000 bottom right
    return "Ellip 2q (40,20)"

def show_triangle():
    """Display in oledsh a triangle """
    cor = array.array('h',[60, 0, 30, 40, 90, 40])
    oledsh.poly(0, 10, cor, 1) 
    return "Triangle (63,10)"

def show_pentagono():
    """Display in oledsh a pentagono """
    cor = array.array('h',[60, 0, 15, 20, 30, 40, 90, 40, 105, 20])
    oledsh.poly(0, 10, cor, 1) # x0, y0, coor[x0,y0, x1,y1, x2, y2...], color
    return "Pentagon (63,10)"

MENU = [[show_rect, 'Rectangulo'],
        [show_circ,'Circulo'],
        [show_ellipse, 'Elipse'],
        [show_triangle, 'Triangulo'],
        [show_pentagono, 'Pentagono'],
        [show_Frect, 'Rect Lleno'],
        [show_QFellipse, 'Elipse 2cuartos'],
        [show_invert, 'Pant Invertida'],
        [show_normal, 'Pantalla Normal']]


# 0.1 Objeto I2C y LCD
i2c = I2C(0, sda = Pin(4), scl = Pin(5), freq = FREQ)
print('Info del bus i2c: ',i2c)

oledsh = sh1106.SH1106_I2C(WIDTH, HEIGHT , i2c, addr = 0x3c, rotate = 0) # constructor - I2C direccion 3C por defecto
oledsh.sleep(False)

#0.2- Creacion  del objeto RE
r = RotaryIRQ(
    pin_num_clk=TRB,
    pin_num_dt=TRA,
    min_val=0,
    max_val=(len(MENU)-1),
    reverse=False,
    incr=1,
    range_mode=RotaryIRQ.RANGE_WRAP,
    # pull_up=True, # si pull up por circuito -> comenta
    half_step=False,
    )
# 0.3 Creacion del objeto writer
wri = Writer(oledsh, font, verbose = False) # verbose = False to suppress console output

# 1- Programa Principal - Presentacion
oledsh.fill(0) # clear screen
oledsh.show()

oledsh.fill(0)
oledsh.text("Test", (WIDTH - len("Test")*8) // 2, 0)
oledsh.text("de", (WIDTH - len("de")*8) // 2, 16)
oledsh.text("Comand Graficos", (WIDTH - len("Comand Graficos")*8) // 2, 32)
oledsh.text("version " + p_version, 0, 44)
msgL8 = "Tecla->comenzar"
oledsh.text(msgL8, (WIDTH - len(msgL8)*8) // 2, 55, 1)
oledsh.show()
while True:
    #utime.sleep(1)
    if teclas != []:        
        teclas = []
        oledsh.fill(0)
        oledsh.show()
        break

opcion = r.value()

try:
    while True:
        oledsh.fill(0)
        oledsh.text("Test de graficos",0,0,1)
        Writer.set_textpos(oledsh, 20, 8)
        msgL4 = MENU[opcion][1]
        wri.printstring(msgL4)        
        msgL8 = 'Ver->Confirm'
        oledsh.text(msgL8, (WIDTH - len(msgL8)*8) // 2, 55, 1)
        oledsh.show(True) # hace que se actualicen todas las paginas, si no no funciona
        opcion = r.value()
        if teclas != [] and teclas[0] == 'confirm':
            teclas = []
            oledsh.fill(0)
            orden = MENU[opcion][0]
            msgL1 = orden()
            msgL8 = 'Volver->Back'
            oledsh.text(msgL1, (WIDTH - len(msgL1)*8) // 2, 0, 1)
            oledsh.text(msgL8, (WIDTH - len(msgL8)*8) // 2, 55, 1)
            oledsh.show(True) # hace que se actualicen todas las paginas, si no no funciona
            while not('back' in teclas):
                pass
            teclas = []
#             while True:
#                 if :
#                     teclas = []
#                     break
                                           
except KeyboardInterrupt: #  si CTRL+C se presiona - > limpiar display
    oledsh.fill(0)
    oledsh.show()

