# keccak-bsv

This is an almost literal translation of
[Keccak's reference VHDL implementation](http://keccak.noekeon.org/KeccakVHDL-3.1.zip)
mid-range core to the Bluespec SystemVerilog (BSV) language. Our goals are:

 * Easier integration with Bluespec and/or Verilog projects, specially when simulating with
   iverilog, whose support for mixed VHDL/Verilog simulation is still at early stages.

 * Be easier to understand and customize. As Bluespec is more flexible for static elaboration
   than VHDL, our code is more compact although it implements the same architecture.

## Building

Typing `make` will test the implementation against the test vectors (using Bluesim) and
subsequently build the `mkKeccak.v` hardware core.

## Synthesis comparison

To prove that our implementation is equivalent to the reference implementation,
we synthesized both implementations (for NumSlices=32) several times targeting an
Altera Cyclone V device (5CSEMA5F31C6), varying the Quartus II fitter seed each time.
The figure below presents histograms for the clock frequency and logic utilization
obtained by each implementation.

![Synthesis results](http://thotypous.github.io/keccak-bsv/synthesis.svg)

The reference implementation (VHDL) tends to achieve a slightly higher clock frequency,
whereas our implementation (BSV) occupies somewhat less area. Overall, both
implementations produce similar results, as expected.
