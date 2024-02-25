all: pico-reader.python

pico-reader.s: pico-reader.c
	$(HOME)/coco-shelf/bin/gcc6809 -S -Os -std=gnu99 $<
pico-reader.o: pico-reader.s
	$(HOME)/coco-shelf/bin/lwasm --format=obj -o'$@' $<

prefix.o: prefix.asm
	$(HOME)/coco-shelf/bin/lwasm --format=obj -o'$@' $<

pico-reader.decb: prefix.o pico-reader.o
	$(HOME)/coco-shelf/bin/lwlink -obj --script=orgC000.script --entry=_main --output=$@ $^
