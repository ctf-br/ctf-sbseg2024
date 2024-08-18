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

import Vector::*;
import KeccakGlobals::*;

typedef struct {
	KRow theta_parity;
	SubState iota;
	SubState theta;
} Out;

function Out chi_iota_theta(
			SubState chi_in,
			SubState theta_inp,
			KSlice k_slice_theta_p_in,
			KRow theta_parity_inp,
			Bool first_round,
			Bool first_block,
			SubLane round_constant_signal,
			Bit#(1) theta_parity_bit_iota_inp
		);

	// chi
	function a chi_f(a in) provisos (PrimUpdateable#(a,ae), PrimUpdateable#(ae,aee), Bitwise#(aee));
		a out = ?;
		for (Integer y = 0; y < np; y = y + 1)
			for (Integer x = 0; x < ns; x = x + 1)
				out[y][x] = in[y][x] ^ (~in[y][(x+1)%ns] & in[y][(x+2)%ns]);
		return out;
	endfunction
	SubState chi_out = chi_f(chi_in);
	KSlice chi_out_for_theta_p = chi_f(k_slice_theta_p_in);

	// iota
	SubState iota_in = chi_out;
	SubState iota_out = iota_in;
	iota_out[0][0] = iota_in[0][0] ^ round_constant_signal;

	// theta
	SubState theta_in = first_round ? theta_inp : iota_out;
	function fsel(pos,vec) = vec[pos];
	function bxor(a,b) = a^b;
	function b col_xor(Vector#(np,a) in) provisos (PrimUpdateable#(a,ae), Literal#(ae), Bitwise#(ae), PrimUpdateable#(b, ae));
		// computes {in[0][0]^...^in[np-1][0], ..., in[0][ns-1]^...^in[np-1][ns-1]}
		// (the xor of all rows in each column)
		b out = ?;
		for (Integer x = 0; x < ns; x = x + 1)
			out[x] = foldr(bxor, 0, map(fsel(x), in));
		return out;
	endfunction
	SubPlane sum_sheet = col_xor(theta_in);
	KRow theta_parity_first_round = col_xor(k_slice_theta_p_in);
	KRow theta_parity_after_chi = col_xor(chi_out_for_theta_p);
	theta_parity_after_chi[0] = theta_parity_after_chi[0] ^ theta_parity_bit_iota_inp;
	KRow theta_parity_out = pack(map(fsel(bitPerSubLane-1), sum_sheet));
	KRow theta_parity =
			(first_round && first_block) ? theta_parity_first_round :
			first_block ? theta_parity_after_chi :
			theta_parity_inp;
	SubState theta_out = ?;
	for (Integer y = 0; y < np; y = y + 1) begin
		for (Integer x = 0; x < ns; x = x + 1) begin
			theta_out[y][x][0] = theta_in[y][x][0] ^ sum_sheet[(ns+x-1)%ns][0] ^ theta_parity[(x+1)%ns];
			for (Integer i = 1; i < bitPerSubLane; i = i + 1)
				theta_out[y][x][i] = theta_in[y][x][i] ^ sum_sheet[(ns+x-1)%ns][i] ^ sum_sheet[(x+1)%ns][i-1];
		end
	end

	return Out {
			theta_parity: theta_parity_out,
			iota: iota_out,
			theta: theta_out
	};
endfunction