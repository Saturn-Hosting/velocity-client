import socket
import sys
import json
import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

with open('config.json') as f:
    config = json.load(f)

server.connect((config['host'], config['port']))

while True:
    socket_list = [sys.stdin, server]
    read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            if not message:
                print("\nDisconnected from chat server")
                sys.exit()
            else:
                print(message.decode())
        else:
            message = sys.stdin.readline()
            server.send(message.encode())
            sys.stdout.write(message)
            sys.stdout.flush()
server.close()