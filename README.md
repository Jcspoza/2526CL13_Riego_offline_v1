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

Resumen inicial

### Tópicos que se van a aprender / repasar

| Topico                     | Detalle                                                                                                                 | Links |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ----- |
| Sensores humedad suelo     |                                                                                                                         |       |
| Transistores BJC en activa |                                                                                                                         |       |
| Libreria writer            | Permite para usar tipos y tamaños de letra en displays B/N, que normalmente solo usan el tipo basico de framebuffer 8x8 |       |
| Excepciones                |                                                                                                                         |       |

### Lista de Materiales

| Material                                                                                                        | Descripcion                                                                                                                                                      | Kit SF                       | Montaje |
| --------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- | ------- |
| [Protoboard 700](https://docs.sunfounder.com/projects/kepler-kit/en/latest/component/component_breadboard.html) | Placa para prototipos ver apartado [Uso de la protoboard](https://github.com/Jcspoza/2526CL1_R_CircElect0#uso-de-la-protoboard). Mejor usar la protoboard de 700 | SI                           | Todos   |
| [Cables dupond M-M](https://docs.sunfounder.com/projects/kepler-kit/en/latest/component/component_wire.html)    | Sirven para hacer conexiones en protoboard                                                                                                                       | SI                           | Todos   |
| Pico _, 2, W, 2W                                                                                                | Vale cualquiera de los 4 modelos de Pico                                                                                                                         | SI                           | Todos   |
|                                                                                                                 |                                                                                                                                                                  |                              |         |
|                                                                                                                 |                                                                                                                                                                  |                              |         |
|                                                                                                                 |                                                                                                                                                                  |                              |         |
|                                                                                                                 |                                                                                                                                                                  |                              |         |
|                                                                                                                 |                                                                                                                                                                  |                              |         |
|                                                                                                                 |                                                                                                                                                                  |                              |         |
| Display SH1106 + R. encoder  pulsadores                                                                         |                                                                                                                                                                  | No , pero comprado por todos | Mon#    |

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

### Tabla resumen de programas

Todos los programas en microPython

| Programa                                                           | Montaje | HW si Robotica y Notas                                                                  | Objetivo de Aprendizaje                                                                 |
| ------------------------------------------------------------------ | ------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| [R2526CL11_ADC_poten_1_0.py](R2526CL11_ADC_poten_1_0.py)           | M#1     | potenciómetro pin central en ADC0, otros 2 pines +3.3v y 0volt                          | Recordar lectura ADC                                                                    |
| [R2526CL11_ADC_poten_1_1.py](R2526CL11_ADC_poten_1_1.py)           | M#1     | idem + formula mapeo mas precisa                                                        |                                                                                         |
| [R2526CL11_ADC_potVccgpio_2_0.py](R2526CL11_ADC_potVccgpio_2_0.py) | M#2     | potenciómetro uno de los ines extremso a GPIO21 -> evitar corrosión + excepciones       | simular montaje de sensor  humedad con potenciómetro                                    |
| [R2526CL11_ADC_potVccgpio_2_1.py](R2526CL11_ADC_potVccgpio_2_1.py) | M#2     | mejoras de presentación , misma linea                                                   | idem                                                                                    |
| [Rbhwt_sh1106_1_0.py](Rbhwt_sh1106_1_0.py)                         | M#3     | **Prueba básica** de HW del display SH1106                                              | requiere libreria 'sh1106.py'                                                           |
| [R2526CL11_ADC_pVgDisp_3_3.py](R2526CL11_ADC_pVgDisp_3_3.py)       | M#3     | Añadir display b/n SH1106                                                               | Hacer el montaje mas autónomo ( sin pc) + requiere libreria 'sh1106.py'                 |
| [Rbhwt_sh1106_writer_1_0.py](Rbhwt_sh1106_writer_1_0.py)           | M#4     | **prueba basica** de letra grande en display SH1106                                     | requiere libreria 'sh1106.py' + 'writer.py' + una fuente de letra                       |
| [R2526CL11_ADC_pVgDisp_4_0.py](R2526CL11_ADC_pVgDisp_4_0.py)       | M#4     | leer pot con Vcc en gpio21 + sh1106 + letra grande                                      | requiere libreria 'sh1106.py' + 'writer.py' + una fuente de letra                       |
| [R2526CL11_ADC_pVgDisp_4_1.py](R2526CL11_ADC_pVgDisp_4_1.py)       | M#4     | idem con mejoras 1                                                                      | requiere libreria 'sh1106.py' + 'writer.py' + una fuente de letra                       |
| [R2526CL11_ADC_pVgDisp_4_2.py](R2526CL11_ADC_pVgDisp_4_2.py)       | M#4     | idem con mejoras 2                                                                      |                                                                                         |
| [Rbhwt_sh1106RE3sw_Testsw1_0.py](Rbhwt_sh1106RE3sw_Testsw1_0.py)   | M#5     | **prueba básic**a de manejo de <u>1 pulsador </u> con interrupciones                    |                                                                                         |
| [Rbhwt_sh1106RE3sw_Test3sw1_0.py](Rbhwt_sh1106RE3sw_Test3sw1_0.py) | M#5     | **prueba básic**a de manejo de <u>3&nbsp;pulsadores&nbsp;</u> con interrupciones        | Tiene un truco l leer el pin que provoco la interrupción, esta explicado en comentarios |
| [R2526CL11_ADC_pVgDisp_5_0.py](R2526CL11_ADC_pVgDisp_5_0.py)       | M#5     | Incorpora a 4.2 la lectura de pulsadores y , de momento no hace nada con ello           | Ver como incorporar de forma basica los pulsadores a un montaje                         |
| [R2526CL11_ADC_pVgDisp_5_1.py](R2526CL11_ADC_pVgDisp_5_1.py)       | M#5     | idem usando una función para tratamiento 'futuro' de la tecla pulsada                   |                                                                                         |
| [R2526CL11_ADC_pVgDisp_5F_1.py](R2526CL11_ADC_pVgDisp_5F_1.py)     | M#5     | Si pulso back salgo del programa de forma limpia con **control de FLUJO**               |                                                                                         |
| [R2526CL11_ADC_pVgDisp_5Ex_1.py](R2526CL11_ADC_pVgDisp_5Ex_1.py)   | M#5     | Si pulso back salgo del programa de forma limpia **con Excepción definida por usuario** |                                                                                         |
| [R2526CL11_ADC_pVgDisp_5F_2.py](R2526CL11_ADC_pVgDisp_5F_2.py)     | M#5     | Elijo el control de flujo por ser mas simple, v2 con mejoras visuales                   |                                                                                         |

---

## Resumen inicial

### Tópicos que se han aprendido y link a lección

| Topico                     | Detalle                                                                                                                 | Links |     |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ----- | --- |
| Sensores humedad suelo     |                                                                                                                         |       |     |
| Transistores BJC en activa |                                                                                                                         |       |     |
| Libreria writer            | Permite para usar tipos y tamaños de letra en displays B/N, que normalmente solo usan el tipo basico de framebuffer 8x8 |       |     |
| Excepciones                |                                                                                                                         |       |     |

### Lista de Materiales

| Material                                                                                                        | Descripcion                                                                                                                                                      | Kit SF                       | Montaje |
| --------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- | ------- |
| [Protoboard 700](https://docs.sunfounder.com/projects/kepler-kit/en/latest/component/component_breadboard.html) | Placa para prototipos ver apartado [Uso de la protoboard](https://github.com/Jcspoza/2526CL1_R_CircElect0#uso-de-la-protoboard). Mejor usar la protoboard de 700 | SI                           | Todos   |
| [Cables dupond M-M](https://docs.sunfounder.com/projects/kepler-kit/en/latest/component/component_wire.html)    | Sirven para hacer conexiones en protoboard                                                                                                                       | SI                           | Todos   |
| Pico _, 2, W, 2W                                                                                                | Vale cualquiera de los 4 modelos de Pico                                                                                                                         | SI                           | Todos   |
|                                                                                                                 |                                                                                                                                                                  |                              |         |
|                                                                                                                 |                                                                                                                                                                  |                              |         |
|                                                                                                                 |                                                                                                                                                                  |                              |         |
|                                                                                                                 |                                                                                                                                                                  |                              |         |
|                                                                                                                 |                                                                                                                                                                  |                              |         |
|                                                                                                                 |                                                                                                                                                                  |                              |         |
| Display SH1106 + R. encoder  pulsadores                                                                         |                                                                                                                                                                  | No , pero comprado por todos | Mon#    |

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
