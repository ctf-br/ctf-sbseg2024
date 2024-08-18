PYTHON = docker run -v ./:/work -w /work --rm $(shell docker build -q .) python

all: ../../public/enc.cpython-38.pyc ../../public/out.png

../../public/out.png: out.png
	cp "$<" "$@"

out.png: __pycache__/enc.cpython-38.pyc in.png
	$(PYTHON) $< 'CTF-BR{W0w_5t3gan0gr4ph7_1s_4W3S0me}'

../../public/enc.cpython-38.pyc: __pycache__/enc.cpython-38.pyc
	cp "$<" "$@"

__pycache__/enc.cpython-38.pyc: enc.py
	$(PYTHON) -m compileall "$<"

clean:
	rm -f out.png ../../public/out.png
	rm -rf __pycache__
	rm -f ../../public/enc.cpython-38.pyc

.PHONY: clean
