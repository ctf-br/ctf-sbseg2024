import StmtFSM::*;
import GetPut::*;
import Connectable::*;
import List::*;
import Assert::*;
import TimekeepersLock::*;
import TimekeepersLockGlobals::*;
import UART::*;

(* synthesize *)
module mkTimekeepersLockTb (Empty);
	let tklock <- mkTimekeepersLock;
	let gps <- mkUartTx;
	let keypad <- mkUartTx;

	Reg#(Bit#(32)) i <- mkReg(0);
	Reg#(Bit#(32)) j <- mkReg(0);

	mkConnection(gps.wires, tklock.gps_uart);
	mkConnection(keypad.wires, tklock.keypad_uart);

	mkAutoFSM(seq
		dynamicAssert(!tklock.open_lock, "FAIL: door should be locked");

		par
			sendStr(i, gps, "$GPRMC,092750.000,A,5321.6802,N,00630.3372,W,0.02,31.66,280511,,,A*43");
			sendStr(j, keypad, "3a675b7ca023704056328e45dbf3e579652cdd9a45e39a51ce5a2c1041d143");
		endpar
		delay(3360);
		dynamicAssert(!tklock.open_lock, "FAIL: door should be locked");

		sendStr(j, keypad, "7e");
		delay(2560);
		dynamicAssert(tklock.open_lock, "FAIL: door should be unlocked");

		sendStr(j, keypad, "\n");
		delay(2560);
		dynamicAssert(!tklock.open_lock, "FAIL: door should be locked");

		$display("OK");
	endseq);
endmodule

function Stmt sendStr(Reg#(Bit#(32)) i, UartTx u, String s);
	List#(Byte) bytelist = map(fromInteger, map(charToInteger, stringToCharList(s)));
	return seq
		i <= 0;
		while (i < fromInteger(stringLength(s))) action
			u.tx.put(bytelist[i]);
			i <= i + 1;
		endaction
	endseq;
endfunction
