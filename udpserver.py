import socket
import os
import hashlib
type = 'utf-8'
host, port = "172.17.0.2" , 12345 # clients ip address and the port
def send_object(pathlist, host, port):
    dest = (host, port)
    end_sent = False
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(1) #1 saniye geçerse excepte girmesini sağlıyo
        s.connect(dest)
        for ind in range(len(pathlist)):
            header_sent, current_packet, current_packet_sent, state = False, 0, False, 0
            data = read_data(pathlist[ind])
            header = create_header(pathlist[ind])
            packet_count = len(data)
            hash_of_header = compute_sha256(header)
            while not header_sent: #header gönderilene kadar deniyo
                s.sendto(hash_of_header+header, dest)
                print(hash_of_header)
                try:
                    message = s.recv(10).decode(type)
                    print(message)
                    if message == "ACK_HEADER": #ack header gelirse looptan çıkıyo
                        header_sent = True
                except:
                    pass
            while True: #tüm paketleri göndermek için loop
                while not current_packet_sent:  #şuanki paketi onaylamak için loop
                    print("vvvv")
                    hash = compute_sha256(str(state).encode(type) + data[current_packet])
                    s.sendto(str(state).encode(type) + hash + data[current_packet], dest) #paketi gönder
                    try:
                        message = s.recv(10).decode(type)
                        if (message == "ACK_DATA_1" and state == 1) or (message == "ACK_DATA_0" and state == 0): #state ve ack uyuyor mu
                            current_packet_sent = True
                            current_packet += 1 #bi sonraki pakete geç
                            state = 1 - state #state 1se 0 0sa 1 yap
                    except:
                        pass
                if current_packet >= packet_count: #tüm paketler gitti mi kontrolü
                    break
                current_packet_sent = False
        while not end_sent: #tüm dosyalar gitti mi kontrolü
            s.sendto("END".encode(type), dest)
            try:
                message = s.recv(1024).decode(type) #karşıya end gönder ok bekle
                if message == "OK":
                    end_sent = True
            except:
                pass


def create_header(path):
    filename = path[14:]
    bytecount = os.path.getsize(path)
    return (filename + "_" + str(bytecount)).encode(type)


def read_data(path):
    data = []
    with open(path,"rb") as f:
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            data.append(chunk)
    return data

def compute_sha256(data):
    return hashlib.sha256(data).hexdigest().encode(type)
paths = ["/root/objects/large-0.obj","/root/objects/large-1.obj","/root/objects/large-2.obj",
"/root/objects/small-0.obj","/root/objects/small-1.obj","/root/objects/small-2.obj"]
send_object(paths, host, port)

