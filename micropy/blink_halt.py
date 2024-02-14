# For Raspberry Pi PiCOW LED plus V1/Aardvark board.
import time

import machine

led = machine.Pin("LED", machine.Pin.OUT)
halt = machine.Pin(13, machine.Pin.OUT)
slenb = machine.Pin(14, machine.Pin.OUT)
dire = machine.Pin(15, machine.Pin.OUT)

led.value(1)
halt.value(0)
slenb.value(0)
dire.value(1)
#halt.value(1)
#slenb.value(1)

#while True: pass

while True:
  led.value(0)
  halt.toggle()
  time.sleep(1)

  led.value(1)
  halt.toggle()
  time.sleep(5.0)
  
