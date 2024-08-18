BSC=bsc
BSCFLAGS=-aggressive-conditions \
	-steps-warn-interval 2000000 -steps-max-intervals 6000000 \
	-opt-undetermined-vals -unspecified-to X
BSCLIBS=keccak-bsv
BSCLFLAGS=-vdir . -bdir . -simdir . \
	-suppress-warnings S0089:S0073
SRCFILES=$(wildcard *.bsv keccak-bsv/*.bsv)

YOSYS     = yosys
NEXTPNR   = nextpnr-ecp5
ECPPACK   = ecppack

PACKAGE=CABGA256
LPF=constraints/ecp5-hub-5a-75b-v7.0.lpf

NEXTPNR_FLAGS=--25k --freq 29.4912 --speed 6 --timing-allow-fail --write top-post-route.json --lpf-allow-unconstrained

all: ../../public/top.bit

# Synthesis
top.json: mkTimekeepersLock.v
	$(YOSYS) -p "\
		$(shell cat mkTimekeepersLock.use | while read m; do \
			echo "read_verilog /opt/bluespec/lib/Verilog/$$m.v; "; \
		  done)\
		read_verilog mkTimekeepersLock.v; \
		synth_ecp5 -top mkTimekeepersLock -json top.json"

top.config: top.json $(LPF)
	$(NEXTPNR) --json $< --lpf $(LPF) --textcfg $@ $(NEXTPNR_FLAGS) --package $(PACKAGE)

../../public/top.bit: top.config
	$(ECPPACK) --bit "$@" "$<"

mkTimekeepersLock.v mkKeccak.v: TimekeepersLock.bsv $(SRCFILES)
	$(BSC) $(BSCFLAGS) $(BSCLFLAGS) -u -verilog -show-module-use -p +:$(BSCLIBS) $<

tb: TimekeepersLockTb.bsv $(SRCFILES)
	$(BSC) $(BSCFLAGS) $(BSCLFLAGS) -u -sim -check-assert -p +:$(BSCLIBS) $<
	$(BSC) $(BSCLFLAGS) -sim -o $@ -e mkTimekeepersLockTb

clean:
	$(MAKE) -C keccak-bsv clean
	rm -f *.bo *.ba mk*.v mk*.cxx mk*.h mk*.o model_*.cxx model_*.h model_*.o *.use
	rm -f tb tb.so
	rm -f *.json *.config
	rm -f ../../public/top.bit

.PHONY: clean
