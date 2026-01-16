import socket
import sys
from message import Message, MessageType

HOST = "0.0.0.0"  # The server's hostname or IP addres, standard loopback
PORT = 1234  # Port na ktorym nasłuchuje server
BUFFSIZE = 512


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"Server is running on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            print(f"Connected from {addr}")

            with conn:
                while True:
                    cli_data = conn.recv(BUFFSIZE)
                    msg = Message.from_bytes(cli_data)

                    print(f"Get data from {addr}: {msg.body.decode('utf-8')}")

                    if msg.type == MessageType.END:
                        print(f"Connection from {addr} closed by client")
                        break

                    body_str = input("Server message: ")
                    msg_type = MessageType.END if body_str == "end" else MessageType.MSG
                    body = b"" if msg_type == MessageType.END else body_str.encode()

                    serv_msg = Message(type=msg_type, body=body)
                    conn.sendall(serv_msg.to_bytes())

                    if msg_type == MessageType.END:
                        print(f"Connection to {addr} closed by server")
                        break
