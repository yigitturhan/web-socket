import socket
import hashlib
import time
dest = ("", 12345)
type = 'utf-8'
def get_objects(dest):
    start = time.time()
    encoded_ok = "OK".encode(type)
    encoded_end_header = "END_HEADER".encode(type)
    encoded_end_header_hash = compute_sha256(encoded_end_header)
    encoded_nack_header = "NACKHEADER".encode(type)
    encoded_ack_header = "ACK_HEADER".encode(type)
    encoded_ack_header_hash = compute_sha256(encoded_ack_header)
    encoded_nack_header_hash = compute_sha256(encoded_nack_header)
    encoded_end = "END".encode(type)
    encoded_end_hash = compute_sha256(encoded_end)
    encoded_ok_hash = compute_sha256(encoded_ok)
    encoded_pipe = "|".encode(type)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(dest)
        file_names, files = [], []
        while True:
            message, addr = s.recvfrom(1024)
            hash = message[:64]
            message = message[64:]
            print("Connection established from ", addr[0])
            if hash == encoded_end_header_hash:
                print("ciktim")
                s.sendto(encoded_ok_hash+encoded_ok, addr) #i�~_lem bitmi�~_se ok gönder
                break
            try:
                data = message.decode(type) #header endse tüm filelar gelmi�~_ deme
                if compute_sha256(message) != hash:
                    s.sendto(encoded_nack_header_hash+encoded_nack_header, addr)
                    continue
                fileName, fileSize = data.split('_') #filename ve size çek
                fileSize = int(fileSize)
                if fileName not in file_names:
                    file_names.append(fileName)
                    files.append([False]*ceil(fileSize,1024))
                s.sendto(encoded_ack_header_hash+encoded_ack_header, addr) #filename ve size ı çekebiliyosa ack header gönder
            except:
                s.sendto(encoded_ok_hash+encoded_ok, addr)
        while True: #tüm paketleri bekle
            message = s.recv(1250) #mesaj al
            hash = message[:64]
            if hash == encoded_end_hash:
                s.sendto(encoded_ok_hash+encoded_ok, addr)
                print("All files are received")
                break
            try:
                a,b,c = message[64:].decode(type).split("|")
            except:
                continue
            file_name, index, data = message[64:].decode(type).split("|")
            print(index)
            data, index = data.encode(type), int(index)
            if compute_sha256(file_name.encode(type)+encoded_pipe+str(index).encode(type)+encoded_pipe+data) == hash:
                files[file_names.index(file_name)][index] = data
                ack_data = ("OK_"+file_name+"_"+str(index)).encode(type)
                hash_of_ack = compute_sha256(ack_data)
                s.sendto(hash_of_ack+ack_data, addr)
        print("ciktim ben")
        write_files(file_names, files)
    end = time.time()
    return end - start



def compute_sha256(data):
    return hashlib.sha256(data).hexdigest().encode(type)

def ceil(num, divider):
    if num//divider == num/divider:
        return num//divider
    return num//divider + 1

def write_files(file_names, file_data):
    for i in range(len(file_names)):
        with open(file_names[i],"wb") as f:
            for data in file_data[i]:
                f.write(data)

def check_continue(lst):
    for el in lst:
        if False in l:
            return True
    return False


print(get_objects(dest))
              

