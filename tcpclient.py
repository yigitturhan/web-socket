# echo-client.py

import socket

host = ""  # empty
port = 12345  # The port specified in server


def get_objects(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")
        conn, addr = s.accept()
        print(f"Connection established from {addr}")

        message = s.recv(1024)
        message = message.decode('utf-8')
        fileName, fileSize = message.split('_')
        fileSize = int(fileSize)
        receivedBytes = 0
        s.sendall(b'NO_PROBLEM')
        with open(fileName, "wb") as f:
            while receivedBytes < fileSize:  # !!!!
                chunk = conn.recv(1024)
                receivedBytes += 1024
                if not chunk:
                    break
                f.write(chunk)

        message = s.recv(1024)
        message = message.decode('utf-8')
        fileName, fileSize = message.split('_')
        fileSize = int(fileSize)
        receivedBytes = 0
        s.sendall(b'NO_PROBLEM')

        with open(fileName, "wb") as f:
            while receivedBytes < fileSize:  # !!!!
                chunk = conn.recv(1024)
                receivedBytes += 1024
                if not chunk:
                    break
                f.write(chunk)
    print("File received successfully.")
    conn.close()


get_objects(host, port)
