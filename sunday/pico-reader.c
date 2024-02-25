/*
	For coco2 cartridge rom at $C000.
	Assumes the Text Screen was initialized at $0400.

	Clears the screen (at $0400) with dots.

	Writes a '+' to 0xFF7A, once.

	After a short delay, reads 511 bytes from 0xFF7B
	and writes them to 511 chars on the screen.

	Then 
*/

// FOR M6809
typedef unsigned char byte;
typedef unsigned int word;

#define delay() { for (word i=0; i<20000; i++) { scrn[511] += *readme; } }

void main() {
  volatile byte* ctrl = (byte*)0xFF7A;
  volatile byte* data = (byte*)0xFF7B;
  volatile byte* scrn = (byte*)0x0400; // start of screen
  volatile byte* readme = (byte*)0x8000;  // in ROM

  for (word i=0; i < 511; i++) { scrn[i] = '.'; }  // Clear with dots.

  while (1) {
    *ctrl = '+';
    delay();
    for (word i=0; i < 511; i++) {
      byte b = *data;
      if (96 <= b && b < 128) b -= 96;  // MAGUSCULE
      scrn[i] = b;
    }

    while(1) {scrn[511]++;}  // Spin last char.
  }
}
