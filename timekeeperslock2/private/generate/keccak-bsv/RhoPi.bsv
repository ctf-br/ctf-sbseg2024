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

import KeccakGlobals::*;

function KState pi(KState in);
	KState out = ?;
	for (Integer y = 0; y < np; y = y + 1)
		for (Integer x = 0; x < ns; x = x + 1)
			for (Integer i = 0; i < n; i = i + 1)
				out[(2*x+3*y)%np][(0*x+1*y)%ns][i] = in[y][x][i];
	return out;
endfunction

function KState rho(KState in);
	Integer rho_disp[np][ns] = {
		/*[0][]*/ { 0,  1, 62, 28, 27},
		/*[1][]*/ {36, 44,  6, 55, 20},
		/*[2][]*/ { 3, 10, 43, 25, 39},
		/*[3][]*/ {41, 45, 15, 21,  8},
		/*[4][]*/ {18,  2, 61, 56, 14}
	};

	KState out = ?;
	for (Integer y = 0; y < np; y = y + 1)
		for (Integer x = 0; x < ns; x = x + 1)
			for(Integer i = 0; i < n; i = i + 1)
				out[y][x][i] = in[y][x][(n+i-rho_disp[y][x])%n];
	return out;
endfunction

function KState rho_pi(KState in) = pi(rho(in));