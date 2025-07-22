# This file is executed on every boot (including wake-boot from deepsleep)
from machine import Pin
from otaDir.configOTA import updateGPIO
con = Pin(updateGPIO, Pin.IN, Pin.PULL_UP)
if con.value() == 0:
    import otaDir.ota
    otaDir.ota.main()