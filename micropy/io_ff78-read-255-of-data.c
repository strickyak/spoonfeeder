// FOR M6809
typedef unsigned char byte;
typedef unsigned int word;

#define delay() { for (word i=0; i<20000; i++) { x += *readme; } }

void main2() {
  asm volatile(
  	"  .globl _main\n_main: ldd #0FF0 \n  tfr d,s \n  tfr d,u"
	);

  {
  volatile byte* ctrl = (byte*)0xFF7A;
  volatile byte* data = (byte*)0xFF7B;
  volatile byte* scrn = (byte*)0x0000; // start of screen
  volatile byte* readme = (byte*)0x8000;  // in ROM

  while (1) {
    *ctrl = '+';
    // delay();
    for (word b=0; b < 511; b++) {
      scrn[b] = *data;
    }

    while(1) {scrn[511]++;}
  }
  }
}
