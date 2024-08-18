import FIFOF::*;
import GetPut::*;
import ClientServer::*;
import Vector::*;
import BUtils::*;
import CharUtils::*;
import TimekeepersLockGlobals::*;

typedef union tagged {
	void Init;
	Vector#(4, Byte) Time;
	Vector#(6, Byte) Date;
	void Finish;
} NmeaInfo deriving (Eq, Bits, FShow);

typedef enum {
	Idle,
	ExpectG,
	ExpectPorN,
	ExpectR,
	ExpectM,
	ExpectC,
	CommaBeforeTime,
	ReadTime,
	CommaBeforeStatus,
	ExpectStatusA,
	Skip7Commas,
	ReadDate,
	AsteriskBeforeCksum,
	Cksum1,
	Cksum2
} State deriving (Eq, Bits, FShow);

module mkNmeaReader (Server#(Byte, NmeaInfo));
	FIFOF#(NmeaInfo) out <- mkFIFOF;
	Reg#(State) state <- mkReg(Idle);
	Reg#(LBit#(6)) counter <- mkRegU;
	Reg#(Vector#(6, Byte)) scratch <- mkRegU;
	Reg#(Byte) cksum <- mkRegU;

	interface Put request;
		method Action put(Byte c);
			Byte lc = lowercase(c);
			Byte cksum_new = cksum ^ c;
			if (c == ord("$")) begin
				cksum_new = 0;
				out.enq(tagged Init);
				state <= ExpectG;
			end else if (state == ExpectG)
				state <= lc == ord("g") ? ExpectPorN : Idle;
			else if (state == ExpectPorN)
				state <= lc == ord("p") || lc == ord("n") ? ExpectR : Idle;
			else if (state == ExpectR)
				state <= lc == ord("r") ? ExpectM : Idle;
			else if (state == ExpectM)
				state <= lc == ord("m") ? ExpectC : Idle;
			else if (state == ExpectC)
				state <= lc == ord("c") ? CommaBeforeTime : Idle;
			else if (state == CommaBeforeTime) begin
				state <= c == ord(",") ? ReadTime : Idle;
				counter <= 4 - 1;
			end else if (state == ReadTime) begin
				scratch <= shiftInAtN(scratch, c);
				if (counter == 0)
					state <= CommaBeforeStatus;
				counter <= counter - 1;
			end else if (state == CommaBeforeStatus && c == ord(",")) begin
				out.enq(tagged Time drop(scratch));
				state <= ExpectStatusA;
			end else if (state == ExpectStatusA) begin
				if (lc == ord("a")) begin
					state <= Skip7Commas;
					counter <= 7 - 1;
				end else state <= Idle;
			end else if (state == Skip7Commas && c == ord(",")) begin
				if (counter == 0) begin
					state <= ReadDate;
					counter <= 6 - 1;
				end else counter <= counter - 1;
			end else if (state == ReadDate) begin
				scratch <= shiftInAtN(scratch, c);
				if (counter == 0)
					state <= AsteriskBeforeCksum;
				counter <= counter - 1;
			end else if (state == AsteriskBeforeCksum && c == ord("*")) begin
				cksum_new = cksum;  // preserve cksum
				out.enq(tagged Date drop(scratch));
				state <= Cksum1;
			end else if (state == Cksum1) begin
				cksum_new = cksum;  // preserve cksum
				state <= cksum[7:4] == conv_dig(c) ? Cksum2 : Idle;
			end else if (state == Cksum2) begin
				if (cksum[3:0] == conv_dig(c))
					out.enq(tagged Finish);
				state <= Idle;
			end
			cksum <= cksum_new;
			$display("NmeaReader { state: ",fshow(state),", counter: ",counter,", cksum: ",fshow(cksum)," }");
		endmethod
	endinterface

	interface response = toGet(out);
endmodule