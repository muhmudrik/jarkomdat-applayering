import socket, os, threading, queue
from datetime import datetime

host = '127.0.0.1'
port = 1244
ThreadCount = 0

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host, port))

clients = set()
recvPackets = queue.Queue()
clients_lock = threading.Lock()
print(clients_lock)

def RecvData(sock, recvPackets):
    # print("Accepted connection from: ", address)
    # with clients_lock:
    #     clients.add(client)
    #     print(clients)
    while True:
        data,addr = sock.recvfrom(1024)

        recvPackets.put((data,addr))

print('Server Running...')

threading.Thread(target=RecvData,args=(s,recvPackets)).start()

while True:
    while not recvPackets.empty():
        data,addr = recvPackets.get()
        if addr not in clients:
            clients.add(addr)
            continue
        clients.add(addr)
        # data = data.decode('utf-8')
        # if data.endswith('qqq'):
        #     clients.remove(addr)
        #     continue

        current_time = datetime.now().strftime("%H:%M:%S")
        
        resp = f"{current_time} {data['nama']}: {data['message']}"

        print(str(addr)+resp)
        for c in clients:
            # if c!=addr:
            s.sendto(resp.encode(),c)