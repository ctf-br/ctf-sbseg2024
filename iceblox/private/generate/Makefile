all: ../../public/iceblox.class

../../public/iceblox.class: iceblox.java makeflag.class
	sed -Ei'' 's/new byte\[\]\{[^}]*\}/'"$$(java makeflag)/" "$<"
	javac -d ../../public --release 8 "$<"

makeflag.class: makeflag.java
	javac "$<"

clean:
	rm -f makeflag.class ../../public/iceblox.class

.PHONY: clean
