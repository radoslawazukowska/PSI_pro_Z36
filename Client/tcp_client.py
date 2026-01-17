import socket
import sys
from time import sleep
from message import Message, MessageType
from session import Session
from dataclasses import dataclass, field
import threading


HOST = "127.0.0.1"  # The server's hostname or IP addres
PORT = 1234  # Port na ktorym nasłuchuje server


@dataclass
class Client:
    host: str
    port: int
    session: Session = field(default_factory=Session)

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.settimeout(0.5)
            self.loop(s)
        print("Client finished")

    def receiver(self, sock, stop_event):
        while not stop_event.is_set():
            try:
                data = sock.recv(1024)
                if not data:
                    stop_event.set()
                    break

                msg = Message.from_bytes(data)
                if msg.type == MessageType.END:
                    print("\n[!] Connection closed by server")
                    stop_event.set()
                    break
                else:
                    print("\nReceived:", msg.body)
            except socket.timeout:
                continue

    def loop(self, sock):
        stop_event = threading.Event()

        threading.Thread(
            target=self.receiver, args=(sock, stop_event), daemon=True
        ).start()

        while not stop_event.is_set():
            cmd = input("client> ").strip()

            if cmd == "END":
                sock.sendall(Message(MessageType.END, b"").to_bytes())
                stop_event.set()
                break

            elif cmd == "CLH":
                sock.sendall(Message(MessageType.CLH, b"Client Hello").to_bytes())

            elif cmd == "MSG":
                sock.sendall(Message(MessageType.MSG, b"Hello").to_bytes())


if __name__ == "__main__":

    host = sys.argv[1] if len(sys.argv) >= 3 else HOST
    port = int(sys.argv[2]) if len(sys.argv) >= 3 else PORT

    client = Client(host, port)
    client.run()
