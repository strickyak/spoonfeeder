// FOR M6809
typedef unsigned char byte;
typedef unsigned int word;

int main() {
  volatile byte* p = (byte*)0xFF78; // first of 4 io ports to probe
  volatile byte* x = (byte*)0x0110; // "OUR " in step2.py
  volatile byte* y = (byte*)0x0100; // mid-screen

  while (1) {
    // write all four ports (with bytes from "OUR ")
    // p[0] = x[0];
    // p[1] = x[1];
    p[2] = x[2];
    p[3] = x[3];

    // read all four ports (and save at mid-screen
    // y[0] = p[0];
    // y[1] = p[1];
    y[2] = p[2];
    y[3] = p[3];

    y[31]++;  // Spin right hand char, mid-screen.
  }
}
