import socket
import hashlib
dest = ("", 12345)
type = 'utf-8'
def get_objects(dest):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(dest)
        file_names, files = [], []
        while True:
            message, addr = s.recvfrom(1024)
            if message.decode(type) == "END_HEADER":
                s.sendto("OK".encode(type), addr) #işlem bitmişse ok gönder
                break
            try:
                hash, header = message[:64], message[64:]
                data = message[64:].decode(type) #header endse tüm filelar gelmiş demek
                if compute_sha256(header) != hash:
                    s.sendto("NACKHEADER".encode(type), addr) 
                    continue
                fileName, fileSize = data.split('_') #filename ve size çek
                fileSize = int(fileSize)
                if fileName not in file_names:
                    file_names.append(fileName)
                    files.append([False]*ceil(fileSize,1024))
                else:
                    s.sendto("NACKHEADER".encode(type), addr) 
                    continue
                s.sendto("ACK_HEADER".encode(type), addr) #filename ve size ı çekebiliyosa ack header gönder
            except:
                pass


            
            while check_continue(files): #tüm paketleri bekle
                message = s.recv(2048) #mesaj al
                hash, file_name, index, data = message.decode(type).split("|")
                hash, data, index = hash.encode(type), data.encode(type), int(index)
                if compute_sha256(data) == hash:
                    if files[file_names.index(file_name)][index] == False:
                        files[file_names.index(file_name)][index] = data
                        ack_data = ("ACK|"+file_name+"|"+str(index)).encode(type)
                        hash_of_ack = compute_sha256(ack_data)
                        s.sendto(hash_of_ack+ack_data, addr)




        
def compute_sha256(data):
    return hashlib.sha256(data).hexdigest().encode(type)

def ceil(num, divider):
    if num//divider == num/divider:
        return num//divider
    return num//divider + 1

def write_files(file_names, file_data):
    for name in file_names:
        with open(name,"wb") as f:
            for data in file_data:
                f.write(data)

def check_continue(lst):
    for el in lst:
        if False in l:
            return True
    return False


get_objects(dest)
