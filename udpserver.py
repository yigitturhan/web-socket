import socket
import os
type = 'utf-8'
def send_object(pathlist, host, port):
    dest = (host, port)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(dest)
            for path in pathlist:
                with open(path, "rb") as f:
                    s.sendto(create_header(path), dest)
                    s.recv(10)  # karşıdan mesaj al
                    while True:
                        chunk = f.read(1024)
                        if not chunk:
                            break
                        s.sendto(chunk, dest)
                s.recv(8)
                print("Object Sent Successfully")
            s.sendto("END".encode(type),dest)
    except:
        print("ERROR OCCURED")

def create_header(path):
    filename = path[14:]
    bytecount = os.path.getsize(path)
    return (filename + "_" + str(bytecount)).encode(type)

host = "172.17.0.3"  # clients ip address
port = 12345  # The port used by the server
paths = ["/root/objects/large-0.obj","/root/objects/large-1.obj","/root/objects/small-0.obj",
"/root/objects/large-2.obj","/root/objects/large-3.obj","/root/objects/small-1.obj"]
send_object(paths, host, port)
