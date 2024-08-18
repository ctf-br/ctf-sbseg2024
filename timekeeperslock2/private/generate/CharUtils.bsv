import TimekeepersLockGlobals::*;

function Byte ord(String s) = fromInteger(charToInteger(stringHead(s)));

function Byte lowercase(Byte c) = c | 'h20;

function Bit#(4) conv_dig(Byte c) =
		pack(
			(c  >= ord("0") && c  <= ord("9"))
					? (c  - ord("0"))
					: (lowercase(c) - ord("a") + 10)
		)[3:0];