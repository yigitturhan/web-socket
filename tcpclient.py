# echo-client.py

import socket

host = ""  # empty
port = 12345  # The port specified in server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    print(f"Server listening on {host}:{port}")
    conn, addr = s.accept()
    print(f"Connection established from {addr}")
    with open("received_model.obj", "wb") as f:
        while True:
            chunk = conn.recv(1024)
            if not chunk:
                break
            f.write(chunk)

    print("File received successfully.")
    conn.close()
