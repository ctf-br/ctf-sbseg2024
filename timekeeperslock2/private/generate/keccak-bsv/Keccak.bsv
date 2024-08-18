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
import BUtils::*;
import ConfigReg::*;
import KeccakGlobals::*;
import RhoPi::*;
import ChiIotaTheta::*;
import KeccakRoundConstantsGen::*;

interface Keccak;
	(* always_ready *)
	method Action init; // reset the core
	method Action go;   // compute the permutation
	method Action absorb(Bit#(N) din);
	method ActionValue#(Bit#(N)) squeeze;
endinterface

module mkKeccak (Keccak);
	KState zero_state = replicate(replicate(0));

	Reg#(KState) reg_data <- mkReg(zero_state);
	Reg#(LBit#(NumRound))  counter_nr_rounds <- mkReg(0);
	Reg#(LBit#(NumSlices)) counter_block <- mkReg(0);
	Reg#(Bool) permutation_computed <- mkReg(True);
	Reg#(Bool) first_block <- mkReg(False);
	Reg#(Bool) first_round <- mkReg(False);
	Reg#(KRow) theta_parity_reg <- mkConfigReg(0);

	Wire#(Bool) init_wire <- mkDWire(False);
	Wire#(Bool) go_wire <- mkDWire(False);
	Wire#(Bool) absorb_wire <- mkDWire(False);
	Wire#(Bit#(N)) absorb_dwire <- mkDWire(0);
	Wire#(Bool) squeeze_wire <- mkDWire(False);

	let rho_pi_out = rho_pi(reg_data);

	let round_constant_signal = keccakRoundConstant(counter_nr_rounds);
	Vector#(NumSlices, SubLane) round_constant_vec = unpack(round_constant_signal);
	let round_constant_signal_sub = round_constant_vec[counter_block];

	function k_to_sub_state(s) = map(map(truncate), s);
	let chi_inp = k_to_sub_state(reg_data);
	let theta_inp = k_to_sub_state(reg_data);

	function fsel(pos,vec) = vec[pos];
	let k_slice_theta_p_in = map(compose(pack, map(fsel(n-1))), reg_data);

	let cit = chi_iota_theta(
			chi_inp,
			theta_inp,
			k_slice_theta_p_in,
			theta_parity_reg,
			first_round,
			first_block,
			round_constant_signal_sub,
			round_constant_signal[n-1]);

	(* preempts = "do_init, (do_go, do_absorb_or_squeeze, permute)" *)
	rule do_init (init_wire);
		reg_data <= zero_state;
		counter_nr_rounds <= 0;
		counter_block <= 0;
		permutation_computed <= True;
		first_block <= False;
		first_round <= False;
	endrule

	rule do_go (permutation_computed && go_wire);
		counter_nr_rounds <= 0;
		counter_block <= 0;
		permutation_computed <= False;
		first_block <= True;
		first_round <= True;  // do the first semi round
	endrule

	rule do_absorb_or_squeeze (permutation_computed && (absorb_wire || squeeze_wire));
		KState st = reg_data;
		st[(rate-1)/ns][(rate-1)%ns] = reg_data[0][0] ^ absorb_dwire;
		for (Integer i = 1; i < rate; i = i + 1)
			st[(i-1)/ns][(i-1)%ns] = reg_data[i/ns][i%ns];
		reg_data <= st;
	endrule

	rule permute (!permutation_computed);
		let first_block_new = False;
		let counter_block_new = counter_block + 1;
		let counter_nr_rounds_new = counter_nr_rounds;
		let first_round_new = first_round;
		KState st = reg_data;

		if (counter_block == 0 || counter_block != fromInteger(numSlices)) begin
			for (Integer row = 0; row < np; row = row + 1)
				for (Integer col = 0; col < ns; col = col + 1)
					st[row][col] = {
							cit.theta[row][col],
							reg_data[row][col][n-1:bitPerSubLane]
					};
		end else if (counter_block == fromInteger(numSlices)) begin
			//do_rho_pi
			st = rho_pi_out;
			counter_block_new = 0;
			counter_nr_rounds_new = counter_nr_rounds + 1;
			first_round_new = False;
			first_block_new = True;
		end

		if (counter_nr_rounds == fromInteger(numRound)) begin
			counter_block_new = counter_block + 1;
			for (Integer row = 0; row < np; row = row + 1)
				for (Integer col = 0; col < ns; col = col + 1)
					st[row][col] = {
							cit.iota[row][col],
							reg_data[row][col][n-1:bitPerSubLane]
					};
			if (counter_block == fromInteger(numSlices-1)) begin
				// do the last part of the last round
				permutation_computed <= True;
				counter_nr_rounds_new = 0;
			end
		end

		first_round <= first_round_new;
		first_block <= first_block_new;
		counter_block <= counter_block_new;
		counter_nr_rounds <= counter_nr_rounds_new;
		reg_data <= st;
	endrule

	rule theta_parity_reg_write;
		theta_parity_reg <= cit.theta_parity;
	endrule

	method Action init;
		init_wire <= True;
	endmethod
	method Action go if (permutation_computed);
		go_wire <= True;
		absorb_wire <= False;
		squeeze_wire <= False;
	endmethod
	method Action absorb(Bit#(N) din) if (permutation_computed);
		absorb_wire <= True;
		absorb_dwire <= din;
	endmethod
	method ActionValue#(Bit#(N)) squeeze if (permutation_computed);
		squeeze_wire <= True;
		return reg_data[0][0];
	endmethod
endmodule
