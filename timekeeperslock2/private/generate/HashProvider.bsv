import GetPut::*;
import Connectable::*;
import GetPut::*;
import ClientServer::*;
import Vector::*;
import BUtils::*;
import Keccak::*;
import NmeaReader::*;

interface HashProvider;
	interface Put#(NmeaInfo) info;
	method Maybe#(Hash) hash;
endinterface

typedef Bit#(256) Hash;
typedef Bit#(64) KeccakWord;
typedef Bit#(4) WordIndex;

typedef enum {
	Idle,
	AbsorbSecretKey,
	StartPermutation,
	SqueezeHash
} State deriving (Eq, Bits, FShow);

module mkHashProvider (HashProvider);
	let keccak <- mkKeccak;
	Reg#(Bool) hashValid <- mkReg(False);
	Reg#(Vector#(4, KeccakWord)) hashReg <- mkRegU;
	Reg#(WordIndex) counter <- mkRegU;
	Reg#(State) state <- mkReg(Idle);

	rule absorbSecretKey (state == AbsorbSecretKey);
		keccak.absorb(secretKey(counter));
		if (counter == 14)
			state <= StartPermutation;
		counter <= counter + 1;
	endrule

	rule startPermutation (state == StartPermutation);
		keccak.go;
		state <= SqueezeHash;
		counter <= 0;
	endrule

	rule squeezeHash (state == SqueezeHash);
		let hashPart <- keccak.squeeze;
		let hashRegNew = shiftInAt0(hashReg, reverse_bytes(hashPart));
		hashReg <= hashRegNew;
		let done = counter == 3;
		hashValid <= done;
		state <= done ? Idle : SqueezeHash;
		if (done)
			$display("HashProvider { hash: ",fshow(pack(hashRegNew))," }");
		counter <= counter + 1;
	endrule

	interface Put info;
		method Action put(NmeaInfo info) if (state == Idle);
			$display("NmeaInfo: ", fshow(info));
			function keccakInput(vec) = pack(append(vec, replicate('h20)));
			case (info) matches
				tagged Init: keccak.init;
				tagged Time .v: keccak.absorb(keccakInput(v));
				tagged Date .v: keccak.absorb(keccakInput(v));
				tagged Finish: action counter <= 0; state <= AbsorbSecretKey; endaction
			endcase
		endmethod
	endinterface

	method hash = hashValid ? tagged Valid pack(hashReg) : tagged Invalid;
endmodule

function KeccakWord secretKey(WordIndex n) =
	case (n)
		0:  'ha7c68cac16935e00;
		1:  'h1d7e03d2a6d3884c;
		2:  'h2a9de313a564a05d;
		3:  'hd61d662ba24231be;
		4:  'h0000000000000006;
		5:  'h0000000000000000;
		6:  'h0000000000000000;
		7:  'h0000000000000000;
		8:  'h0000000000000000;
		9:  'h0000000000000000;
		10: 'h0000000000000000;
		11: 'h0000000000000000;
		12: 'h0000000000000000;
		13: 'h0000000000000000;
		14: 'h8000000000000000;
		default: ?;
	endcase;
