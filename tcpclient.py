# echo-client.
import socket
import time
host, port,a = "", 12345, 0
def get_objects(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        global a
        s.bind((host,port))
        s.listen()
        conn, addr = s.accept()
        a = time.time()
        message = conn.recv(20)
        message = message.decode('utf-8')
        print(message)
        fileName, fileSize = message.split("_")
        fileSize, received_bytes = int(fileSize), 0
        conn.send(b"NO_PROBLEM")
        flag, last_byte = True, 0
        with open(fileName, "wb") as f:
            while received_bytes < fileSize:
                chunk = conn.recv(1024)
                last_byte = chunk[-5:]
                if last_byte == b"bitti":
                    flag = False
                    break
                received_bytes += len(chunk)
                f.write(chunk)
        print("çiktim")
        if flag and last_byte != b"bitti":
            message = conn.recv(5)
            print(message)
        print("file received")
        conn.send(b"RECEIVED")
        message = conn.recv(20)
        message = message.decode('utf-8')
        print(message)
        fileName, fileSize = message.split("_")
        fileSize, received_bytes = int(fileSize), 0
        conn.send(b"NO_PROBLEM")
        flag, last_byte = True, 0
        with open(fileName, "wb") as f:
            while received_bytes < fileSize:
                chunk = conn.recv(1024)
                last_byte = chunk[-5:]
                if last_byte == b"bitti":
                    flag = False
                    break
                received_bytes += len(chunk)
                f.write(chunk)
        print("çiktim")
        if flag and last_byte != b"bitti":
            message = conn.recv(5)
            print(message)
        print("file received")
        conn.send(b"RECEIVED")
        message = conn.recv(20)
        message = message.decode('utf-8')
        print(message)
        fileName, fileSize = message.split("_")
        fileSize, received_bytes = int(fileSize), 0
        conn.send(b"NO_PROBLEM")
        flag, last_byte = True, 0
        with open(fileName, "wb") as f:
            while received_bytes < fileSize:
                chunk = conn.recv(1024)
                last_byte = chunk[-5:]
                if last_byte == b"bitti":
                    flag = False
                    break
                received_bytes += len(chunk)
                f.write(chunk)
        print("çiktim")
        if flag and last_byte != b"bitti":
            message = conn.recv(5)
            print(message)
        print("file received")
        conn.send(b"RECEIVED")
        message = conn.recv(20)
        message = message.decode('utf-8')
        print(message)
        fileName, fileSize = message.split("_")
        fileSize, received_bytes = int(fileSize), 0
        conn.send(b"NO_PROBLEM")
        flag, last_byte = True, 0
        with open(fileName, "wb") as f:
            while received_bytes < fileSize:
                chunk = conn.recv(1024)
                last_byte = chunk[-5:]
                if last_byte == b"bitti":
                    flag = False
                    break
                received_bytes += len(chunk)
                f.write(chunk)
        print("çiktim")
        if flag and last_byte != b"bitti":
            message = conn.recv(5)
            print(message)
        print("file received")
        conn.send(b"RECEIVED")
        message = conn.recv(20)
        message = message.decode('utf-8')
        print(message)
        fileName, fileSize = message.split("_")
        fileSize, received_bytes = int(fileSize), 0
        conn.send(b"NO_PROBLEM")
        flag, last_byte = True, 0
        with open(fileName, "wb") as f:
            while received_bytes < fileSize:
                chunk = conn.recv(1024)
                last_byte = chunk[-5:]
                if last_byte == b"bitti":
                    flag = False
                    break
                received_bytes += len(chunk)
                f.write(chunk)
        print("çiktim")
        if flag and last_byte != b"bitti":
            message = conn.recv(5)
            print(message)
        print("file received")
        conn.send(b"RECEIVED")
        message = conn.recv(20)
        message = message.decode('utf-8')
        print(message)
        fileName, fileSize = message.split("_")
        fileSize, received_bytes = int(fileSize), 0
        conn.send(b"NO_PROBLEM")
        flag, last_byte = True, 0
        with open(fileName, "wb") as f:
            while received_bytes < fileSize:
                chunk = conn.recv(1024)
                last_byte = chunk[-5:]
                if last_byte == b"bitti":
                    flag = False
                    break
                received_bytes += len(chunk)
                f.write(chunk)
        print("çiktim")
        if flag and last_byte != b"bitti":
            message = conn.recv(5)
            print(message)
        print("file received")
        conn.send(b"RECEIVED")

get_objects(host, port)
print(time.time()-a)


