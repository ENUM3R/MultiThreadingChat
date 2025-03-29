import threading
import socket
import datetime

port = 65432
host = "127.0.0.1"
clients_list = {} #dictionary for clients address
lock = threading.Lock() #blockade for synchronization access to clients_list

#function to manage chat from server perspective
def manage_chat(client_socket, client_address):
    global selected_client_port
    selected_client_port = client_address[1]
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
        if data.lower() == "exit":
            break
        selected_client_port = client_address[1]
        while True:
            response = input(f"Server->{selected_client_port} ('change' to change client, 'end' to stop server): \n")
            if response.lower() == "end":
                print("Shutting down...")
                with lock:
                    for _, client_sock in clients_list.items():
                        client_sock.close()
                exit()
            elif response.lower() == "change":
                client_choice_port = input("Enter client port to answer: ")
                try:
                    client_choice_port = int(client_choice_port)
                    with lock:
                        if client_choice_port in [addr[1] for addr in clients_list.keys()]:
                            selected_client_port = client_choice_port
                        else:
                            print(f"No client found on port {client_choice_port}, please try again.")
                except ValueError:
                    print("Invalid input. Please enter a valid port number.")
                continue
            else:
                with lock:
                    selected_client_socket = next(
                        (client_sock for client_addr, client_sock in clients_list.items() if
                         client_addr[1] == selected_client_port),
                        None
                    )
                    if selected_client_socket:
                        selected_client_socket.send(response.encode())
                    else:
                        print("No client selected or client disconnected.")
                break
    with lock:
        del clients_list[client_address]
    client_socket.close()
    print(f"Connection with {client_address} lost.")

#main function, where server starts working
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