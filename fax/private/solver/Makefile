all: fax_tests.tif

fax_tests.tif: fax.wav
	fax_tests -Ce -p FAX-replay-FAX -d "$<"

fax.wav: ../../public/fax.flac
	sox "$<" "$@"

clean:
	rm -f fax.wav fax_tests.tif

.PHONY: clean
