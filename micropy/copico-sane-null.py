import time
from time import sleep

import machine
from machine import Pin

Led = Pin("LED", Pin.OUT)
Direction = Pin(26, Pin.OUT)
GHalt = Pin(27, Pin.OUT)
GSlenb = Pin(28, Pin.OUT)

Led.value(1)
Direction.value(1)
GHalt.value(0)
GSlenb.value(0)

while True:
    pass
