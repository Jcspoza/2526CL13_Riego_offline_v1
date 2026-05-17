# 2526CL13_Riego_offline v1 - ~~borrador i~~

Clase 13- Prototipo de Riego automático off line v1

Indice evolutivo del las clases del taller + libros y webs de referencia:

[GitHub - Jcspoza/2526_PyR_Index: Curso Programación y Robotica 2025 2026 - CMM BML](https://github.com/Jcspoza/2526_PyR_Index)

---

## Proyecto Riego-> Montaje completo ver sin conexión v1

En esta lección vamos a **montar todos los elementos del Proyecto de riego automatico**, sin incluir conexión a internet 

---

## Clase13 - Indice

- Resumen inicial
  
  - Tópicos que se van a aprender
  
  - Lista de materiales
  
  - Links a Tutoriales e informacion
  
  - Librerías usadas
  
  - Tabla resumen de programas

- Panorama de Conexiones de todos los elementos

- Punto de partida M#5 F_2 de CL11

- TO DO y Notas
  
  ---

## Resumen inicial

### Tópicos que se van a aprender / repasar

| Topico                     | Detalle                                                                                                                 | Links |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ----- |
| Sensores humedad suelo     |                                                                                                                         |       |
| Transistores BJC en activa |                                                                                                                         |       |
| Libreria writer            | Permite para usar tipos y tamaños de letra en displays B/N, que normalmente solo usan el tipo basico de framebuffer 8x8 |       |
| Excepciones                |                                                                                                                         |       |

### Lista de Materiales

| Material                                                                                                        | Descripcion                                                                                                                                                                                        | Kit SF                                  | Montaje |
| --------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- | ------- |
| [Protoboard 700](https://docs.sunfounder.com/projects/kepler-kit/en/latest/component/component_breadboard.html) | Placa para prototipos ver apartado [Uso de la protoboard](https://github.com/Jcspoza/2526CL1_R_CircElect0#uso-de-la-protoboard). Mejor usar la protoboard de 700                                   | SI                                      | Todos   |
| [Cables dupond M-M](https://docs.sunfounder.com/projects/kepler-kit/en/latest/component/component_wire.html)    | Sirven para hacer conexiones en protoboard                                                                                                                                                         | SI                                      | Todos   |
| Pico W, 2W                                                                                                      | Vale cualquiera de los 4 modelos de Pico                                                                                                                                                           | SI                                      | Todos   |
| DHT22                                                                                                           | Sensor de temperatura e Humedad aire - protocolo 1 hilo / **COMPROBAR EN INICIALIZACION**                                                                                                          | NO , esta el DHT11 peor caracteristicas |         |
| Rdhtpullup = 4,7k o similar                                                                                     | circuito DHT22                                                                                                                                                                                     |                                         |         |
| Sensor Humedad de suelo tipo sparkfun                                                                           | Lo hemos sustituido en muchos montajes por un potenciómetro - salida pin analógico                                                                                                                 | NO                                      |         |
| Sensor humedad con comparador                                                                                   | Lo usaremos para ver si el deposito esta lleno - salida digital 1 pin                                                                                                                              | NO                                      |         |
| Display SH1106 + R. encoder  pulsadores                                                                         | Display Grafico 1128 x 60 pixels blanco y negro, protocolo I2C 3,3 volt + Circuitería de Rotary encoder + Circuitería de 3 pulsadores con circuitos anti rebotes / **COMPROBAR EN INICIALIZACION** | No , pero comprado por todos            | Mon#    |
| Motor bomba                                                                                                     | Motor de bomba con salida tubo vertical. 3,3 a 4.5 volt , 430 mA de corriente máxima a 5 volt                                                                                                      | SI                                      |         |
| Transistor NPN BJC tipo S8050                                                                                   | usado en circuito de motor, requiere una Ic > 450mA                                                                                                                                                |                                         |         |
| Diodo tipo 1N4007                                                                                               | Diodo fly-back del circuito de motor                                                                                                                                                               |                                         |         |
| Rb = 2k, Rbpulldoun= 10k                                                                                        | circuito de motor                                                                                                                                                                                  |                                         |         |

### Links a informacion

| Tema | Link |
| ---- | ---- |
|      |      |
|      |      |

### Librerías usadas

Comprobar que estén en la menoría de la PICO y preferentemente en /lib. si no estan copiar los ficheros a /lib

Seguramente 'writer.py' no estará.

| Libreria                       | Uso para                                                                                                     | Link                                                                                                                                                            |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [sh1106.py](sh1106.py)         | manejo del display b/n grafico SH1106 de 1.3 pulgadas y128 x 64 pixeles                                      | [GitHub - robert-hh/SH1106: MicroPython driver for the SH1106 OLED controller · GitHub](https://github.com/robert-hh/SH1106)                                    |
| [writer.py](writer.py)         | Permite el uso de varios tipos y tamaños de letra en displays b/n, como el ssd1306 y el SH1106 ( el nuestro) | [micropython-font-to-py/writer at master · peterhinch/micropython-font-to-py · GitHub](https://github.com/peterhinch/micropython-font-to-py/tree/master/writer) |
| [freesans20.py](freesans20.py) | Letra alternativa a usar con writer                                                                          |                                                                                                                                                                 |
| [inkfree20.py](inkfree20.py)   | Letra alternativa a usar con writer                                                                          |                                                                                                                                                                 |
|                                | DHT22                                                                                                        | ](R2526CL11_ADC_pVgDisp_5F_2.py)                                                                                                                                |

### Tabla resumen de programas

Todos los programas en microPython

| Programa                                                       | Montaje  | HW si Robotica y Notas                                                | Objetivo de Aprendizaje |
| -------------------------------------------------------------- | -------- | --------------------------------------------------------------------- | ----------------------- |
| [R2526CL11_ADC_pVgDisp_5F_2.py](R2526CL11_ADC_pVgDisp_5F_2.py) | CL11 M#5 | Elijo el control de flujo por ser mas simple, v2 con mejoras visuales |                         |
|                                                                |          |                                                                       |                         |
|                                                                |          |                                                                       |                         |
|                                                                |          |                                                                       |                         |
|                                                                |          |                                                                       |                         |
|                                                                |          |                                                                       |                         |
|                                                                |          |                                                                       |                         |

---

## Panorama de Conexiones de todos los elementos

| GPIOs            | Pin proto | Elemento HW | Alimentación y Notas |
| ---------------- | --------- | ----------- | -------------------- |
| GPIO04  + GPIO05 | 6         |             |                      |
|                  |           |             |                      |
|                  |           |             |                      |
|                  |           |             |                      |
|                  |           |             |                      |
|                  |           |             |                      |
|                  |           |             |                      |
|                  |           |             |                      |
