import socket
import os
import time

def send_object(pathLarge, pathSmall, host, port):
    start = time.time()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            
            # Sending large file
            send_file(s, pathLarge)
            s.send(b"done")
            message = s.recv(20)
            print(message)
            
            # Sending small file
            send_file(s, pathSmall)
            message = s.recv(20)
            print(message)

            
            print("Objects Sent Successfully")
            
    except Exception as e:
        print(f"ERROR OCCURRED: {e}")
    
    end = time.time()
    print("Time taken:", end - start)

def send_file(s, filePath):
    with open(filePath, "rb") as f:
        fileName = filePath[14:]
        fileSize = os.path.getsize(filePath)
        s.send((f"{fileName}_{fileSize}").encode('utf-8'))
        message = s.recv(10)  # receive acknowledgment
        print(message)
        flag = False
        current_chunk = 0
        while True:
            try:
                if not flag:
                    chunk = f.read(1024)
                if not chunk:
                    break
                s.sendall(chunk)
                flag = False
            except Exception as e:
                print(f"Error sending chunk: {e}. Retrying with the next chunk...")
                flag = True
                continue
            
        s.recv(8)  # receive final acknowledgment
send_object("/root/objects/large-0.obj", "/root/objects/small-0.obj", "172.17.0.2", 12345)