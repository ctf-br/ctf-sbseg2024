from hill_crypto import Cipher
import random

KEY_SIZE = 7

while True:
    key = random.randbytes(KEY_SIZE**2)
    try:
        Cipher(key)
    except AssertionError as ex:
        continue

    with open('key', 'wb') as f:
        f.write(key)

    break

