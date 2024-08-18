/* The Keccak sponge function, translated from the designer's
 * VHDL code to BSV by Paulo Matias.
 *
 * Please refer to http://keccak.noekeon.org/
 * for information about Keccak.
 *
 * To the extent possible under law, the implementer has waived
 * all copyright and related or neighboring rights to the source
 * code in this file.
 * http://creativecommons.org/publicdomain/zero/1.0/
 */

import StmtFSM::*;
import FIFOF::*;
import BUtils::*;
import Keccak::*;
import KeccakGlobals::*;

(* synthesize *)
module mkKeccakTb(Empty);
	FIFOF#(LineContents) infifo <- mkSizedFIFOF(256);
	Reg#(LBit#(Rate)) counter <- mkReg(0);
	Reg#(Bool) entryEnd <- mkReg(False);

	let reader <- mkLineReader;
	let keccak <- mkKeccak;

	function squeeze = action
		let x <- keccak.squeeze;
		$display("%h", x);
	endaction;
	function squeeze4 = seq
		squeeze; squeeze; squeeze; squeeze;
	endseq;

	function discardLine = seq
		reader.start; action let x = reader.result; endaction
	endseq;

	mkAutoFSM(seq
		keccak.init; discardLine;

		while (True) seq
			while (True) seq
				reader.start;
				infifo.enq(reader.result);
				if (!isValid(reader.result))
					break;
			endseq

			action
				counter <= fromInteger(rate);
				entryEnd <= False;
				keccak.init;
			endaction

			while (!entryEnd)
				action
					if (counter != 0) begin
						case (infifo.first) matches
							tagged Valid .n: keccak.absorb(n);
							tagged Invalid: action
								$display("ERROR: input size must be multiple of the rate (%d bit)", rate*n);
								$finish(1);
							endaction
						endcase
						counter <= counter - 1;
						infifo.deq;
					end else begin
						keccak.go;
						counter <= fromInteger(rate);
						entryEnd <= !isValid(infifo.first);
					end
				endaction

			squeeze4;
			$display("-");
			infifo.deq;
		endseq
	endseq);
endmodule

typedef Maybe#(Bit#(N)) LineContents;

interface LineReader;
	method Action start;
	method LineContents result;
endinterface

module mkLineReader(LineReader);
	function ord(s) = fromInteger(charToInteger(stringHead(s)));
	function conv_dig(c) = pack(
		(c >= ord("0") && c <= ord("9")) ? (c - ord("0")) :
		(c >= ord("A") && c <= ord("F")) ? (c - ord("A") + 10) :
		(c >= ord("a") && c <= ord("f")) ? (c - ord("a") + 10) :
		(?))[3:0];

	Reg#(LineContents) res <- mkRegU;
	Reg#(Int#(32)) c <- mkRegU;

	FSM fsm <- mkFSM(seq
		while (True) seq
			action
				let cin <- $fgetc(stdin);
				if (cin == -1) begin
					$display("Unexpected EOF");
					$finish(1);
				end
				c <= cin;
			endaction
			if (c == ord("\n"))
				break;
			action
				case (c)
					13, ord("\t"), ord(" "), ord("_"): noAction;
					ord("-"): res <= tagged Invalid;
					ord("."): $finish();
					default:  res <= tagged Valid (
						(fromMaybe(0, res) << 4) | extend(conv_dig(c)));
				endcase
			endaction
		endseq
	endseq);
	method start = fsm.start;
	method result if (fsm.done) = res;
endmodule