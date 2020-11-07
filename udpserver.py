import socket, os, threading, queue, json
from datetime import datetime
from _thread import *

host = '127.0.0.1'
port = 1244
ThreadCount = 0

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host, port))

clients = set()
recvPackets = queue.Queue()
clients_lock = threading.Lock()
print(clients_lock)

print('Server Running...')

def RecvData(sock, recvPackets):
    while True:
        data, addr = sock.recvfrom(2048)
        
        recvPackets.put((data, addr))

# threading.Thread(target = RecvData,args = (s,recvPackets)).start()
start_new_thread(RecvData, (s, recvPackets))

while True:
    while not recvPackets.empty():
        data, addr = recvPackets.get()
        if addr not in clients:
            print('Connected to: ' + addr[0] + ':' + str(addr[1]))
            clients.add(addr)
            usr_baru = json.loads(data)['nama']
            msg = usr_baru + ' telah bergabung.'
            msg = json.dumps(msg).encode()
            for c in clients:
                if c!=addr:
                    s.sendto(msg,c)
            continue
        clients.add(addr)

        if json.loads(data)['message'] == 'quit':
            usr = json.loads(data)['nama']
            msg = usr + ' telah keluar.'
            msg = json.dumps(msg).encode()
            for c in clients:
                if c!=addr:
                    s.sendto(msg,c)

            clients.remove(addr)
            print(addr[0] + ':' + str(addr[1]) + ' telah keluar.')
            continue

        data = json.loads(data)

        current_time = datetime.now().strftime("%H:%M:%S")
        
        resp = f"{current_time} {data['nama']}: {data['message']}"

        print(resp)
        for c in clients:
            # if c!=addr:
            s.sendto(resp.encode(),c)

# Referensi
# https://realpython.com/python-sockets/