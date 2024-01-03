# echo-client.
import socket
import time
host, port,type = "", 12345, "utf-8"
def get_objects(dest):
    start = time.time()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(dest)
        s.listen()
        conn, addr = s.accept()
        while True:
            message = conn.recv(20).decode
            message = message.decode(type)
            if message == "END":
                break
            fileName, fileSize = message.split("_")
            fileSize, received_bytes = int(fileSize), 0
            conn.send(b"NO_PROBLEM")
            with open(fileName, "wb") as f:
                while received_bytes < fileSize:
                    chunk = conn.recv(1024)
                    received_bytes += len(chunk)
                    f.write(chunk)
            conn.send(b"RECEIVED")
            print(fileName, " received.")
    end = time.time()
    return end - start
        
dest = (host, port)
print(get_objects(dest))


