import socket, os, threading, queue, random, json

host = '127.0.0.1'
port = 1244

data = {}


# Input nama
nama = input("Masukkan nama anda: \n")
data['nama'] = nama
data['status'] = "nama"

# Connect Server
server = (host, 5000)
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# s.bind((host,port))
print(f"Koneksi ke {host}:{port} Berhasil!")
s.sendto(json.dumps(data).encode(),server)

# Receive function for threading
def ReceiveData(sock):
    while True:
        try:
            data,addr = sock.recvfrom(1024)
            print(data.decode())
        except:
            pass

threading.Thread(target = ReceiveData, args=(s,)).start()

# Send function
while True:
    word = input()
    data['message'] = word
    data['status'] = "message"
    s.sendto(json.dumps(data).encode(),server)

s.sendto(data.encode('utf-8'),server)
s.close()