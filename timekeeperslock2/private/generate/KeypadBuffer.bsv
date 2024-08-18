import GetPut::*;
import TimekeepersLockGlobals::*;
import HashProvider::*;
import CharUtils::*;

interface KeypadBuffer;
	interface Put#(Byte) uart;
	method Hash hash;
endinterface

module mkKeypadBuffer (KeypadBuffer);
	Reg#(Hash) bufReg <- mkRegU;

	interface Put uart;
		method Action put(Byte c);
			bufReg <= (bufReg << 4) | extend(conv_dig(c));
		endmethod
	endinterface

	method hash = bufReg;
endmodule