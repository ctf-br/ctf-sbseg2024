#!/usr/local/bin/python

from Crypto.Cipher import AES
from hashlib import md5
import os 

KEY = os.urandom(16)
USED_RNG = set()

def encrypt(data: bytes, user_rng: bytes):
    if len(user_rng) > 200:
        print('Valor aleatorio muito grande!')
        exit(0)
        
    if user_rng in USED_RNG:
        print('Valor aleatorio ja utilizado!')
        exit(0)

    USED_RNG.add(user_rng)

    nonce = md5(user_rng).digest()[:12]
    cipher = AES.new(KEY, AES.MODE_CTR, nonce=nonce)
    return cipher.encrypt(data)


def read_file(filename: str):
    try:
        f = open(filename, 'rb')
        data = f.read()
        f.close()
    except FileNotFoundError:
        print('Arquivo nao encontrado!')
        exit(0)

    return data


def main():
    print('===============================')
    print('=== SISTEMA DE ARQUIVOS OHM ===')
    print('===============================')
    print('')

    cont = 's'

    while cont == 's':
        fname = input('Arquivo: ')
        user_rng = input('Valor aleatorio (em hexadecimal, maximo 200 bytes): ')
        user_rng = bytes.fromhex(user_rng)

        data = read_file(fname)
        enc = encrypt(data, user_rng)

        print(enc.hex())

        cont = input('\nDeseja continuar (s/N)? ').lower().strip()


if __name__ == '__main__':
    main()
        
