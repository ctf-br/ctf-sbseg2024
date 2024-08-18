JAVA_HOME ?= /usr/lib/jvm/java-8-openjdk

all: solve.class
	$(JAVA_HOME)/bin/appletviewer solve.html

solve.class: solve.java
	javac --release 8 "$<"

clean:
	rm -f solve.class

.PHONY: clean
