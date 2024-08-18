import sys
import os 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad 

def encrypt(key: bytes, data: bytes) -> bytes:
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    
    return iv + cipher.encrypt(pad(data, 16))


def decrypt(key: bytes, data: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, iv=data[:16])
    
    return unpad(cipher.decrypt(data[16:]), 16)
    

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('Uso: python crypto_signature.py mode key file out_file')
        exit(1)

    mode = sys.argv[1].lower()
    if mode not in ['encrypt', 'decrypt']:
        print('Modo inválido.')
        exit(1)
    
    key = open(sys.argv[2], 'rb').read()
    assert len(key) == 16
    
    data = open(sys.argv[3], 'rb').read()
    
    with open(sys.argv[4], 'wb') as f:
        if mode == 'encrypt':
            f.write(encrypt(key, data))
        elif mode == 'decrypt':
            f.write(decrypt(key, data))
        
