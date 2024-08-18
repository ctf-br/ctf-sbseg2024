from Crypto.Util.number import bytes_to_long, getPrime 

flag = bytes_to_long(b'CTF-BR{M3ns@gEM_t3M_Q_s3r_c0prim0}')

p, q = getPrime(512), getPrime(512)
N = p*q

e = 0x10001

mf = pow(flag, e, N)
mp = pow(p, e, N)

print(f'(N, e) = {hex(N), hex(e)}')
print(f'mf = {hex(mf)}')
print(f'mp = {hex(mp)}')

