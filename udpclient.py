import socket, os, threading, queue, random, json

host = '127.0.0.1'
port = 1244

data = {}


# Input nama
nama = input("Masukkan nama anda: \n")
data['nama'] = nama
data['status'] = "nama"

# Connect Server
server = (host, port)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(f"Koneksi ke {host}:{port} Berhasil!")
s.sendto(json.dumps(data).encode(), server)

# Receive function for threading
def ReceiveData(sock):
    while True:
        try:
            data,addr = sock.recvfrom(2048)
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

    # Quit
    if word == "quit":
        s.close()
        os._exit(1)

s.sendto(data.encode('utf-8'),server)
s.close()