# echo-server.py
import socket
import time
import os

def send_object(pathLarge, pathSmall, host, port):
    start = time.time()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            with open(pathLarge, "rb") as f:
                fileName = pathLarge[14:]
                largeBytes = os.path.getsize(pathLarge)
                largeBytes = str(largeBytes)
                s.send((fileName+"_"+largeBytes).encode('utf-8'))
                message = s.recv(10)  # karşıdan mesaj al
                while True:
                    chunk = f.read(1024)
                    if not chunk:
                        break
                    s.sendall(chunk)
            s.recv(8)
            with open(pathSmall, "rb") as f:
                fileName = pathSmall[14:]
                smallBytes = os.path.getsize(pathSmall)
                smallBytes = str(smallBytes)
                s.send((fileName+"_"+smallBytes).encode('utf-8'))
                print(fileName+"_"+smallBytes)
                message = s.recv(10)  # karşıdan mesaj al
                while True:
                    chunk = f.read(1024)
                    if not chunk:
                        break
                    s.sendall(chunk)
            s.recv(8)
            print("Objects Sent Successfully")
    except:
        print("ERROR OCCURED")
    end = time.time()
    print(end - start)


host = "172.17.0.3"  # clients ip address
port = 12345  # The port used by the server
path_of_large_object = "/root/objects/large-0.obj"
path_of_small_object = "/root/objects/small-0.obj"
send_object(path_of_large_object, path_of_small_object, host, port)
