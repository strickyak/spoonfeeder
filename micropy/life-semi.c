// FOR M6809 -- life for Coco Semigraphics (VDG Text mode)
typedef unsigned char byte;
typedef unsigned int word;

#define N 2048
#define W 64
#define H 32

#if unix
#include <stdio.h>
byte A[N];
byte B[N];
byte S[W*H/4];
#else
#define A ((byte*)0x0800)
#define B ((byte*)0x1000)
#define S ((byte*)0x0000)
#endif

#define AA(X,Y) A[(X&(W-1)) + W*(Y&(H-1))]
#define BB(X,Y) B[(X&(W-1)) + W*(Y&(H-1))]

void Qmemset(byte* p, byte c, word n) {
	while (n--) *p++ = c;
}
void Qmemcpy(byte* d, byte* s, word n) {
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
			S[y*(H/2) + (x>>1)] = z;
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
  	"  .globl _main\n_main: ldd #4000 \n  tfr d,s \n  tfr d,u"
	);

#endif
  {
	  Qmemset(S, 128, 512);
	  Qmemset(A, 0, N);

	  for (word i=800; i<1200; i+=7) A[i]=1;
	  for (word i=400; i<1500; i+=9) A[i]=1;
	  for (word i=5; i<N; i+=13) A[i]=1;
	  for (word i=1000; i<N-200; i+=17) A[i]=1;
	  show(A);

	  while (1) {
		generation();
		render();
		show(B);
		Qmemcpy(A, B, N);
	  }
  }
}
