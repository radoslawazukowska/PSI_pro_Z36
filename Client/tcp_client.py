import socket
import sys
from time import sleep
from message import Message, MessageType
from session import Session
from dataclasses import dataclass, field
import threading
from queue import Empty, Queue


HOST = "127.0.0.1"  # The server's hostname or IP addres
PORT = 1234  # Port na ktorym nasłuchuje server


@dataclass
class Client:
    host: str
    port: int
    session: Session = field(default_factory=Session)
    inbox: Queue = field(default_factory=Queue)

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
                self.inbox.put(msg)

                if msg.type == MessageType.END:
                    print("\n[!] Connection closed by server")
                    stop_event.set()
                    break

            except socket.timeout:
                continue

    def loop(self, sock):
        stop_event = threading.Event()

        threading.Thread(
            target=self.receiver, args=(sock, stop_event), daemon=True
        ).start()

        while not stop_event.is_set():
            cmd = input("client> ").strip()

            if not self.session.tls_established:
                if cmd == "CONNECT":
                    self.session.generate_keys()
                    sock.sendall(
                        Message(
                            MessageType.CLH, self.session.public_key_bytes()
                        ).to_bytes()
                    )

                    try:
                        sock.settimeout(3.0)
                        msg = self.inbox.get()
                    except Empty:
                        print("[-] Timeout waiting for ServerHello")
                        continue
                    finally:
                        sock.settimeout(0.5)

                    if msg.type == MessageType.SVH:
                        self.session.set_peer_key(msg.body)
                        self.session.calculate_shared_key()
                        print("[+] TLS established")
                        continue
                else:
                    print("[-] Please establish TLS first using CONNECT command.")
                    continue

            # After TLS established
            if cmd == "CONNECT":
                print("TLS already established.")
                continue

            if cmd == "END":
                sock.sendall(Message(MessageType.END, b"").to_bytes())
                stop_event.set()
                print("[+] Sent END to server")
                break

            elif cmd == "MSG":
                sock.sendall(Message(MessageType.MSG, b"Hello").to_bytes())
                print("[+] Sent MSG to server")


if __name__ == "__main__":

    host = sys.argv[1] if len(sys.argv) >= 3 else HOST
    port = int(sys.argv[2]) if len(sys.argv) >= 3 else PORT

    client = Client(host, port)
    client.run()
