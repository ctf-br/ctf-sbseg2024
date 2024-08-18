#!/usr/local/bin/python

import os
from crypto_signature import decrypt

key = open('key', 'rb').read()

data = bytes.fromhex(input('Forneca o binário (em hexadecimal): '))
dec = decrypt(key, data)

# Faz esse esquema para nao precisar escrever no disco
# Precisa pois o filesystem do docker é read-only
fd = os.memfd_create('aes-integro-binary', os.MFD_CLOEXEC)
os.pwrite(fd, dec, 0)
os.execve(fd, ['binary'], {})

