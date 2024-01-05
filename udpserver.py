import socket
import os
import hashlib
import time
type = 'utf-8'
host, port = "172.17.0.2" , 12345 # clients ip address and the port
def send_object(pathlist, host, port):
    start = time.time()
    encoded_pipe = "|".encode(type)
    encoded_ack_header = "ACK_HEADER".encode(type)
    encoded_end_header = "END_HEADER".encode(type)
    encoded_end_header_hash = compute_sha256(encoded_end_header)
    encoded_ack_header_hash = compute_sha256(encoded_ack_header)
    encoded_end = "END".encode(type)
    encoded_ok = "OK".encode(type)
    encoded_end_hash = compute_sha256(encoded_end)
    encoded_ok_hash = compute_sha256(encoded_ok)
    dest, end_sent = (host, port), False
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        rtt_sum, rtt_count = 0, 0
        while rtt_count < 10:
            rtt = calculate_rtt(s,dest,encoded_ok,encoded_pipe)
            if rtt != 0:
                rtt_sum += rtt
                rtt_count +=1
        rtt = rtt_sum / rtt_count
        if rtt < 0.001:
            rtt = 0.001
        s.settimeout(0.3) #1 saniye geçerse excepte girmesini sa�~_lıyo
        s.connect(dest)
        data_list = read_data(pathlist)
        index_list = get_index_list(data_list)
        header_to_sent = create_one_header_with_hash(pathlist, encoded_pipe)
        while True:
            s.sendto(header_to_sent, dest)
            try:
                message = s.recv(1024)
                print(encoded_ack_header_hash + encoded_ack_header)
                if message == encoded_ack_header_hash + encoded_ack_header:
                    break
            except:
                pass
        s.settimeout(rtt)
        for _ in range(20)
            s.sendto(encoded_end_header_hash + encoded_end_header, dest)
            try:
                message = s.recv(128) #hashli gelsin
                hash_mes = message[:64]
                if hash_mes == encoded_ok_hash and message[64:] == encoded_ok:
                    break
            except:
                pass
        while index_list: #tüm paketleri göndermek için loop
            try:
                #packets_to_send, indexes_of_packets, file_names_as_bytes, hashes, hashed_packets, i2 = [], [], [], [], [], 0
                for x,y in index_list:
                    packets_to_send = data_list[x][y]
                    indexes_of_packets = str(y).encode(type)
                    file_name_2 = pathlist[x][14:]
                    file_names_as_bytes = file_name_2.encode(type)
                    hashes = compute_sha256((file_name_2 + "|" + str(y)).encode(type) + encoded_pipe + data_list[x][y])
                    hashed_packets = hashes+file_names_as_bytes+encoded_pipe+indexes_of_packets+encoded_pipe+packets_to_send
                    s.sendto(hashed_packets, dest)
                for i in range(len(index_list)):
                    message = s.recv(1024)
                    hash = message[:64]
                    ok, rec_filename, rec_index = message[64:].decode(type).split("_") #hash ok_filename_index
                    rec_index = int(rec_index)
                    if ok == "OK" and hash == compute_sha256(("OK_"+ rec_filename+"_"+str(rec_index)).encode(type)):
                        try:
                            index_list.remove((get_index_of_file(pathlist,rec_filename),rec_index))
                        except:
                            pass

            except Exception as e:
                print(e)
        for _ in range(15) #tüm dosyalar gitti mi kontrol
            s.sendto(encoded_end_hash + encoded_end, dest)
            try:
                message = s.recv(1024) #kar�~_ıya end gönder ok b
                hash_mes = message[:64]
                if hash_mes == encoded_ok_hash:
                    s.sendto(encoded_end_hash + encoded_end,dest)
                    break
            except Exception as e:
                print(e)
    end = time.time()
    return end - start

def create_header(path):
    filename = path[14:]
    bytecount = os.path.getsize(path)
    return (filename + "_" + str(bytecount)).encode(type)

def get_index_of_file(pathlist, file_name):
    for path in pathlist:
        if path[14:] == file_name:
            return pathlist.index(path)
    raise Exception

def create_one_header_with_hash(pathlist, encoded_pipe):
    paths = bytearray()
    for index, path in enumerate(pathlist):
        paths.extend(create_header(path))
        if index != len(pathlist) -1:
            paths.extend(encoded_pipe)
    result = bytes(paths)
    hash = compute_sha256(result)
    return hash+result



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
def calculate_rtt(s, dest, encoded_ok, encoded_pipe):
    s.settimeout(0.3)
    a, b = 0, 0
    s.sendto(encoded_pipe,dest)
    try:
        a = time.time()
        s.recv(10)
        b = time.time()
        return b-a
    except:
        return 0

paths= ["/root/objects/large-0.obj","/root/objects/large-1.obj","/root/objects/large-2.obj",
"/root/objects/large-3.obj","/root/objects/large-4.obj","/root/objects/large-5.obj",
"/root/objects/large-6.obj","/root/objects/large-7.obj","/root/objects/large-8.obj",
"/root/objects/large-9.obj","/root/objects/small-0.obj","/root/objects/small-1.obj",
"/root/objects/small-2.obj","/root/objects/small-3.obj","/root/objects/small-4.obj",
"/root/objects/small-5.obj","/root/objects/small-6.obj","/root/objects/small-7.obj",
"/root/objects/small-8.obj","/root/objects/small-9.obj"]
print(send_object(paths, host, port))

        