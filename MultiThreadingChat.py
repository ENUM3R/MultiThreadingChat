import threading
import socket

host = '127.0.0.1'
port = 8080
client_number = 5


#Creating server TCP
def server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(client_number)
        print('Waiting for connection...')
        clients_list = []
        message_history = []
        lock = threading.Lock()
        while True:
            client_socket, client_address = s.accept()
            clients_list.append(client_socket)
            thread = threading.Thread(target=clients,
                                      args=(client_socket, clients_list, message_history, lock))
            thread.start()
            print('Connected by ', client_address)
            data = client_socket.recv(1024)
            print(f"Data: {data.decode()}")
            lock.acquire()
            try:
                if client_socket in clients_list:
                    clients_list.remove(client_socket)
            finally:
                lock.release()
            if not data:
                break
            message_history.append(data.decode())
            if len(message_history) > 10:
                message_history.pop(0)
            print(message_history)
            client_socket.sendall(data)
        client_socket.close()

#Creating clients
def clients():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    thread = threading.Thread()
    thread.start()
    message = 'Hello World!'
    client.send(message.encode('utf-8'))

    data = client.recv(1024)
    print(f"Data from server {data.decode('utf-8')}")
    client.close()

server(host, port)