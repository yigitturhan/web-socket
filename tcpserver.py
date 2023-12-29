# echo-server.py
import socket
from . import util  # utils  mi util mi


def send_large_object(path, host, port):

    fileName = path[14:]
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(fileName)

        with open(path, "rb") as f:
            while True:
                chunk = f.read(1024)
                if not chunk:
                    break
                s.sendall(chunk)
        print("Large Object Sent Successfully")


def send_small_object(path, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        with open(path, "rb") as f:
            chunk = f.read(1024)
            s.sendall(chunk)
        print("Small Object Sent Successfully")


host = "172.17.0.3"  # clients ip address
port = 12345  # The port used by the server

path_of_large_obj = "/root/objects/large-0.obj"

send_large_object(path_of_large_obj, host, port)

path_of_small_object = "/root/objects/small-0.obj"

send_small_objects(path_of_small_object, host, port)
