import socket
import os
from _thread import *
import threading
from datetime import datetime
import json

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(10)

clients = set()
clients_lock = threading.Lock()
print(clients_lock)

def listener(client, address):
    print("Accepted connection from: ", address)
    with clients_lock:
        clients.add(client)
    try:    
        while True:
            current_time = datetime.now().strftime("%H:%M:%S")
            data = json.loads(client.recv(2048).decode())
            
            resp = f"{current_time} {data['nama']}: {data['message']}"
            
            if not data:
                break
            else:
                print(repr(resp))
                with clients_lock:
                    for c in clients:
                        c.sendall(resp.encode())
                    
    finally:
        with clients_lock:
            clients.remove(client)
            client.close()

while True:
    Client, address = ServerSocket.accept()

    # Apdet ke semua user ada User Baru
    usr_baru = json.loads(Client.recv(2048).decode())['nama']
    msg = usr_baru + ' telah bergabung.'
    msg = json.dumps(msg).encode()
    for c in clients:
        c.sendall(msg)
    
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(listener, (Client, address))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()


# Dokumentasi
# https://stackoverflow.com/questions/55496858/how-to-send-and-receive-message-from-client-to-client-with-python-socket