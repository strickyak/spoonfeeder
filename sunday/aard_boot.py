# Sane Boot Defaults that won't stop the CoCo CPU

import machine

AardLED = machine.Pin("LED", machine.Pin.OUT)

AardHalt = machine.Pin(13, machine.Pin.OUT)  # 1 = Halt CoCo
AardSlenb = machine.Pin(14, machine.Pin.OUT) # 1 = Assert SLENB to CoCo
AardDir = machine.Pin(15, machine.Pin.OUT)   # 1 = IN to PicoW from CoCo

AardLED.value(0)   # LED off
AardHalt.value(0)  # 0 = Don't HALT; run CoCo
AardSlenb.value(0) # 0 = Don't assert SLENB; CoCo device select works normally
AardDir.value(1)   # 1 = IN to PicoW from CoCo
