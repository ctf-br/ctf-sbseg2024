from pwn import *
import os 

# https://www.mscs.dal.ca/~selinger/md5collision/
SEQ1 = bytes.fromhex('d131dd02c5e6eec4693d9a0698aff95c2fcab58712467eab4004583eb8fb7f8955ad340609f4b30283e488832571415a085125e8f7cdc99fd91dbdf280373c5bd8823e3156348f5bae6dacd436c919c6dd53e2b487da03fd02396306d248cda0e99f33420f577ee8ce54b67080a80d1ec69821bcb6a8839396f9652b6ff72a70')
SEQ2 = bytes.fromhex('d131dd02c5e6eec4693d9a0698aff95c2fcab50712467eab4004583eb8fb7f8955ad340609f4b30283e4888325f1415a085125e8f7cdc99fd91dbd7280373c5bd8823e3156348f5bae6dacd436c919c6dd53e23487da03fd02396306d248cda0e99f33420f577ee8ce54b67080280d1ec69821bcb6a8839396f965ab6ff72a70 ')

def get_enc(fname, rng):
    conn.sendlineafter(b'Arquivo: ', fname.encode())
    conn.sendlineafter(b'bytes): ', rng.hex().encode())

    return bytes.fromhex(conn.recvline().decode())


cwd = os.path.abspath('../server')
#conn: tube = process(['python', 'server.py'], cwd=cwd)
conn: tube = remote('localhost', 5000)

flag_enc = get_enc('flag.txt', SEQ1)
conn.sendline(b's')
server_enc = get_enc('server.py', SEQ2)
conn.sendline(b'n')

with open(os.path.join(cwd, 'server.py'), 'rb') as f:
    ks = xor(server_enc, f.read())

flag = xor(ks, flag_enc)
print(flag[:1+flag.find(b'}')].decode())
    
