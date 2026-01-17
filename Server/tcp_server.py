import socket
import sys
import threading
from message import Message, MessageType

HOST = "0.0.0.0"  # The server's hostname or IP addres, standard loopback
PORT = 1234  # Port na ktorym nasłuchuje server
BUFFSIZE = 512


def admin_console(clients, clients_to_del, clients_lock):
    while True:
        cmd = input("server> ").strip()

        if cmd == "list":
            with clients_lock:
                print("Connected clients:")
                for cid in clients:
                    print(f" - {cid}")

        elif cmd.startswith("kick"):
            parts = cmd.split()
            if len(parts) != 2:
                print("Usage: kick <client_id>")
                continue

            client_id = int(parts[1])
            clients_to_del.append(client_id)
            # with clients_lock:
            #     conn = clients.get(client_id)

            # if conn:
            #     try:
            #         end_msg = Message(type=MessageType.END, body=b"")
            #         conn.sendall(end_msg.to_bytes())
            #         conn.close()
            #         print(f"[!] Kicked client {client_id}")
            #         del clients[client_id]
            #     except OSError:
            #         print("Error closing connection")
            # else:
            #     print("No such client")

        elif cmd == "quit":
            print("Server shutting down")
            break

        else:
            print("Commands: list | kick <id> | quit")


def handle_client(cli_id, conn, addr, clients, clients_to_del):
    with conn:
        print(f"Connected from {addr}")
        while True:
            if cli_id in clients_to_del:
                end_msg = Message(type=MessageType.END, body=b"")
                conn.sendall(end_msg.to_bytes())
                # conn.close()
                print(f"[!] Kicked client {client_id}")
                del clients[client_id]
                clients_to_del.remove(client_id)
                break

            cli_data = conn.recv(BUFFSIZE)
            msg = Message.from_bytes(cli_data)

            print(f"Get data from {addr}: {msg.body.decode('utf-8')}")

            if msg.type == MessageType.END:
                print(f"Connection from {addr} closed by client")
                conn.close()
                break

            # body_str = input("Server message: ")
            # msg_type = MessageType.END if body_str == "end" else MessageType.MSG
            # body = b"" if msg_type == MessageType.END else body_str.encode()

            # serv_msg = Message(type=MessageType.MSG, body=b"ACK")
            # conn.sendall(serv_msg.to_bytes())

            # if msg_type == MessageType.END:
            #     print(f"Connection to {addr} closed by server")
            #     break


if __name__ == "__main__":
    clients = {}
    clients_to_del = []
    clients_lock = threading.Lock()
    client_id_counter = 0

    threading.Thread(
        target=admin_console, daemon=True, args=(clients, clients_to_del, clients_lock)
    ).start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"Server is running on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            # cli_thread = threading.Thread(
            #     target=handle_client, args=(conn, addr), daemon=True
            # )

            with clients_lock:
                client_id_counter += 1
                client_id = client_id_counter
                clients[client_id] = conn

            cli_thread = threading.Thread(
                target=handle_client,
                args=(client_id, conn, addr, clients, clients_to_del),
                daemon=True,
            )
            # t.start()

            cli_thread.start()
            print("New client thread started")
