all: secret.png.enc perfil.png.enc ../../public/ransomware.py ../../public/perfil.png.enc ../../public/perfil.png ../../public/secret.png.enc

perfil.png.enc secret.png.enc: perfil.png secret.png ransomware.py
	python ransomware.py $$(head -c 16 /dev/urandom | cksum | cut -f1 -d " ")

../../public/%: %
	cp $< ../../public

clean:
	rm secret.png.enc perfil.png.enc ../../public/ransomware.py ../../public/perfil.png.enc ../../public/perfil.png ../../public/secret.png.enc
