all: ../../public/fax.flac

../../public/fax.flac: fax_tests.wav
	sox "$<" "$@" remix 3,4

fax_tests.wav fax_tests.tif: fax-1.tif
	fax_tests -Cel -p FAX-FAX -i "$<"

fax-1.tif: fax.pdf
	pdftocairo -tiff "$<"

fax.pdf: fax.odt
	libreoffice --headless --convert-to pdf "$<"

clean:
	rm -f fax.pdf fax-1.tif fax_tests.wav fax_tests.tif

.PHONY: clean
