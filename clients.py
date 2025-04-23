import threading
import socket
import consoleColors as cc

port = 65432
host = "127.0.0.1"

#function to receive messages from server, handles separate threads
def receive_message(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                print(f"{cc.ConsoleColors.RED}\nDisconnected from server.")
                break
            print(f"{cc.ConsoleColors.MAGENTA}\nServer: {data}\n ", end="")
        except:
            break

#function to send message from client to server, handles separate threads
def send_message(client_socket):
    print(f"{cc.ConsoleColors.GREEN}Type your message and press enter, write 'exit' to quit")
    while True:
        try:
            client_msg = input(f"{cc.ConsoleColors.GREEN}>")
            if client_msg.lower() == "exit":
                client_socket.send(client_msg.encode())
                break
            client_socket.send(client_msg.encode())
        except:
            break
    client_socket.close()

#main function, client initialization
def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    #starting threads for sending and receiving messages
    receive_thread = threading.Thread(target=receive_message, args=(client_socket,))
    send_thread = threading.Thread(target=send_message, args=(client_socket,))
    receive_thread.start()
    send_thread.start()

    send_thread.join()
    client_socket.close()

if __name__ == '__main__':
    main()