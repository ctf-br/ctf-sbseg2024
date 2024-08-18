CC = gcc
CFLAGS = -Wall -fno-stack-protector -no-pie

all: ../../public/run

../../public/run: brop.c
	$(CC) $(CFLAGS) -o $@ $^
	strip $@
	cp $@ ../server/

clean:
	rm -f ../../public/run ../server/run

run: ../../public/run
	./$<

.PHONY: clean run
