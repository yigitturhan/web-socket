import os
import socket
import time
type = "utf-8"
def send_object(path_list, dest):
    start = time.time()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(dest)
            for path in path_list:
                send_file(s, path)
            s.send(b"END")
            print("Files are sent.")
    except Exception as e:
        print(e)
    end = time.time()
    return end - start

def send_file(s, filePath):
    with open(filePath, "rb") as f:
        fileName = filePath[14:]
        fileSize = os.path.getsize(filePath)
        s.send((fileName+"_"+str(fileSize)).encode(type))
        message = s.recv(10)
        flag = False
        while True:
            try:
                if not flag:
                    chunk = f.read(1024)
                if not chunk:
                    break
                s.sendall(chunk)
                flag = False
            except Exception as e:
                print(e)
                flag = True
                continue
        message = s.recv(8)
host = "172.17.0.2"
port = 12345
dest = (host, port)
send_object(["/root/objects/large-0.obj", "/root/objects/small-0.obj", "/root/objects/large-1.obj", "/root/objects/small-1.obj", 
"/root/objects/large-2.obj", "/root/objects/small-2.obj","/root/objects/large-3.obj", "/root/objects/small-3.obj",
"/root/objects/large-4.obj", "/root/objects/small-4.obj","/root/objects/large-5.obj", "/root/objects/small-5.obj",
"/root/objects/large-6.obj", "/root/objects/small-6.obj","/root/objects/large-7.obj", "/root/objects/small-7.obj",
"/root/objects/large-8.obj", "/root/objects/small-8.obj","/root/objects/large-9.obj", "/root/objects/small-9.obj"], dest)
