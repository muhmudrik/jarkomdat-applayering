import socket
import os
from _thread import *
from threading import Thread

# ServerSocket = socket.socket()
# host = '127.0.0.1'
# port = 1233
# ThreadCount = 0
# try:
#     ServerSocket.bind((host, port))
# except socket.error as e:
#     print(str(e))

# print('Waitiing for a Connection..')
# ServerSocket.listen(5)

clients = set()
clients_lock = threading.Lock()

def listener(client, address):
    print("Accepted connection from: ", address)
    with clients_lock:
        clients.add(client)
    try:    
        while True:
            data = client.recv(1024)
            if not data:
                break
            else:
                print(repr(data))
                with clients_lock:
                    for c in clients:
                        c.sendall(data)
    finally:
        with clients_lock:
            clients.remove(client)
            client.close()

# def threaded_client(connection):
#     connection.send(str.encode('Welcome to the Server\n'))
#     while True:
#         data = connection.recv(2048)
#         reply = 'Answer: ' + data.decode('utf-8').upper()
#         if not data:
#             break
#         connection.sendall(str.encode(reply))
#     connection.close()

# while True:
#     Client, address = ServerSocket.accept()
#     print('Connected to: ' + address[0] + ':' + str(address[1]))
#     start_new_thread(threaded_client, (Client, ))
#     ThreadCount += 1
#     print('Thread Number: ' + str(ThreadCount))
# ServerSocket.close()