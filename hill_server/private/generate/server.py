from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import sys

FLAG = 'CTF-BR{h1lL_c1Ph3r_eh_H0rr1vLl}'

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ['/', '/flag']:
            self.send_response(400)
            self.end_headers()
            return
        
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        HEADER = b'<html><head><title>Hill Server</title></head><body>'
        FOOTER = b'</body></html>'

        self.wfile.write(HEADER)
        if self.path == '/':
            self.wfile.write(f'<h1>Links úteis</h1><a href="http://{HOSTNAME}:{FORWARD_PORT}/flag">Flag</a>'.encode())
        else:
            self.wfile.write(f'<p>{FLAG}</p>'.encode())
        self.wfile.write(FOOTER)
            
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('Usage: python server.py LISTEN_PORT HOSTNAME FORWARD_PORT')
        exit(1)
        
    LISTEN_PORT, HOSTNAME, FORWARD_PORT = sys.argv[1:]
    LISTEN_PORT = int(LISTEN_PORT)
    webServer = HTTPServer(('localhost', LISTEN_PORT), MyServer)
    print("Server started http://localhost:%s" % (LISTEN_PORT))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
