import socket
import sys
from time import sleep

HOST = "127.0.0.1"  # The server's hostname or IP addres
PORT = 1234  # Port na ktorym nasłuchuje server

if __name__ == "__main__":
    sleep(5)
    print("Client wakes up")

    host = HOST
    port = PORT
    if len(sys.argv) < 3:
        print("No host or port specfied")
    else:
        host = sys.argv[1]
        port = int(sys.argv[2])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(b"Hello, world!")
        data = s.recv(1024)
    print("Data: ", data)
    print("Client finished")
