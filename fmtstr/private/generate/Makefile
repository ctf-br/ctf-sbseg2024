CC = gcc
CFLAGS = -Wall -fstack-protector-all -no-pie

all: ../../public/run

../../public/run: main.c
	$(CC) $(CFLAGS) -o $@ $^
	strip $@
	cp $@ ../server/

clean:
	rm -f ../../public/run ../server/run

run: ../../public/run
	./$<

.PHONY: clean run
