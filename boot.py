from machine import Pin
from configOTA import updateGPIO
con = Pin(updateGPIO, Pin.IN, Pin.PULL_UP)
if con.value() == 0:
    import ota
    ota.main()
