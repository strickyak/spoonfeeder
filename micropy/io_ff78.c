// FOR M6809
typedef unsigned char byte;
typedef unsigned int word;

#if 0
int delay() {
  volatile byte* readme = (byte*)0x8000;  // in ROM
  word x = 0;
  for (word i=0; i<60000; i++) {
    x += *readme;
  }
  return x;
}
#endif

#define delay() { for (word i=0; i<20000; i++) { x += *readme; } }

void main2() {
  asm volatile(
  	"  .globl _main\n_main: ldd #4000 \n  tfr d,s \n  tfr d,u"
	);

  {
  volatile byte* ctrl = (byte*)0xFF7A;
  volatile byte* data = (byte*)0xFF7B;
  volatile byte* scrn = (byte*)0x0000; // start of screen
  volatile byte* readme = (byte*)0x8000;  // in ROM
  // word x = 0;

  while (1) {
    *ctrl = '+';
    // delay();
    for (word b=0; b < 255; b++) {
      scrn[b] = *data;

      scrn[255]++;  // Spin right hand char, mid-screen.
    }
    // delay();
    // scrn[256]++;  // Spin left hand char, mid-screen.
    // scrn[257] = x;

    while(1) {}
  }
  }
}
