import socket
import sys
from time import sleep
from message import Message, MessageType
from dataclasses import dataclass


HOST = "127.0.0.1"  # The server's hostname or IP addres
PORT = 1234  # Port na ktorym nasłuchuje server


@dataclass
class Client:
    host: str
    port: int

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.settimeout(0.5)
            self.loop(s)
        print("Client finished")

    def loop(self, sock):
        while True:
            cmd = input("client> ").strip()

            # przed wykonaniem swojego zadania sprawdzam czy klient nie przerwał
            try:
                data = sock.recv(1024)
                if len(data) > 0:
                    msg = Message.from_bytes(data)
                    if msg.type == MessageType.END:
                        print("Operation not performed. Connection closed by server")
                        break
                    else:
                        print("Received:", msg.body.decode("utf-8"))

            except socket.timeout:
                pass

            if cmd == "CLH":
                # Client hello
                pass

            elif cmd == "MSG":
                cli_msg = Message(type=MessageType.MSG, body="Hello".encode("utf-8"))
                sock.sendall(cli_msg.to_bytes())

            elif cmd == "END":
                cli_msg = Message(type=MessageType.END, body=b"")
                sock.sendall(cli_msg.to_bytes())

                print("Connection closed by client")
                break
            else:
                print("Commands: CLH | MSG | END")


if __name__ == "__main__":

    host = sys.argv[1] if len(sys.argv) >= 3 else HOST
    port = int(sys.argv[2]) if len(sys.argv) >= 3 else PORT
    client = Client(host, port)
    client.run()
