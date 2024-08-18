FRAMEWORK ?= net8.0

all: ../../public/StackOverflow.zip

../../public/StackOverflow.zip: StackOverflow/bin/Release/$(FRAMEWORK)/StackOverflow.dll
	zip -r "$@" StackOverflow/bin/Release

StackOverflow/bin/Release/$(FRAMEWORK)/StackOverflow.dll: StackOverflow/Program.fs
	set -xe; \
		cd StackOverflow; \
		dotnet build --configuration Release; \
		mv bin/Release/$(FRAMEWORK)/obfuscated/*.dll bin/Release/$(FRAMEWORK)/; \
		rm -f bin/Release/$(FRAMEWORK)/*.pdb; \
		rm -f bin/Release/$(FRAMEWORK)/obfuscar.xml; \
		rm -rf bin/Release/$(FRAMEWORK)/obfuscated

clean:
	rm -rf StackOverflow/{bin,obj}
	rm -f ../../public/StackOverflow.zip

.PHONY: clean
