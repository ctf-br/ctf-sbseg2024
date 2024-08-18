CC = riscv64-linux-gnu-gcc
CFLAGS = -Wall -fstack-protector-all -march=rv64id
STRIP = riscv64-linux-gnu-strip
QEMU = qemu-riscv64
QFLAGS = -L /usr/riscv64-linux-gnu

all: ../../public/rvrop

../../public/rvrop: rvrop.c
	$(CC) $(CFLAGS) -o $@ $^
	$(STRIP) $@
	cp $@ ../server/

clean:
	rm -f ../../public/rvrop ../server/rvrop 

run: ../../public/rvrop
	$(QEMU) $(QFLAGS) $<

.PHONY: clean run
