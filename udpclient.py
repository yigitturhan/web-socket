import socket
dest = ("", 12345)
type = 'utf-8'
def get_objects(dest):
    g = 0
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(dest)
        while True:
            
            header_received, state = False, 0
            while not header_received: #header ı alma loopu
                message, addr = s.recvfrom(1024)
                message = message.decode(type) #header endse tüm filelar gelmiş demek
                if message == "END":
                    s.sendto("OK".encode(type), addr) #işlem bitmişse ok gönder
                    return
                try:
                    fileName, fileSize = message.split('_') #filename ve size çek
                    fileSize, receivedBytes = int(fileSize), 0
                    s.sendto("ACK_HEADER".encode(type), addr) #filename ve size ı çekebiliyosa ack header gönder
                    header_received = True #looptan çık
                except:
                    pass
            with open(fileName, "wb") as f: #dosyaya yazma
                while receivedBytes < fileSize: #tüm paketleri bekle
                    message = s.recv(1025) #mesaj al
                    if message[0] != state + 48:
                        s.sendto(("ACK_DATA_" + str(state)).encode(type), addr)
                        continue
                    if not message:
                        break
                    f.write(message[1:])
                    s.sendto(("ACK_DATA_" + str(state)).encode(type), addr) #ack 0 ya da 1 gönder (state e göre)
                    receivedBytes += 1024 #güncelle ki looptan çıksın
                    state = 1 - state #state değiştirme

get_objects(dest)
