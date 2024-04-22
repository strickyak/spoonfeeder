; # Protocol1 for Copico
; 
; strick 2024-04-21
; 
; ## Command Byte 1: Program Request
; 
; Coco will read the Data Port 1024 times,
; and will save the bytes at $2000-$23FF,
; and will then jump to $2000.
; 
; ## Command Byte 2: Upload Web Request
; 
; Coco will write the Data Port 64 times.
; (The contents of that request may be the
; path portion of URL, zero-padded.)
; 
; ## Command Byte 3: Download Web Response
; 
; Coco will read the Data Port 1024 times.
; The first 1024 bytes returned for the
; peviously uploaded URL will be read back.
; 
; ## Boot Program
; 
; This program would suffice to use Program Request
; to load the program and execute it:

ControlPort EQU $FF7A
DataPort    EQU $FF7B

Start:
        lda #1         ; "Program Request" Code
        sta ControlPort  ; Send the command.

        ldx #$2000     ; RAM destination
        ldy #1024      ; how many times to load a byte
        ldb DataPort   ; load the byte
Loop:   stb ,x+        ; save it to RAM
        leay -1,y      ; decrement counter
        bne Loop

        jmp $2000      ; execute what got loaded.
Finish:

; HINT: lwasm -r proto1.asm --list=proto1.list
