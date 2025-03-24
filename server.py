import threading
import socket
import datetime

port = 65432
host = "127.0.0.1"
clients_list = {}
lock = threading.Lock()

def manage_chat(client_socket, client_address):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
        except ConnectionResetError:
            break
        time = datetime.datetime.now().strftime("%H:%M:%S")
        msg = f"Client: {client_address}:[{time}]:{data}"
        print(msg)
        while True:
            response = input(f"Server->{client_address}: ")
            if response != "":
                try:
                    client_socket.send(response.encode())
                    break
                except:
                    break
    with lock:
        del clients_list[client_address]
    client_socket.close()
    print(f"Connection with {client_address} disconnected.")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Server Listening on host:{host}, port:{port}")
    while True:
        client_socket, client_address = server_socket.accept()
        print("Client connected: ", client_address)
        with lock:
            clients_list[client_address] = client_socket
        thread = threading.Thread(target=manage_chat, args=(client_socket,client_address))
        thread.start()

if __name__ == "__main__":
    main()