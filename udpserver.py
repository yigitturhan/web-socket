# echo-server.py
import socket
def send_large_object(path, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        with open(path, "rb") as f:
            while True:
                chunk = f.read(1024)
                if not chunk:
                    break
                s.sendto(chunk, (host,port))
        print("Large Object Sent Successfully")

def send_small_object(path,host,port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        with open(path, "rb") as f:
            chunk = f.read(1024)
            s.sendto(chunk , (host, port))
        print("Small Object Sent Successfully")

host = "172.17.0.3"  # clients ip address
port = 12345  # The port used by the server

path_of_large_obj = "/root/objects/large-0.obj"

send_large_object(path_of_large_obj, host, port)

path_of_small_object = "root/objects/small-0.obj"

send_small_objects(path_of_small_object, host, port)
