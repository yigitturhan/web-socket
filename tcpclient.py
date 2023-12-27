# echo-client.py

import socket

host = ""  # empty
port = 12345  # The port specified in server
model_count = 0
def get_large_objects(host, port):
    global model_count
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")
        conn, addr = s.accept()
        print(f"Connection established from {addr}")
        with open("received_model_"+str(model_count)+".obj", "wb") as f:
            while True:
                chunk = conn.recv(1024)
                if not chunk:
                    break
                f.write(chunk)
        model_count += 1
    print("File received successfully.")
    conn.close()

def get_small_objects(host, port):
    global model_count
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")
        conn, addr = s.accept()
        print(f"Connection established from {addr}")
        with open("received_model_"+str(model_count)+".obj", "wb") as f:
            chunk = conn.recv(1024)
            f.write(chunk)
        model_count += 1
    print("File received successfully.")
    conn.close()

get_large_objects(host, port)
get_small_objects(host, port)
