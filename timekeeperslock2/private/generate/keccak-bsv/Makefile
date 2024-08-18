BSCFLAGS=-aggressive-conditions \
	-steps-warn-interval 2000000 -steps-max-intervals 6000000 \
	-opt-undetermined-vals -unspecified-to X

all: test mkKeccak.v

test: tb
	./tb < test_vectors/keccak_in.txt > test_vectors/keccak_out.txt
	diff -b test_vectors/keccak_out.txt test_vectors/keccak_ref.txt

mkKeccak.v: $(wildcard *.bsv)
	bsc $(BSCFLAGS) -u -verilog Keccak.bsv

mkKeccakTb.v: $(wildcard *.bsv)
	bsc $(BSCFLAGS) -u -verilog KeccakTb.bsv

tb: $(wildcard *.bsv)
	bsc $(BSCFLAGS) -u -sim KeccakTb.bsv
	bsc -sim -o $@ -e mkKeccakTb

clean:
	rm -f *.bo *.ba mk*.v mk*.cxx mk*.h mk*.o model_*.cxx model_*.h model_*.o
	rm -f tb tb.so
	rm -f test_vectors/*_out.txt
