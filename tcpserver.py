# echo-server.py
import socket

host = "172.17.0.3"  # clients ip address
port = 12345  # The port used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    with open("/root/objects/large-0.obj", "rb") as f:
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            s.sendall(chunk)

    print("File sent successfully.")
