all: ../../public/crypto_signature.py ../../public/sample ../../public/signed_sample ../server/crypto_signature.py ../server/key ../server/password.txt

sample: sample.c
	gcc sample.c -o sample -O1

key:
	head -c 16 /dev/urandom > key 

password.txt:
	head -c 16 /dev/urandom | base64 > password.txt

signed_sample: sample key crypto_signature.py
	python crypto_signature.py encrypt key sample signed_sample

../../public/sample: sample
	cp sample ../../public

../../public/signed_sample: signed_sample
	cp signed_sample ../../public

../../public/crypto_signature.py: crypto_signature.py
	cp crypto_signature.py ../../public

../server/crypto_signature.py: crypto_signature.py
	cp crypto_signature.py ../server

../server/key: key
	cp key ../server

../server/password.txt: password.txt
	cp password.txt ../server

clean:
	rm sample signed_sample key ../../public/sample ../../public/signed_sample

