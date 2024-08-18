from randcrack import RandCrack


def xor(sa, sb):  
    return bytes(a^b for a, b in zip(sa, sb))


plain = open('../../public/perfil.png', 'rb').read()
cipher = open('../../public/perfil.png.enc', 'rb').read()
ks = xor(plain, cipher)

rc = RandCrack()

for i in range(624):
    rc.submit(int.from_bytes(ks[i*4:(i+1)*4], 'little'))

resto = len(cipher) - 624*4
rc.predict_getrandbits(resto * 8)

secret_enc = open('../../public/secret.png.enc', 'rb').read()
ks2 = [rc.predict_getrandbits(32).to_bytes(4, 'little') for _ in range(0, len(secret_enc), 4)]
ks2 = b''.join(ks2)

with open('secret.png', 'wb') as f:
    f.write(xor(secret_enc, ks2))

