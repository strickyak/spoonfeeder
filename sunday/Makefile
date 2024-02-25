all: pico-reader.decb pico-reader.raw pico-reader.lemma

pico-reader.s: pico-reader.c
	$(HOME)/coco-shelf/bin/gcc6809 -S -Os -std=gnu99 $<
pico-reader.o: pico-reader.s
	$(HOME)/coco-shelf/bin/lwasm --format=obj -o'$@' $<

prefix.o: prefix.asm
	$(HOME)/coco-shelf/bin/lwasm --format=obj -o'$@' $<

pico-reader.decb: prefix.o pico-reader.o
	$(HOME)/coco-shelf/bin/lwlink --decb --script=orgC000.script --entry=_start --output=$@ $^
pico-reader.raw: prefix.o pico-reader.o
	$(HOME)/coco-shelf/bin/lwlink --raw  --script=orgC000.script --entry=_start --output=$@ $^

pico-reader.lemma: pico-reader.decb
	$(HOME)/coco-shelf/build-frobio/decb-triples < $< > $<.triples
	cat "$(HOME)/coco-shelf/build-frobio/burn" "$<.triples" > $@
