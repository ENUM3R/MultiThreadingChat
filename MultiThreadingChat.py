import threading
import socket

host = '127.0.0.1'
port = 8080
client_number = 5

#Creating server TCP
def Server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(client_number)
        print('Waiting for connection...')
        conn, addr = s.accept()
        with conn:
            print('Connected by ', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Data: {data.decode()}")
                conn.sendall(data)

#Creating clients
def clients():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    message = 'Hello World!'
    client.send(message.encode('utf-8'))

    data = client.recv(1024)
    print(f"Data from server {data.decode('utf-8')}")
    client.close()