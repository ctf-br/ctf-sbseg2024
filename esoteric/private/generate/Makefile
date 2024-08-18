CC = riscv64-linux-gnu-gcc
CFLAGS = -Os -Wall
STRIP = riscv64-linux-gnu-strip
QEMU = qemu-riscv64
QFLAGS = -L /usr/riscv64-linux-gnu
LUA = luajit

all: ../../public/esoteric

../../public/esoteric: main.dynasm.o
	$(CC) -o $@ $^
	$(STRIP) $@
	cp $@ ../server/

main.dynasm.c: main.c
	$(LUA) LuaJIT/dynasm/dynasm.lua $< > $@ || rm $@

clean:
	rm -f *.dynasm.c *.o ../../public/esoteric ../server/esoteric 

run: ../../public/esoteric
	$(QEMU) $(QFLAGS) $<

.PHONY: clean run
