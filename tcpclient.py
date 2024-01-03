# echo-client.py

import socket
import time
host = ""  # empty
port = 12345  # The port specified in server
a = 0

def get_objects(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        global a
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")
        conn, addr = s.accept()
        a = time.time()
        print(f"Connection established from {addr}")
        message = conn.recv(1024)
        message = message.decode('utf-8')
        fileName, fileSize = message.split('_')
        fileSize = int(fileSize)
        receivedBytes = 0
        conn.send(b'NO_PROBLEM')
        flag = True
        with open(fileName, "wb") as f:
            while receivedBytes < fileSize:  # !!!!
                chunk = conn.recv(1024)
                if chunk == b"done":
                    flag = False
                    break
                receivedBytes += 1024
                if not chunk:
                    break
                f.write(chunk)
        if flag:
            message = conn.recv(20)
            print(message)
        conn.send(b'RECEIVED')
        message = conn.recv(1024)
        message = message.decode('utf-8')
        fileName, fileSize = message.split('_')
        fileSize = int(fileSize)
        receivedBytes = 0
        conn.send(b'NO_PROBLEM')
        with open(fileName, "wb") as f:
            while fileSize > receivedBytes: # !!!!
                chunk = conn.recv(1024)
                receivedBytes += 1024
                if not chunk:
                    break
                f.write(chunk)
    print("File received successfully.")
    conn.send(b'RECEIVED')
    conn.close()

get_objects(host, port)
print(time.time()-a)