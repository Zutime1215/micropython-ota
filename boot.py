from machine import Pin
con = Pin(15, Pin.IN, Pin.PULL_UP)
if con.value() == 0:
	import ota
	ota.main()
else:
	continue
