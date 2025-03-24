import threading
import socket

port = 65432
host = "127.0.0.1"

def receive_message(client_socket, ):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(f"\nServer: {data}\n ", end="")
        except:
            break
def send_message(client_socket):
    print("Type your message and press enter, write 'exit' to quit")
    while True:
        client_msg = input(">")
        if client_msg.lower() == "exit":
            break
        client_socket.send(client_msg.encode())
    client_socket.close()

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    receive_thread = threading.Thread(target=receive_message, args=(client_socket,))
    send_thread = threading.Thread(target=send_message, args=(client_socket,))
    receive_thread.start()
    send_thread.start()

if __name__ == '__main__':
    main()