all: io_ff78.python life-semi.python step5.py copico5.py

io_ff78.s: io_ff78.c
	$(HOME)/coco-shelf/bin/gcc6809 -S -Os -std=gnu99 $<
io_ff78.o: io_ff78.s
	$(HOME)/coco-shelf/bin/lwasm --format=obj -o'$@' $<
io_ff78.decb: io_ff78.o
	$(HOME)/coco-shelf/bin/lwlink -obj --section-base=.text=0x0120 --entry=_main --output=$@ $<
io_ff78.python: io_ff78.decb decb_to_word_pairs
	./decb_to_word_pairs < $< > $@

life-semi.s: life-semi.c
	$(HOME)/coco-shelf/bin/gcc6809 -S -O2 -std=gnu99 $<
life-semi.o: life-semi.s
	$(HOME)/coco-shelf/bin/lwasm --format=obj -o'$@' $<
life-semi.decb: life-semi.o
	$(HOME)/coco-shelf/bin/lwlink -obj --script=text0200.script --entry=_main --output=$@ $< --map=life-semi.map
life-semi.python: life-semi.decb decb_to_word_pairs
	./decb_to_word_pairs < $< > $@

hello5.s: hello5.c
	$(HOME)/coco-shelf/bin/gcc6809 -S -Os -std=gnu99 $<
hello5.o: hello5.s
	$(HOME)/coco-shelf/bin/lwasm --format=obj -o'$@' $<
hello5.decb: hello5.o
	$(HOME)/coco-shelf/bin/lwlink -obj --script=text0200.script --entry=_main --output=$@ $< --map=hello5.map
hello5.python: hello5.decb decb_to_word_pairs
	./decb_to_word_pairs < $< > $@

step5.py: life-semi.python carrier-py
	cat $^ > $@

copico5.py: life-semi.python carrier-copico-py
	cat $^ > $@
