import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

zeroed = False
while True:
    msg = b'CTF-BR{4Ovrg1MrNdjF}'
    if zeroed:
        msg = b'\x00'*len(msg)
    print(msg)
    sock.sendto(msg, ("192.168.0.2", 51966))
    zeroed = not zeroed
    time.sleep(1)
