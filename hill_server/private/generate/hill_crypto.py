import numpy as np
from sympy import Matrix, matrix2numpy, NotInvertible
from math import isqrt
import random


def invert_matrix(matrix: np.array):
    # Uses sympy because numpy cant invert modular matrix 

    try:
        inv = Matrix(matrix).inv_mod(256)
        return matrix2numpy(inv, dtype=np.ubyte)
    except (ValueError, NotInvertible):
        return None

    
class Cipher:
    def __init__(self, key: bytes):
        self.n = isqrt(len(key))
        assert self.n ** 2 == len(key)
        n = self.n
        
        self.matrix = np.array([ list(key[i:i+n]) for i in range(0, n*n, n) ], dtype=np.ubyte)
        self.matrix_inv = invert_matrix(self.matrix)

        assert self.matrix_inv is not None

    def pad(self, msg: bytes) -> bytes:
        rest = len(msg) % self.n
        if rest != 0:
            return msg + b'\x00' * (self.n - rest)
        return msg

    def unpad(self, msg: bytes) -> bytes:
        return msg.rstrip(b'\x00')

    def split_msg(self, msg: bytes):
        return [ msg[i:i+self.n] for i in range(0, len(msg), self.n) ]

    def _apply_matrix(self, msg: bytes, matrix: np.array) -> bytes:
        res = b''
        for block in self.split_msg(msg):
            vec = np.array(list(block), dtype=np.ubyte)
            res += bytes(matrix @ vec)

        return res

    def encrypt(self, plaintext: bytes) -> bytes:
        plaintext = self.pad(plaintext)
        return self._apply_matrix(plaintext, self.matrix)

    def decrypt(self, ciphertext: bytes) -> bytes:
        plaintext = self._apply_matrix(ciphertext, self.matrix_inv)
        return self.unpad(plaintext)

