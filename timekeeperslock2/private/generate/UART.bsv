import BUtils::*;
import GetPut::*;
import Connectable::*;
import TimekeepersLockGlobals::*;

interface UartRx;
	interface Get#(Byte) rx;
	interface UartRxWires wires;
endinterface

interface UartTx;
	interface Put#(Byte) tx;
	interface UartTxWires wires;
endinterface


interface UartRxWires;
	(* always_ready, always_enabled, prefix="" *)
	method Action put((*port="rx"*)Bit#(1) b);
endinterface

interface UartTxWires;
	(* always_ready, result="tx" *)
	method Bit#(1) get;
endinterface


typedef Bit#(TLog#(BaudCycles)) Phase;
Integer baudCycles = valueOf(BaudCycles);
Phase midPhase = fromInteger(baudCycles / 2);
Phase maxPhase = fromInteger(baudCycles - 1);


module mkUartRx(UartRx);
	Wire#(Bit#(1)) inb <- mkBypassWire;
	Reg#(Bit#(10)) shiftReg <- mkReg(0);  // {stop_bit, data, start_bit}
	let idle = shiftReg[0] == 0;   // the UartRx is idle when the start bit (0) is in place
	Array#(Reg#(Bool)) pending <- mkCRegU(2);
	Reg#(Phase) phase <- mkRegU;

	(* no_implicit_conditions, fire_when_enabled, preempts="detectStartBit, incPhase" *)
	rule detectStartBit (idle && inb == 0);
		shiftReg <= 'b1_1111_1111_1;  // idle becomes False
		pending[1] <= True;
		phase <= midPhase + 1;
	endrule

	(* no_implicit_conditions *)
	rule incPhase;
		phase <= phase == maxPhase ? 0 : phase + 1;
	endrule

	(* no_implicit_conditions, fire_when_enabled *)
	rule sampleBit (!idle && phase == 0);
		shiftReg <= {inb, shiftReg[9:1]};
	endrule

	interface Get rx;
		method ActionValue#(Byte) get if (idle && pending[0]);
			pending[0] <= False;
			return shiftReg[8:1];
		endmethod
	endinterface

	interface UartRxWires wires;
		method Action put(Bit#(1) b);
			inb <= b;
		endmethod
	endinterface
endmodule


module mkUartTx(UartTx);
	Reg#(Bit#(1)) outb <- mkReg(1);
	Reg#(Bit#(10)) shiftReg <- mkReg(0); // {stop_bit, data, start_bit}
	Reg#(Phase) phase <- mkReg(0);
	let idle = shiftReg == 0 && phase == 0;

	(* no_implicit_conditions, fire_when_enabled *)
	rule produceOut (!idle);
		phase <= phase == maxPhase ? 0 : phase + 1;
		if (phase == 0) begin
			outb <= shiftReg[0];
			shiftReg <= shiftReg >> 1;
		end
	endrule

	(* no_implicit_conditions, fire_when_enabled *)
	rule clearOut (idle);
		outb <= 1;
	endrule

	interface Put tx;
		method Action put(Byte b) if (idle);
			shiftReg <= {1'b1, b, 1'b0};
			phase <= 0;
		endmethod
	endinterface

	interface UartTxWires wires;
		method get = outb;
	endinterface
endmodule


instance Connectable#(UartTxWires, UartRxWires);
	module mkConnection#(UartTxWires tx, UartRxWires rx)(Empty);
		mkConnection(tx.get, rx.put);
	endmodule
endinstance

instance Connectable#(UartRxWires, UartTxWires);
	module mkConnection#(UartRxWires rx, UartTxWires tx)(Empty);
		mkConnection(rx.put, tx.get);
	endmodule
endinstance