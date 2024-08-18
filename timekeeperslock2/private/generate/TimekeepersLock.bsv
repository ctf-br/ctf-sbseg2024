import GetPut::*;
import Connectable::*;
import ClientServer::*;
import UART::*;
import NmeaReader::*;
import HashProvider::*;
import KeypadBuffer::*;

interface TimekeepersLock;
	(* always_ready *)
	method Bool open_lock;
	interface UartRxWires gps_uart;
	interface UartRxWires keypad_uart;
endinterface

(* synthesize *)
module mkTimekeepersLock(TimekeepersLock);
	let gps <- mkUartRx;
	let keypad <- mkUartRx;
	let nmea <- mkNmeaReader;
	let prov <- mkHashProvider;
	let kbuf <- mkKeypadBuffer;

	Reg#(Bool) hash_is_correct <- mkReg(False);

	mkConnection(gps.rx, nmea.request);
	mkConnection(nmea.response, prov.info);

	mkConnection(keypad.rx, kbuf.uart);

	rule check_hash (prov.hash matches tagged Valid .h);
		hash_is_correct <= h == kbuf.hash;
	endrule

	method Bool open_lock = hash_is_correct;

	interface gps_uart = gps.wires;
	interface keypad_uart = keypad.wires;
endmodule