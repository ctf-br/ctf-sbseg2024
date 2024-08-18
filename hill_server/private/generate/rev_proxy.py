import socket
import sys
import signal 
from hill_crypto import Cipher 
from math import isqrt

HOST = "0.0.0.0"      

class SimpleProxy:
    def __init__(self, dest_ip, dest_port, listen_port, is_rev):
        self.dest_ip = dest_ip
        self.dest_port = dest_port
        self.is_rev = is_rev
        self.listen_port = listen_port

        with open('key', 'rb') as f:
            self.cipher = Cipher(f.read())
 
    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.s = s 
            self.s.bind((HOST, self.listen_port))
            self.s.listen()

            print(f'Proxy listening on port {self.listen_port}')

            while True:
                try:
                    conn, addr = s.accept()
                except KeyboardInterrupt:
                    print('Quitting')
                    s.close()
                    break 

                with conn:
                    print(f"Connected by {addr}")
                    data = conn.recv(1024)
                    if self.is_rev:
                        data = self.cipher.decrypt(data)
                    else:
                        data = self.cipher.encrypt(data)

                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_http:
                        print(f'Connecting on {self.dest_ip}:{self.dest_port}')
                        s_http.connect_ex((self.dest_ip, self.dest_port))                            
                        s_http.sendall(data)

                        print('Data sent')
                        
                        resp = b''
                        while True:
                            tmp = s_http.recv(1024)
                            if not tmp:
                                break
                            resp += tmp
                            
                        print('Received response')
                        
                        if self.is_rev:
                            resp = self.cipher.encrypt(resp)
                        else:
                            resp = self.cipher.decrypt(resp)
                            
                        print(resp)

                        conn.sendall(resp)
                        conn.shutdown(socket.SHUT_RDWR)

    def quit(self):
        print('Exiting...')
        self.s.close()


if __name__ == '__main__':
    if len(sys.argv) == 5:
        host, dest_port, listen_port, is_rev = sys.argv[1:]
        
        if is_rev in ['0', '1']:
            is_rev = is_rev == '1'
            dest_port = int(dest_port)
            listen_port = int(listen_port)
            
            proxy = SimpleProxy(host, dest_port, listen_port, is_rev)
            signal.signal(signal.SIGINT, proxy.quit)
            
            proxy.start()
            exit(0)
        
    print('Usage: python rev_proxy.py DEST_HOST DEST_PORT LISTEN_PORT IS_REVERSE')
    print('IS_REVERSE = 0 or 1')
    exit(1)
                        
