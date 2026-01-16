import socket
import sys
from time import sleep
from models import Message, MessageType
from models import Session

HOST = "127.0.0.1"  # The server's hostname or IP addres
PORT = 1234  # Port na ktorym nasłuchuje server


def interactive_loop(sock, session):
    while True:
        print("1 - ClientHello")
        print("2 - ServerHello")
        print("3 - End")
        print("4 - Message")
        choice = input("> ")

        if choice == "1":
            payload = session.public_key
            msg = Message(MessageType.CLH, payload)

        elif choice == "2":
            payload = session.public_key
            msg = Message(MessageType.SVH, payload)

        elif choice == "3":
            msg = Message(MessageType.END, b"")

        elif choice == "4":
            text = input("Message: ").encode("utf-8")
            encrypted = session.encrypt_and_mac(text)
            msg = Message(MessageType.MSG, encrypted)

        else:
            print("Invalid choice")
            continue

        sock.sendall(msg.encode())

        if msg.msg_type == MessageType.END:
            break


if __name__ == "__main__":
    # sleep(5)
    # print("Client wakes up")
    inp = input("Write here: ")
    print("Input: ", inp)

    host = HOST
    port = PORT
    if len(sys.argv) < 3:
        print("No host or port specfied")
    else:
        host = sys.argv[1]
        port = int(sys.argv[2])

    print(host)
    print(port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(b"Hello, world!")
        data = s.recv(1024)
    print("Data: ", data)
    print("Client finished")
