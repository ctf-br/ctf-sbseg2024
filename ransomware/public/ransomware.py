import random
from glob import glob 
import sys 


def xor(sa, sb):  
    return bytes(a^b for a, b in zip(sa, sb))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Uso: python ransomware.py SEED')
        exit(1)

    if sys.argv[1].startswith('0x'):
        seed = int(sys.argv[1], 16)
    else:
        seed = int(sys.argv[1])
    random.seed(seed)

    files = list(glob('*.png'))
    files.sort()

    for file in files:
        with open(file, 'rb') as f:
            data = f.read()

        with open(file + '.enc', 'wb') as f:
            f.write(xor(data, random.randbytes(len(data))))
