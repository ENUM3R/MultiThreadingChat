import threading
import socket
import datetime
import consoleColors as cc

port = 65432
host = "127.0.0.1"
clients_list = {}  # Dictionary for clients: key = address, value = socket
lock = threading.Lock()  # Lock for synchronization


# Function to manage communication with a client
def manage_chat(client_socket, client_address):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
        except ConnectionResetError:
            break
        time = datetime.datetime.now().strftime("%H:%M:%S")
        msg = f"{cc.ConsoleColors.BLUE}Client: {client_address}:[{time}]:{data}"
        print(msg)
        # Broadcast the message to all other clients
        with lock:
            for client_addr, client_sock in clients_list.items():
                if client_addr != client_address:
                    try:
                        client_sock.send(msg.encode())
                    except:
                        pass
        # If client sends 'exit', disconnect them
        if data.lower() == "exit":
            print(f"{cc.ConsoleColors.RED} Connection with client {client_address} has ended!")
            break
    # Remove client from the list when they disconnect
    with lock:
        del clients_list[client_address]
    client_socket.close()
    print(f"Connection with {client_address} lost.")

# Function to allow the server to send a message to all clients
def server_input_thread():
    while True:
        response = input(f"{cc.ConsoleColors.MAGENTA}Server: ")
        if response.lower() == "exit":
            print(f"{cc.ConsoleColors.WHITE}Shutting down server...")
            with lock:
                for _, client_sock in clients_list.items():
                    client_sock.send("Server is shutting down...".encode())
                    client_sock.close()
            exit()
        elif response.lower().startswith("choose "):
            # Get the target client port from the input command
            try:
                _, target_port, *message = response.split()
                target_port = int(target_port)
                message = " ".join(message)
                # Find the client by port and send the message
                target_client = None
                for client_addr, client_sock in clients_list.items():
                    if client_addr[1] == target_port:
                        target_client = client_sock
                        break
                if target_client:
                    target_client.send(f"{cc.ConsoleColors.CYAN}Message from server: {message}".encode())
                    print(f"Message sent to client with port {target_port}.")
                else:
                    print(f"{cc.ConsoleColors.RED}Client with port {target_port} not found.")
            except ValueError:
                print(f"{cc.ConsoleColors.RED}Invalid port or message format.")
        elif response.strip():
            # Send the message to all clients
            with lock:
                for _, client_sock in clients_list.items():
                    try:
                        client_sock.send(f"{response}".encode())
                    except:
                        pass


# Main function to start the server
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Server Listening on host:{host}, port:{port}")

    # Start a thread for the server to send messages
    server_thread = threading.Thread(target=server_input_thread, daemon=True)
    server_thread.start()

    # Accept incoming client connections and start threads for each
    while True:
        client_socket, client_address = server_socket.accept()
        print("Client connected: ", client_address)
        with lock:
            clients_list[client_address] = client_socket
        client_thread = threading.Thread(target=manage_chat, args=(client_socket, client_address))
        client_thread.start()


if __name__ == "__main__":
    main()
