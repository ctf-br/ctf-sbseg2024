// parameters

typedef 29491200 ClockFreq;
typedef 115200 BaudRate;

// base types

typedef Bit#(8) Byte;

// derived types

typedef TDiv#(ClockFreq, BaudRate) BaudCycles;