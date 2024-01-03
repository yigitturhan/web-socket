import socket
import os
import hashlib
import time
type = 'utf-8'
host, port = "172.17.0.2" , 12345 # clients ip address and the port
def send_object(pathlist, host, port):
    encoded_pipe = "|".encode(type)
    encoded_ack_header = "ACK_HEADER".encode(type)
    encoded_end_header = "END_HEADER".encode(type)
    encoded_end = "END".encode(type)
    encoded_ok = "OK".encode(type)
    dest, end_sent = (host, port), False
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(1) #1 saniye geçerse excepte girmesini sağlıyo
        s.connect(dest)
        print("Connection established with "+host+" at the port number "+str(port))
        data_list = read_data(pathlist)
        index_list = get_index_list(data_list)
        for ind in range(len(pathlist)):
            header = create_header(pathlist[ind])
            hash_of_header = compute_sha256(header)
            while True: #header gönderilene kadar deniyo
                s.sendto(hash_of_header+header, dest)
                try:
                    message = s.recv(64)
                    if message == encoded_ack_header:
                        break
                except Exception as e:
                    print(e)
        
        while True:
            s.sendto(encoded_end_header, dest)
            try:
                message = s.recv(8)
                if message == encoded_ok:
                    break   
            except:
                pass

        while index_list: #tüm paketleri göndermek için loop
            try:
                packets_to_send, indexes_of_packets, file_names_as_bytes, hashes, hashed_packets, i2 = [], [], [], [], [], 0
                for x,y in index_list[:5]:
                    packets_to_send.append(data_list[x][y])
                    indexes_of_packets.append(str(y).encode(type))
                    file_name_2 = pathlist[x][14:]
                    file_names_as_bytes.append(file_name_2.encode(type))
                    hashes.append(compute_sha256((file_name_2 + "|" + str(y)).encode(type) + encoded_pipe + data_list[x][y]))
                    hashed_packets.append(hashes[i2]+file_names_as_bytes[i2]+encoded_pipe+indexes_of_packets[i2]+encoded_pipe+packets_to_send[i2])
                    i2 += 1
                for packet in hashed_packets:
                    s.sendto(packet, dest)
                for i in range(len(packets_to_send)):
                    message = s.recv(1024)
                    hash = message[:64]
                    ok, rec_filename, rec_index = message[64:].decode(type).split("_") #hash ok_filename_index
                    rec_index = int(rec_index)
                    if ok == "OK" and hash == compute_sha256(("OK_"+ rec_filename+"_"+str(rec_index)).encode(type)):
                        index_list.remove((get_index_of_file(pathlist,rec_filename),rec_index))
            
            except Exception as e:
                print(e)
        while not end_sent: #tüm dosyalar gitti mi kontrolü
            s.sendto(encoded_end, dest)
            try:
                message = s.recv(1024) #karşıya end gönder ok bekle
                if message:
                    end_sent = True
                    print("All files are sent and the connection is closed.")
            except Exception as e:
                print(e)


def create_header(path):
    filename = path[14:]
    bytecount = os.path.getsize(path)
    return (filename + "_" + str(bytecount)).encode(type)

def get_index_of_file(pathlist, file_name):
    for path in pathlist:
        if path[14:] == file_name:
            return pathlist.index(path)
    raise Exception


def read_data(pathlist):
    data = []
    for path in pathlist:
        with open(path,"rb") as f:
            temp = []
            while True:
                chunk = f.read(1024)
                if not chunk:
                    break
                temp.append(chunk)
            data.append(temp)
    return data

def compute_sha256(data):
    return hashlib.sha256(data).hexdigest().encode(type)


def get_index_list(data_list):
    res = [(i,j) for i in range(len(data_list)) for j in range(len(data_list[i]))]
    return res

paths = ["/root/objects/large-0.obj","/root/objects/large-1.obj","/root/objects/large-2.obj",
"/root/objects/small-0.obj","/root/objects/small-1.obj","/root/objects/small-2.obj"]
a = time.time()
send_object(paths, host, port)
print(time.time()-a)

