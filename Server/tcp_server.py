import socket
import sys
import threading
from message import Message, MessageType
from dataclasses import dataclass, field

HOST = "0.0.0.0"  # The server's hostname or IP addres, standard loopback
PORT = 1234  # Port na ktorym nasłuchuje server
BUFFSIZE = 512


@dataclass
class Server:
    clients: dict = field(default_factory=dict)
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
            print(f"Connected from {addr}")
            while True:
                if client_id in self.clients_to_del:
                    end_msg = Message(type=MessageType.END, body=b"")
                    conn.sendall(end_msg.to_bytes())

                    print(f"[!] Kicked client {client_id}")
                    del self.clients[client_id]
                    self.clients_to_del.remove(client_id)
                    break

                try:
                    cli_data = conn.recv(BUFFSIZE)
                    if not cli_data:
                        break
                    msg = Message.from_bytes(cli_data)
                    if msg.type == MessageType.END:
                        print(f"Connection closed by client {addr}")
                        del self.clients[client_id]
                    else:
                        print(f"Get data from {addr}: {msg.body.decode('utf-8')}")
                except socket.timeout:
                    continue


if __name__ == "__main__":
    server = Server()
    server.run()
