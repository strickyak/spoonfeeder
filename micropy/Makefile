all: io_ff78.python

io_ff78.s: io_ff78.c
	$(HOME)/coco-shelf/bin/gcc6809 -S -Os $<
io_ff78.o: io_ff78.s
	$(HOME)/coco-shelf/bin/lwasm --format=obj -o'$@' $<
io_ff78.decb: io_ff78.o
	$(HOME)/coco-shelf/bin/lwlink -obj --section-base=.text.startup=0x0180 --entry=_main --output=$@ $<
io_ff78.python: io_ff78.decb decb_to_word_pairs
	./decb_to_word_pairs < $< > $@
