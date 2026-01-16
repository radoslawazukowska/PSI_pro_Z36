import socket
import sys

from models import greet

HOST = "0.0.0.0"  # The server's hostname or IP addres, standard loopback
PORT = 1234  # Port na ktorym nasłuchuje server
BUFFSIZE = 512


if __name__ == "__main__":
    print(greet("Ola"))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"Server is running on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            with conn:
                print("Connect from: ", addr)
                data = conn.recv(BUFFSIZE)
                conn.sendall(data)
            conn.close()
            print(f"Connection from {addr} closed by client")
            x = input("Potwierdź:")
            print("Potwierdzono")
