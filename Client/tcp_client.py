import socket
import sys
from time import sleep
from message import Message, MessageType


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
        s.settimeout(0.5)
        while True:
            body_str = input("Co napisać? ")

            try:
                data = s.recv(1024)
                if len(data) > 0:
                    msg = Message.from_bytes(data)
                    print("Received:", msg.body.decode("utf-8"))
                    if msg.type == MessageType.END:
                        print("Connection closed by server")
                        break
            except socket.timeout:
                pass

            msg_type = MessageType.END if body_str == "end" else MessageType.MSG
            body = b"" if msg_type == MessageType.END else body_str.encode("utf-8")

            cli_msg = Message(type=msg_type, body=body)
            s.sendall(cli_msg.to_bytes())

            if msg_type == MessageType.END:
                print("Connection closed by client")
                break

    print("Client finished")
