import socket
import sys
import os
import time
from random import randint
from multiprocessing import Process

PORT = 5000
OK_MESSAGE = 'Succesful Request!'

def handle_with_process(endpoint_socket):
    print(f'Procesando solicitud en proceso: {os.getpid()}')
    time.sleep(randint(0, 6))
    totalsent = 0
    message_bytes = bytes(OK_MESSAGE, 'utf-8')
    while totalsent < len(message_bytes):
        sent = endpoint_socket.send(message_bytes[totalsent:])
        if sent == 0:
            raise RuntimeError('Socket connection broken')
        totalsent = totalsent + sent
    endpoint_socket.close()
    sys.exit(0)

if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', PORT))
    print(f'> Listenening on port {PORT}')
    server_socket.listen(5)
    try:
        while True:
            try:
                (server_client_sock, s_addr) = server_socket.accept()
                p = Process(target = handle_with_process, args = (server_client_sock,))
                p.start()
            except socket.error:
                # stop the client disconnect from killing us
                print('Unexpected socket error')
    except Exception as e:
        print('Exception occured: \n', e)
        sys.exit(1)
    finally:
        server_socket.close()