import time
from time import sleep

import machine, rp2
from machine import Pin
from rp2 import PIO

Led = Pin("LED", Pin.OUT)
Halt = Pin(13, Pin.OUT)
Slenb = Pin(14, Pin.OUT)
Dir = Pin(15, Pin.OUT)
ResetN = Pin(8, Pin.IN)
EClock = Pin(9, Pin.IN)
WriteC = Pin(10, Pin.IN)
WriteD = Pin(11, Pin.IN)
ReadD = Pin(12, Pin.IN)

Led.value(1)
Halt.value(0)
Slenb.value(0)
Dir.value(1)

OH, OL, IH = PIO.OUT_HIGH, PIO.OUT_LOW, PIO.IN_HIGH
@rp2.asm_pio(
    out_init=tuple(8 * [IH]),   # 0-7: D0-D7
    sideset_init=(OH, OL, OH),  # 13:Halt 14:Slenb 15:dir
    out_shiftdir=PIO.SHIFT_RIGHT, # 8 bits at a time
    autopull=True,
    pull_thresh=32,
    )
def onreset_unhalt_prog():
    e = 9
    wait(0, gpio, e)# sync
    wait(1, gpio, e)# e hi
    wait(0, gpio, e)# e lo
    set(x, 3)         .side(0b100) # loop 4x # halt=0 slenb=0 dir=1 # Unhalts the M6809
    
    label("four")
    wait(1, gpio, e) # e hi
    wait(0, gpio, e) # e lo
    jmp(x_dec, "four")
    
    out(pindirs, 8)   .side(0b010) # direction OUT and SLENB
    out(pins, 8)                   # output a byte
    wait(1, gpio, e) # e hi
    wait(0, gpio, e) # e lo
    out(pins, 8)                   # output another byte
    wait(1, gpio, e) # e hi
    wait(0, gpio, e) # e lo
    out(pindirs, 8)   .side(0b100) # direction IN and NOT SLENB
    label("inf")
    jmp("inf")
    


while ResetN.value()==1: pass  # wait for drop
sleep(0.1)                     # debounce
Halt.value(1)                  # halt while resetting
while ResetN.value()==0: pass  # wait for ResetN to release
sleep(0.5)                     # debounce and wait to sync on Halt
sm = rp2.StateMachine(
    0,  # which pio
    onreset_unhalt_prog,
    freq=125_000_000,
    sideset_base=Halt,
    out_base=0,
)
# sm.put(0x0027a0ff)
sm.put(0x0027a0ff)

sm.active(True)

print("running...")
while True:
    pass
