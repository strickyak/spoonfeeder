// FOR M6809 -- life for Coco Semigraphics (VDG Text mode)
//
//   Runs in the first 4K of RAM (all under $1000).
typedef unsigned char byte;
typedef unsigned int word;

#define N 1024
#define W 64
#define H 16

#if unix
#include <stdio.h>
byte A[N];
byte B[N];
byte S[W*H/4];
#else
#define A ((volatile byte*)0x0800)
#define B ((volatile byte*)0x0C00)
#define S ((volatile byte*)0x0000)
#endif

#define AA(X,Y) A[(X&(W-1)) + W*(Y&(H-1))]
#define BB(X,Y) B[(X&(W-1)) + W*(Y&(H-1))]

#define STOP() { while (1) { ++(S[0]); } }

void Qmemset(volatile byte* p, byte c, word n) {
	while (n--) *p++ = c;
}
void Qmemcpy(volatile byte* d, byte* s, word n) {
	while (n--) *d++ = *s++;
}

void show(byte* p) {
#if unix
	static gen;
	for (word y=0; y<H; y++) {
		for (word x=0; x<W; x++) {
			putchar(p[x + y*W] ? '#' : '.');
		}
		putchar('\n');
	}
	printf("---------------------------------- %d\n", ++gen);
#endif
}

void render() {
	for (word y=0; y<H; y+=2) {
		for (word x=0; x<W; x+=2) {
			byte z = 128;
			if (BB(x+0, y+0)) z |= 8;
			if (BB(x+1, y+0)) z |= 4;
			if (BB(x+0, y+1)) z |= 2;
			if (BB(x+1, y+1)) z |= 1;
			S[(y*(W/4)) + (x>>1)] = z;
		}
	}
}

void generation() {
	for (word x=0; x<W; x++) {
		for (word y=0; y<H; y++) {
			byte count = 0;
			for (byte i=0; i<3; i++) {
				for (byte j=0; j<3; j++) {
					count += AA(x+i, y+j);
				}
			}
			if (AA(x+1, y+1)) {
				BB(x+1, y+1) = (count==3 || count==4);
			} else {
				BB(x+1, y+1) = (count==3);
			}
		}
	}
}

#if unix
  #define WRAPPER main
#else
  #define WRAPPER wrapper
#endif

void WRAPPER() {
#ifndef unix
  asm volatile(
  	"  .globl _main\n_main: ldd #$07F0 \n  tfr d,s \n  tfr d,u"
	);

#endif
  {
  //STOP();
	  Qmemset(S, '.', 512);
	  Qmemset(A, 0, N);

	  for (word i=221; i<N-100; i+=7) A[i]=1;
	  for (word i=2*N/6; i<5*N/6; i+=9) A[i]=1;
	  for (word i=5; i<N; i+=13) A[i]=1;
	  for (word i=N/4; i<N/2; i+=17) A[i]=1;
	  show(A);

	  while (1) {
		generation();
		render();
  // STOP();
		show(B);
		Qmemcpy(A, B, N);
	  }
  }
}
