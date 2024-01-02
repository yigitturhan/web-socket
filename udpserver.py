import socket
import os
import hashlib
type = 'utf-8'
host, port = "172.17.0.2" , 12345 # clients ip address and the port
def send_object(pathlist, host, port):
    dest, end_sent = (host, port), False
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(1) #1 saniye geçerse excepte girmesini sağlıyo
        s.connect(dest)
        print("Connection established with "+host+" at the port number "+str(port))
        data_list = read_data(pathlist)
        index_list = get_index_list(data_list)
        for ind in range(len(pathlist)):
            header_sent = False
            header = create_header(pathlist[ind])
            hash_of_header = compute_sha256(header)
            while not header_sent: #header gönderilene kadar deniyo
                s.sendto(hash_of_header+header, dest)
                try:
                    message = s.recv(64).decode(type)
                    if message == "ACK_HEADER":
                        header_sent = True
                except Exception as e:
                    print(e)     

        while index_list: #tüm paketleri göndermek için loop
            packets_to_send = [data_list[x][y] for x,y in index_list[:5]]
            hashes = [compute_sha256((pathlist[x][14:] + str(y)).encode(type) + data_list[x][y]) for x,y in index_list[:5]]
            hashed_packets = [hashes[i]+packets_to_send[i]]
            hash = compute_sha256(data_to_hashed)
                    data_to_send = hash + ("|" + pathlist[ind][14:] + "|" +  str(current_packet)).encode(type) + data[current_packet]#hash, dosya adı, index, data
                    s.sendto(data_to_send, dest) #paketi gönder
                    try:
                        message = s.recv(128)
                        hash, ack, received_filename, received_index = message.decode(type)[:64], message.decode(type)[64:].split("|")
                        if compute_sha256((received_filename+received_index).encode(type)) == hash:

                    except Exception as e:
                        print(e)
                if current_packet >= packet_count: #tüm paketler gitti mi kontrolü
                    print("Packet with name " + str(pathlist[ind][14:]) +" is sent.")
                    break
                current_packet_sent = False
        while not end_sent: #tüm dosyalar gitti mi kontrolü
            s.sendto("END".encode(type), dest)
            try:
                message = s.recv(1024).decode(type) #karşıya end gönder ok bekle
                if message == "OK":
                    end_sent = True
                    print("All files are sent and the connection is closed.")
            except Exception as e:
                print(e)


def create_header(path):
    filename = path[14:]
    bytecount = os.path.getsize(path)
    return (filename + "_" + str(bytecount)).encode(type)


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
            data.append(path)
    return data

def compute_sha256(data):
    return hashlib.sha256(data).hexdigest().encode(type)



def get_index_list(data_list):
    res = []
    for i in range(len(data_list)):
        for j in range(len(i)):
            res.append((i,j))
    return res

paths = ["/root/objects/large-0.obj","/root/objects/large-1.obj","/root/objects/large-2.obj",
"/root/objects/small-0.obj","/root/objects/small-1.obj","/root/objects/small-2.obj"]
send_object(paths, host, port)

