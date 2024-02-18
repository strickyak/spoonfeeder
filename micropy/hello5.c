typedef unsigned char byte;
typedef unsigned int word;

int main() {
	volatile char* p = (void*) 0x0000;

	for (word i = 0; i < 512; i++) {
		p[i] = '/';
	}

	for (char i = 0; i < 5; i++) {
		p[i+32] = "HELLO"[i];
	}
	while (1) {}
#if 0	
	for (char* s = "HELLO"; *s; s++) {
		*p++ = *s;
	}
#endif
}
