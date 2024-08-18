all: ../../public/flagchecker
	QEMU_LD_PREFIX=/usr/riscv64-linux-gnu qemu-riscv64 ../../public/flagchecker 'CTF-BR{6CVTspw7n84hbEs6}'

../../public/flagchecker: flagchecker.c
	riscv64-linux-gnu-gcc -O0 -o "$@" "$<"
	riscv64-linux-gnu-strip "$@"

clean:
	rm -f ../../public/flagchecker

.PHONY: clean sanity_check
