import numpy as np
from sympy import Matrix, matrix2numpy, NotInvertible
from math import isqrt
import itertools

# Valores extraidos do pcap

# enc_sent e enc_got voce peder por seguir a primeira tcp stream
enc_sent = bytes.fromhex('8af983c898a0ced53bd89533dc221d26d2c1a1949fcfdce7127319536cd9d34b2f169551ed4f61107eb353005ae0a2994b355db31be01d98aa68ffdc989af6e11e9a626e09531ca35bb96c46e82f79521618330405b86703173caf')
enc_got = bytes.fromhex('85096b0aaa3f743943e3b515d6042e952caf33e068c57eeb2977677bacd3fad88eb75df08a3a9963ae98f70b994c094bfc40f56f00696dc9ffe0c8c12134db18441ceddbf5bce0082c8c98dcaa4cef0724390ab9cd92897fc4dcd8f61595dd81a0db7ff341fded7cc39e671163eb5c7f165eba1ee455b5b2f32099034e722a1019ff707822dd9c223b52c4cd656aac04bcd8c6b82ba10e2bf9f1a847cc6d2292c5dddc00fc0b2ed93bfca602b4f949e323934044d868fd4182c23ecc3cf287e42a7b6afe085210267d56b96adb3b26d788b5d1c33472ea6a27430c73314c454a7e766ca9f85fd51354ea8e4d7ee2a6afa9f6fb5f7f8a79f4a7ae5032aef124f9cbacf2ec2ea15de43c9ca99076e8ca500b')

# Esse aqui e o valor de retorno do site, na segunda tcp stream
targ_ciphertext = bytes.fromhex('85096b0aaa3f743943e3b515d6042e952caf33e068c57eeb2977677bacd3fad88eb75df08a3a9963ae98f70b994c094bfc40f56f00696dc9ffe0c8c12134db18441ceddbf5bce0082c8c98dcaa75e4f8e93cbc6fcd92897fc4dcd8f61595dd81a0db7ff341fded7cc39e671163eb5c7f165eba1ee455b5b2f32099034e722a1019ff707822dd9c223b52c4cd656aac04bcd8c6b82ba10e2bf9f1a847cc6d2292c5dddc00fc0b2ed93bfca602b4f949e323934044d868507a3e7f81b606ac7b2d27c5535d3f2c2631d08e4e5a5186928de85096fb2f4e3b2a33927c096b9b494d972778d5221f7c6deb68b42e7217')

n = 7

# Deixa a formatacao para brutar a versao do http depois
known_sent = 'GET / HTTP/{version}\r\nHost: headquarter.secure.hill\r\nUser-Agent: '
knwon_got = 'HTTP/{version} 200 OK\r\n'
all_versions = ['1.0', '1.1', '2']


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

    
def solve(ciphertexts, plaintexts):
    back_pl = list(plaintexts)
    back_ci = list(ciphertexts)

    # Escolhe n entre os plaintexts/ciphertexts para serem usados
    # Bruta por todas combinações: alguma delas deve dar certo
    for selec in itertools.combinations(range(len(plaintexts)), n):
        plaintexts = [back_pl[i] for i in selec]
        ciphertexts = [back_ci[i] for i in selec]

        # Monta a matriz de plaintexts
        matrix = np.array( [ list(plaintext) for plaintext in plaintexts ] , dtype=np.ubyte)
        matrix_inv = invert_matrix(matrix)

        if matrix_inv is not None:
            break
    else:
        return False 

    # Recupera a chave, linha por linha
    key = []
    for i in range(n):
        vec = np.array([ciphertexts[j][i] for j in range(n)], dtype=np.ubyte)
        key.extend(list(matrix_inv @ vec))

    try:
        cipher = Cipher(key)
    except AssertionError as ex:
        return False

    res = cipher.decrypt(targ_ciphertext)
    if b'CTF-BR' not in res:
        return False

    print(res)
    return True



for v1, v2 in itertools.product(all_versions, repeat=2):
    print(v1, v2)
    
    def trim(lst):
        # Faz com que a lista seja múltiplo de n, removendo elementos do final
        r = len(lst) % n
        if r == 0:
            return lst
        return lst[:-r]
        
    sent = known_sent.format(version=v1).encode()
    sent = trim(sent)

    got = knwon_got.format(version=v2).encode()
    got = trim(got)

    all_known = sent + got
    all_enc = enc_sent[:len(sent)] + enc_got[:len(got)]

    ciphertexts = []
    plaintexts = []
    
    for i in range(0, len(all_enc), n):
        ciphertexts.append(all_enc[i:i+n])
        plaintexts.append(all_known[i:i+n])

    if not solve(ciphertexts, plaintexts):
        print('Nao deu')
        
