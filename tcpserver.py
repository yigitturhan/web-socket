import os
import socket
import time

def send_object(path_list host, port):
    start = time.time()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host,port))
            for path in path_list:
                send_file(s, path)
            print("sent")
    except Exception as e:
        print(e)
    end = time.time()
    print(end-start)

def send_file(s, filePath):
    with open(filePath, "rb") as f:
        fileName = filePath[14:]
        fileSize = os.path.getsize(filePath)
        s.send((fileName+"_"+str(fileSize)).encode('utf-8'))
        message = s.recv(10)
        print(message)
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
        s.send(b"bitti")
        message = s.recv(8)
        print(message)

host = "172.17.0.2"
port = 12345
send_object(["/root/objects/large-0.obj", "/root/objects/small-0.obj", "/root/objects/large-1.obj", "/root/objects/small-1.obj", 
"/root/objects/large-2.obj", "/root/objects/small-2.obj"], host, port)
