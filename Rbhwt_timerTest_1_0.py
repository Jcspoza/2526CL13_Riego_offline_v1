from machine import Pin, Timer
from time import sleep

# opion 1
# tim = Timer()
# tim.init(period=2000, mode=Timer.PERIODIC, callback=lambda t:print(2))

# opcion corta
iled = Pin("LED", Pin.OUT)
tim = Timer(period=1000, mode=Timer.PERIODIC, callback=lambda t:iled.toggle())
sleep(5)
tim.init(period=250,mode=Timer.PERIODIC, callback=lambda t:iled.toggle())
sleep(5)
tim.deinit()
sleep(1)
iled.off()
