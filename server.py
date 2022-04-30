from fileinput import filename
from Crypto.PublicKey import RSA
import socketserver, sys
from Crypto.Util.number import bytes_to_long
import logging
from datetime import datetime

logging.basicConfig(filename=datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+".log", level=logging.INFO)

key = RSA.generate(2048)

m = open("flag.txt", "r").read().encode()
assert(len(m) < key.size_in_bytes())
m = bytes_to_long(m)
ct = pow(m, key.e, key.n)
del m

banner='''welcome to NTNU orcale service
please input your action
1) get service source code
2) get leastest 2nd bit from input ciphertext
3) get ciphertext & public key
4) donate asef18766
'''

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            try:
                self.request.send(banner.encode())
                indata:str = self.request.recv(1024).decode().strip()
                logging.info('recv: ' + indata)
                if indata == '1':
                    self.request.send("please visit my github for source code\n".encode())
                elif indata == '2':
                    indata = int(self.request.recv(10240).decode().strip())
                    pt = pow(indata, key.d, key.n)
                    logging.info(pt)
                    self.request.send((bin(pt)[-2] + '\n').encode())
                elif indata == '3':
                    self.request.send(f"{ct}|({key.e}, {key.n})\n".encode())
                elif indata == '4':
                    self.request.send("please visit website and fill in the form for flag: https://forms.gle/PYMBNzYLBGQSTPcN7\n".encode())
                else:
                    self.request.send("you bad bad".encode())
                    break
            except ConnectionResetError:
                logging.info(f'client {self.request.getpeername()} closed connection.')
                break
            except Exception as e:
                logging.info(e.with_traceback())
                break

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

if __name__ == '__main__':
    HOST, PORT = '0.0.0.0', 7000
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    logging.info('server start at: %s:%s' % (HOST, PORT))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
