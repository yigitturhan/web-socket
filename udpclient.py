import socket
dest = ("", 12345)
type = 'utf-8'
def get_objects(dest):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(dest)
        print(f"Server listening on {dest}")
        while True:
            message, addr = s.recvfrom(1024)
            message = message.decode(type)
            if message == "END":
                break
            fileName, fileSize = message.split('_')
            fileSize = int(fileSize)
            receivedBytes = 0
            s.sendto(b'NO_PROBLEM', addr)
            with open(fileName, "wb") as f:
                while receivedBytes < fileSize:
                    chunk = s.recv(1024)
                    receivedBytes += 1024
                    if not chunk:
                        break
                    f.write(chunk)
            s.sendto(b'RECEIVED',addr)
get_objects(dest)
