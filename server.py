from pathlib import Path
from socket import socket

LOAD_BALANCER_PORT_FILE = './server_port'
RECIEVE_BUFFER_SIZE = 1024
MESSAGE_END = '\r\n\r\n'

def get_lb_port(lb_port_filename: str = LOAD_BALANCER_PORT_FILE) -> int:
    lb_port_filepath = Path.cwd().joinpath(lb_port_filename)
    with lb_port_filepath.open('r') as lb_port_file:
        port = int(lb_port_file.readline())

    return port

def main():
    lb_port = get_lb_port(LOAD_BALANCER_PORT_FILE)
    
    lb_socket = socket()
    lb_socket.connect(('localhost', lb_port))

    recieved_all = False
    chunks = []
    bytes_recieved = 0
    while not recieved_all:
        chunk = socket.recv(bufsize=RECIEVE_BUFFER_SIZE)
        if chunk == '':
            raise RuntimeError('socket connection broken')

        if chunk.endswith(MESSAGE_END):
            recieved_all = True

        chunks.append(chunk)
        bytes_recieved = bytes_recieved + len(chunk)

    return ''.join(chunks)
    


if __name__ == "__main__":
    main()