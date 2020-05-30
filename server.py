import os
from pathlib import Path
from socket import socket

LOAD_BALANCER_PORT_FILE = '../ex3_lb/cmake-build-debug/server_port'
RECIEVE_BUFFER_SIZE = 1024
MESSAGE_END = '\r\n\r\n'

def get_lb_port(lb_port_filename: str = LOAD_BALANCER_PORT_FILE) -> int:
    lb_port_filepath = Path.cwd().joinpath(lb_port_filename)
    #with open(LOAD_BALANCER_PORT_FILE, 'r') as lb_port_file:
    with lb_port_filepath.open('r') as lb_port_file:
        port = int(lb_port_file.readline())

    return port

def main():
    lb_port = get_lb_port(LOAD_BALANCER_PORT_FILE)
    
    lb_socket = socket()
    print(f'Connecting to server on port {lb_port}')
    lb_socket.connect(('localhost', lb_port))

    recieved_all = False
    chunks = []
    bytes_recieved = 0
    with lb_socket:
        while not recieved_all:
            chunk = lb_socket.recv(RECIEVE_BUFFER_SIZE)
            print(f'Got chunk: {chunk}')
            if chunk == '':
                raise RuntimeError('socket connection broken')

            if chunk.endswith(MESSAGE_END.encode()):
                recieved_all = True

            chunks.append(chunk)
            bytes_recieved = bytes_recieved + len(chunk)

    message = ''.join([x.decode('latin-1') for x in chunks])
    print(message)
    


if __name__ == "__main__":
    main()