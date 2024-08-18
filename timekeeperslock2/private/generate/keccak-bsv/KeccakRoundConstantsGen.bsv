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

import BUtils::*;
import KeccakGlobals::*;

function Bit#(N) keccakRoundConstant(LBit#(NumRound) round_number) =
	case (round_number)
		'b00000: 'h0000000000000000;
		'b00001: 'h0000000000000001;
		'b00010: 'h0000000000008082;
		'b00011: 'h800000000000808A;
		'b00100: 'h8000000080008000;
		'b00101: 'h000000000000808B;
		'b00110: 'h0000000080000001;
		'b00111: 'h8000000080008081;
		'b01000: 'h8000000000008009;
		'b01001: 'h000000000000008A;
		'b01010: 'h0000000000000088;
		'b01011: 'h0000000080008009;
		'b01100: 'h000000008000000A;
		'b01101: 'h000000008000808B;
		'b01110: 'h800000000000008B;
		'b01111: 'h8000000000008089;
		'b10000: 'h8000000000008003;
		'b10001: 'h8000000000008002;
		'b10010: 'h8000000000000080;
		'b10011: 'h000000000000800A;
		'b10100: 'h800000008000000A;
		'b10101: 'h8000000080008081;
		'b10110: 'h8000000000008080;
		'b10111: 'h0000000080000001;
		'b11000: 'h8000000080008008;
		default: 0;
	endcase;
