#!/usr/bin/python3 -tt

from pathlib import Path
from socket import socket

LOAD_BALANCER_PORT_FILE = '../ex3_lb/cmake-build-debug/server_port'
RECEIVE_BUFFER_SIZE = 1024
MESSAGE_END = '\r\n\r\n'
LINE_END = '\r\n'
ERROR_404_MESSAGE = 'HTTP/1.1 404 Not Found\r\nContent-type: text/html\r\nContent-length: 113\r\n\r\n<html><head><title>Not Found</title></head><body>\r\nSorry, the object you requested was not found.\r\n</body></html>\r\n\r\n'


def get_lb_port(lb_port_filename: str = LOAD_BALANCER_PORT_FILE) -> int:
    lb_port_filepath = Path.cwd().joinpath(lb_port_filename)
    with lb_port_filepath.open('r') as lb_port_file:
        port = int(lb_port_file.readline())

    return port


def is_get_request(message):
    try:
        first_line_list = message.split(LINE_END)[0].split()
        request = first_line_list[0]
    except:
        return False
    if request == 'GET':
        return True
    else:
        return False


def is_count_address(message):
    try:
        first_line_list = message.split(LINE_END)[0].split()
        address = first_line_list[1]
    except:
        return False
    if address == '/counter':
        return True
    else:
        return False


def main():
    lb_port = get_lb_port(LOAD_BALANCER_PORT_FILE)

    lb_socket = socket()

    lb_socket.connect(('localhost', lb_port))

    count_requests = 0

    while True:
        received_all = False
        chunks = []
        bytes_received = 0
        while not received_all:
            chunk = lb_socket.recv(RECEIVE_BUFFER_SIZE)
            if len(chunk) == 0:
                raise RuntimeError('socket connection broken')

            chunks.append(chunk)
            bytes_received = bytes_received + len(chunk)

            message = ''.join([x.decode('latin-1') for x in chunks])
            if message.endswith(MESSAGE_END):
                received_all = True

        if is_count_address(message) and is_get_request(message):
            count_requests = count_requests + 1
            content_length = len(str(count_requests))
            lb_socket.send(f'HTTP/1.0 200 OK\r\nContent-Type: text/html\r\nContent-Length: {content_length}\r\n\r\n{count_requests}\r\n\r\n'.encode())
        else:
            lb_socket.send(ERROR_404_MESSAGE.encode())


if __name__ == "__main__":
    main()
