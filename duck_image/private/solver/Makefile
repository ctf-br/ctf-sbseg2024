all: enc.decompyled.py

enc.decompyled.py: ../../public/enc.cpython-38.pyc
	poetry run decompyle3 "$<" > "$@"
