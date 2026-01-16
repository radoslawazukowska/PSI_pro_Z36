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

            with conn:
                # tymczasowe - zmienić
                serv_msg = Message(type=MessageType.MSG, body=b"")

                while serv_msg.type != MessageType.END:
                    cli_data = conn.recv(BUFFSIZE)
                    msg = Message.from_bytes(cli_data)
                    print(f"Get data: {msg.body} from {addr}")

                    if msg.type == MessageType.END:
                        print(f"Connection from {addr} closed by client")
                        break

                    body_str = input(f"Server message: ")
                    if body_str == "end":
                        serv_msg = serv_msg = Message(type=MessageType.END, body=b"")
                        print(f"Connection to {addr} closed by server")
                    else:
                        serv_msg = Message(
                            type=MessageType.MSG, body=body_str.encode("utf-8")
                        )

                    conn.sendall(serv_msg.to_bytes())
