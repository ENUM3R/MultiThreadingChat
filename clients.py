import threading
import socket

host = '127.0.0.1'
port = 65432
client_number = 5

clients_list = [1,2,3,4]
message_history = []
lock = threading.Lock()

#Creating clients
def clients(client_socket, clients_list, message_history, lock):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    history = client.recv(4096).decode('utf-8')
    print(f"Chat history:\n{history}")
    thread = threading.Thread(target=receive_message, args=(client,))
    thread.start()
    print(f"If you want to exit, write 'exit'")
    while True:
        message = input(" ")
        if message.lower() == "exit":
            break
        client.send(message.encode('utf-8'))
    client.close()

def receive_message(client):
    while True:
        try:
            data = client.recv(1024)
            if not data:
                break
            print(f"\nData from server: {data.decode('utf-8')}\n> ", end="")
        except:
            print("\nConnection error.")
            break

if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clients(client_socket, clients_list, message_history, lock)