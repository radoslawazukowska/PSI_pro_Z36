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
BUFFSIZE = 1024


@dataclass
class Client:
    host: str
    port: int
    session: Session = field(default_factory=Session)
    inbox: Queue = field(default_factory=Queue)
    sock: socket.socket | None = None

    def run(self):
        self.loop()

    def receiver(self, stop_event: threading.Event):
        while not stop_event.is_set() and self.sock:
            try:
                data = self.sock.recv(BUFFSIZE)
                if not data:
                    print("[!] Server closed connection")
                    stop_event.set()
                    self.reset_connection()
                    break

                msg = self.process_message(data)
                self.inbox.put(msg)

                if msg.type == MessageType.END:
                    print("\n[!] Server sent END")
                    stop_event.set()
                    self.reset_connection()
                    break

            except socket.timeout:
                continue
            except Exception as e:
                # print(f"[!] Receiver error: {e}")
                stop_event.set()
                self.reset_connection()
                break

    def reset_connection(self):
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
        self.sock = None
        self.session = Session()
        self.inbox.queue.clear()

    def send_message(self, msg: Message):
        msg_bytes = msg.to_bytes()
        if self.session.tls_established:
            msg_bytes = self.session.encrypt_and_mac(msg_bytes)
        self.sock.sendall(msg_bytes)

    def process_message(self, data) -> Message:
        if self.session.tls_established:
            data = self.session.verify_and_decrypt(data)

        return Message.from_bytes(data)

    def loop(self):
        while True:
            cmd = input("client> ").strip().upper()

            if cmd == "QUIT":
                print("[+] Exiting client")
                self.reset_connection()
                break

            if not self.session.tls_established:
                if cmd != "CONNECT":
                    print("[-] TLS not established. Allowed command: CONNECT")
                    continue

                # New TCP Connection
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.host, self.port))
                self.sock.settimeout(0.5)
                stop_event = threading.Event()

                threading.Thread(
                    target=self.receiver, args=(stop_event,), daemon=True
                ).start()

                # Send ClientHello
                self.session.generate_keys()

                self.send_message(
                    Message(MessageType.CLH, self.session.public_key_bytes())
                )

                # Wait for ServerHello
                try:
                    self.sock.settimeout(3.0)
                    msg = self.inbox.get(timeout=3)
                except Empty:
                    print("[-] Timeout waiting for ServerHello")
                    self.reset_connection()
                    continue
                finally:
                    if self.sock:
                        self.sock.settimeout(0.5)

                if msg.type == MessageType.SVH:
                    self.session.set_peer_key(msg.body)
                    self.session.calculate_shared_key()
                    print("[+] TLS established")
                else:
                    print("[-] Unexpected message from server")
                continue

            # After TLS is established
            if cmd == "CONNECT":
                print("[+] TLS already established.")
                continue

            if cmd == "END":
                self.send_message(Message(MessageType.END, b""))
                print("[+] Sent END to server, session reset")
                self.reset_connection()
                continue

            if cmd == "MSG":
                self.send_message(Message(MessageType.MSG, b"Hello"))
                print("[+] Sent MSG to server")


if __name__ == "__main__":

    host = sys.argv[1] if len(sys.argv) >= 3 else HOST
    port = int(sys.argv[2]) if len(sys.argv) >= 3 else PORT

    client = Client(host, port)
    client.run()
