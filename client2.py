import socket
import json
from _thread import *
import threading

client_socket = socket.socket()
host = '127.0.0.1'
port = 1233

data = {}
nama = input("Masukkan nama anda: \n")
data['nama'] = nama
data['status'] = "nama"

try:
    client_socket.connect((host, port))
    print(f"Koneksi ke {host}:{port} Berhasil!")
    client_socket.send(json.dumps(data).encode())
except socket.error as e:
    print(str(e))

exit = False

def client_send():
    while True:
        word = input('')
        # print(word)
        data['message'] = word
        data['status'] = "message"
        # print(f"data: {data}")
        client_socket.send(json.dumps(data).encode())

def client_recv():
    while True:
        reply = client_socket.recv(2048)
        print(reply.decode('utf-8'))

td = threading.Thread(target = client_send)
td.start()

tdd = threading.Thread(target = client_recv)
tdd.start()

# while True:
#     word = input('> ')
#     data['message'] = word
#     data['status'] = "message"
#     client_socket.send(json.dumps(data).encode())
#     Response = client_socket.recv(2048)
#     print("> ",Response.decode('utf-8'))


# client_socket.close()
