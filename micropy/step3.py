import time
from time import sleep

import machine, rp2
from machine import Pin
from rp2 import PIO

Led = Pin("LED", Pin.OUT)
Halt = Pin(13, Pin.OUT)
Slenb = Pin(14, Pin.OUT)
Dir = Pin(15, Pin.OUT)
Trigger = Pin(16, Pin.OUT)
ResetN = Pin(8, Pin.IN)
EClock = Pin(9, Pin.IN)
WriteC = Pin(10, Pin.IN)
WriteD = Pin(11, Pin.IN)
ReadD = Pin(12, Pin.IN)

Led.value(1)
Halt.value(0)
Slenb.value(0)
Dir.value(1)
Trigger.value(0)

OH, OL, IH = PIO.OUT_HIGH, PIO.OUT_LOW, PIO.IN_HIGH
@rp2.asm_pio(
    out_init=tuple(8 * [IH]),   # 0-7: D0-D7
    sideset_init=(OH, OL, OH, OL),  # 13:Halt 14:Slenb 15:dir 16:trigger
    out_shiftdir=PIO.SHIFT_RIGHT, # 8 bits at a time
    autopull=True,
    pull_thresh=32,
    )
def onreset_prog():
    E_PIN = 9
    wait(0, gpio, E_PIN) # synchronize on a full pulse of E.
    wait(1, gpio, E_PIN) # wait until E hi
    wait(0, gpio, E_PIN) # wait until E lo

    # Unhalt at the beginning of a Cycle, so we can count cycles.
    # "direction" is the direction of the bidirectional (low voltage cmos) buffer
    # between the Coco Data Bus (D0-D7) and the Pico's GPIO0-GPIO7.
    # Out means out to the coco.  In means in from the Coco.
    # The default is IN, unless we really mean to be writing to the Coco.
    set(x, 3)         .side(0b100) # 3 means loop 4x # direction=1=IN Slenb=no Halt=no # Unhalts the M6809
    
    # Count four dead cycles (includes the one in which we unhalted).
    label("four_times")
    wait(1, gpio, E_PIN) # wait until E hi
    wait(0, gpio, E_PIN) # wait until E lo
    jmp(x_dec, "four_times")
    
    # Output the HIGH then the LOW byte of the reset vector we want.
    out(pindirs, 8)   .side(0b010) # direction=0=OUT Slenb=yes Halt=no
    out(pins, 8)                   # output HIGH byte of Reset Vector (8 bits from OSR)
    wait(1, gpio, E_PIN) # wait until E hi
    wait(0, gpio, E_PIN) # wait until E lo
    out(pins, 8)                   # output LOW byte of Reset Vector (8 bits from OSR)
    wait(1, gpio, E_PIN)  .side(0b011) # wait until E hi, Halt=yes (to halt before first instruction)
    wait(0, gpio, E_PIN) # wait until E lo
    out(pindirs, 8)   .side(0b101) # direction=1=IN, Slenb=no, Halt=yes

    # Get stuck here until the main routine re-inits this state machine.
    label("loop_forever")
    jmp("loop_forever")
    
@rp2.asm_pio(
    out_init=tuple(8 * [IH]),   # 0-7: D0-D7
    sideset_init=(OH, OL, OH, OL),  # 13:Halt 14:Slenb 15:dir 16:trigger
    out_shiftdir=PIO.SHIFT_RIGHT, # 8 bits at a time
    autopull=True,
    pull_thresh=32,
    )
def ldd_immediate_std_extended_prog():
    """This PIO program is designed to unhalt, to output 6 bytes of opcodes
       in the first six cycles, then to allow 3 more cycles to pass,
       and then halt again.  That matches a sequence like this:
         LDD #$4845  (3 instruction bytes; 3 cycles)
	 STD $0400   (3 instruction bytes; 6 cycles)
    """
    E_PIN = 9
    wait(0, gpio, E_PIN) # synchronize on a full pulse of E.
    wait(1, gpio, E_PIN) # wait until E hi
    wait(0, gpio, E_PIN) # wait until E lo

    # Three dead cycles.  We release halt during these.
    set(x, 2)              # Loop three times, so count down with X=2.
    label("three_times")
    wait(1, gpio, E_PIN) .side(0b0100) # wait until E hi # trigger=0 direction=1=IN Slenb=no Halt=no # Unhalts the M6809
    wait(0, gpio, E_PIN) # wait until E lo
    jmp(x_dec, "three_times")

    set(x, 5)         # Loop six times, so count down with X=5.
    out(pindirs, 8)   .side(0b0010) # trigger=0 direction=0=OUT Slenb=yes Halt=no
    label("six_times")
    out(pins, 8)                   # output HIGH byte of Reset Vector (8 bits from OSR)
    wait(1, gpio, E_PIN)  .side(0b0010) # wait until E hi
    wait(0, gpio, E_PIN)  .side(0b1010) # wait until E lo
    jmp(x_dec, "six_times")

    # Three more cycles will execute, but we don't have to wait for them.
    # The CPU will halt after those cycles, at the end of the instruction.
    out(pindirs, 8)   .side(0b0101) # trigger=0 direction=1=IN Slenb=no Halt=yes

    # Get stuck here until the main routine re-inits this state machine.
    label("loop_forever")
    jmp("loop_forever")

print("Step2: waiting for RESET.  ")
while ResetN.value()==1: pass  # wait for drop
print("got RESET.  ")
Led.value(0)
Halt.value(1)                  # halt while resetting
sleep(0.1)                     # debounce
print("debounced.  ")
while ResetN.value()==0: pass  # wait for ResetN to release
print("RESET gone.  ")
sleep(0.5)                     # debounce and wait to sync on Halt
print("SLEPT half a second.  ")

pio0 = rp2.PIO(0)
pio0.add_program(onreset_prog)

sm1 = pio0.state_machine(
    1,  # which state machine in pio0
    onreset_prog,
    freq=125_000_000,
    sideset_base=Halt,
    out_base=0,
)
# FF=outputs A027=reset_vector 00=inputs
sm1.put(0x0027a0ff)

Led.value(1)
sm1.active(True)
print("Activated onreset prog.  Deactivating.\n")
sm1.active(False)
pio0.remove_program(onreset_prog)
pio0.add_program(ldd_immediate_std_extended_prog)

PairsOfWords = [ # Included from io_ff78.python
        ( 0x0034ccff, 0x008001fd ),
    ( 0x0040ccff, 0x008101fd ),
    ( 0x0033ccff, 0x008201fd ),
    ( 0x00e4ccff, 0x008301fd ),
    ( 0x00f6ccff, 0x008401fd ),
    ( 0x0001ccff, 0x008501fd ),
    ( 0x0012ccff, 0x008601fd ),
    ( 0x00f7ccff, 0x008701fd ),
    ( 0x00ffccff, 0x008801fd ),
    ( 0x007accff, 0x008901fd ),
    ( 0x00f6ccff, 0x008a01fd ),
    ( 0x0001ccff, 0x008b01fd ),
    ( 0x0013ccff, 0x008c01fd ),
    ( 0x00f7ccff, 0x008d01fd ),
    ( 0x00ffccff, 0x008e01fd ),
    ( 0x007bccff, 0x008f01fd ),
    ( 0x00f6ccff, 0x009001fd ),
    ( 0x00ffccff, 0x009101fd ),
    ( 0x007accff, 0x009201fd ),
    ( 0x00f7ccff, 0x009301fd ),
    ( 0x0001ccff, 0x009401fd ),
    ( 0x0002ccff, 0x009501fd ),
    ( 0x00f6ccff, 0x009601fd ),
    ( 0x00ffccff, 0x009701fd ),
    ( 0x007bccff, 0x009801fd ),
    ( 0x00f7ccff, 0x009901fd ),
    ( 0x0001ccff, 0x009a01fd ),
    ( 0x0003ccff, 0x009b01fd ),
    ( 0x007cccff, 0x009c01fd ),
    ( 0x0001ccff, 0x009d01fd ),
    ( 0x001fccff, 0x009e01fd ),
    ( 0x00f6ccff, 0x009f01fd ),
    ( 0x0001ccff, 0x00a001fd ),
    ( 0x001fccff, 0x00a101fd ),
    ( 0x0020ccff, 0x00a201fd ),
    ( 0x00e0ccff, 0x00a301fd ),
    ( 0x0000ccff, 0x0080017e ),
]

for (w1, w2) in PairsOfWords:
  sm2 = pio0.state_machine(2) # which state machine in pio
  sm2.init(ldd_immediate_std_extended_prog,
    freq=125_000_000,
    sideset_base=Halt,
    out_base=0,
  )
  # sm2.put(0x5958CCff)  # ff=outputs CC=LDD_immediate $58='X' $59='Y'
  # sm2.put(0x000000FD)  # FD=STD_extended 00=inputs
  sm2.put(w1)  # ff=outputs CC=LDD_immediate $58='X' $59='Y'
  sm2.put(w2)  # FD=STD_extended 00=inputs
  sm2.active(True)
  print("(%08x, %08x) Activated sm2. Deactivating." % (w1, w2))
  sm2.active(False)

Dir.value(1)
Slenb.value(0)
Halt.value(0)
pio0.remove_program(ldd_immediate_std_extended_prog)
print("DONE step3")
while True:
    Halt = Pin(13, Pin.OUT)
    Halt.value(0)
