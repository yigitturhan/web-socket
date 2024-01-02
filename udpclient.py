import socket
import hashlib
dest = ("", 12345)
type = 'utf-8'
def get_objects(dest):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(dest)
        while True:
            header_received, state = False, 0
            while not header_received: #header ı alma loopu
                message, addr = s.recvfrom(1024)
                hash, header = message[:64], message[64:]
                message = message.decode(type) #header endse tüm filelar gelmiş demek
                if message == "END":
                    s.sendto("OK".encode(type), addr) #işlem bitmişse ok gönder
                    return
                try:
                    if compute_sha256(header) != hash:
                        s.sendto("NACKHEADER".encode(type), addr) 
                        continue
                    fileName, fileSize = message.split('_') #filename ve size çek
                    fileName, fileSize, receivedBytes =  fileName[64:], int(fileSize), 0
                    s.sendto("ACK_HEADER".encode(type), addr) #filename ve size ı çekebiliyosa ack header gönder
                    header_received = True #looptan çık
                except:
                    pass
            with open(fileName, "wb") as f: #dosyaya yazma
                while receivedBytes < fileSize: #tüm paketleri bekle
                    message = s.recv(1089) #mesaj al
                    hash, data = message[1:65], message[65:]
                    if message[0] != state + 48 or hash != compute_sha256(str(message[0]-48).encode(type) + data):
                        s.sendto(("ACK_DATA_" + str(state)).encode(type), addr)
                        continue
                    if not message:
                        break
                    f.write(data)
                    s.sendto(("ACK_DATA_" + str(state)).encode(type), addr) #ack 0 ya da 1 gönder (state e göre)
                    receivedBytes += 1024 #güncelle ki looptan çıksın
                    state = 1 - state #state değiştirme
def compute_sha256(data):
    return hashlib.sha256(data).hexdigest().encode(type)
get_objects(dest)
