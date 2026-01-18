import socket
import sys
import threading
from message import Message, MessageType
from session import Session
from dataclasses import dataclass, field

HOST = "0.0.0.0"  # The server's hostname or IP addres, standard loopback
PORT = 1234  # Port na ktorym nasłuchuje server
BUFFSIZE = 512


@dataclass
class Server:
    clients: dict = field(default_factory=dict)
    clients_sessions: dict = field(default_factory=dict)
    clients_to_del: list = field(default_factory=list)
    clients_lock: threading.Lock = field(default_factory=threading.Lock)
    client_id_counter: int = 0

    def run(self):
        threading.Thread(
            target=self.admin_console,
            daemon=True,
            args=(),
        ).start()
        self.loop()

    def admin_console(self):
        while True:
            cmd = input("server> ").strip()

            if cmd == "list":
                with self.clients_lock:
                    print("Connected clients:")
                    for cid in self.clients:
                        print(f" - {cid}")

            elif cmd.startswith("kick"):
                parts = cmd.split()
                if len(parts) != 2:
                    print("Usage: kick <client_id>")
                    continue

                client_id = int(parts[1])
                self.clients_to_del.append(client_id)

            elif cmd == "quit":
                print("Server shutting down")
                break

            else:
                print("Commands: list | kick <id> | quit")

    def loop(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen(5)
            print(f"Server is running on {HOST}:{PORT}")

            while True:
                conn, addr = s.accept()

                with self.clients_lock:
                    self.client_id_counter += 1
                    client_id = self.client_id_counter
                    self.clients[client_id] = conn
                    self.clients_sessions[client_id] = Session()

                cli_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_id, conn, addr),
                    daemon=True,
                )

                cli_thread.start()
                print("New client thread started")

    def handle_client(self, client_id, conn, addr):
        with conn:
            conn.settimeout(0.5)
            print(f"TCP connection from {addr}")
            session = self.clients_sessions[client_id]

            while True:
                # delete client if requested by admin
                with self.clients_lock:
                    if client_id in self.clients_to_del:
                        conn.sendall(Message(MessageType.END, b"").to_bytes())
                        self.delete_client(client_id)
                        break

                try:
                    cli_data = conn.recv(BUFFSIZE)
                    if not cli_data:
                        break

                    msg = Message.from_bytes(cli_data)

                    if not session.tls_established:
                        if msg.type == MessageType.CLH:
                            session.generate_keys()
                            conn.sendall(
                                Message(
                                    MessageType.SVH, session.public_key_bytes()
                                ).to_bytes()
                            )
                            session.set_peer_key(msg.body)
                            session.calculate_shared_key()
                            print(f"TLS session established with {addr}")
                            continue
                        else:
                            print(f"Unexpected message from {addr} before TLS")
                            continue

                    # after TLS established
                    if msg.type == MessageType.END:
                        print(f"Connection closed by client {addr}")
                        with self.clients_lock:
                            del self.clients[client_id]
                        break

                    elif msg.type == MessageType.MSG:
                        print(f"Get data from {addr}: {msg.body.decode()}")

                except socket.timeout:
                    continue

    def delete_client(self, client_id):
        self.clients_to_del.remove(client_id)
        del self.clients[client_id]
        del self.clients_sessions[client_id]
        print(f"[!] Deleted client {client_id}")


if __name__ == "__main__":
    server = Server()
    server.run()
