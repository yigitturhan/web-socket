import socket
import os
import hashlib
import time
type = 'utf-8'
host, port = "172.17.0.2" , 12345 # clients ip address and the port number
def send_object(pathlist, host, port):
    start = time.time() #starting time to calculate total time to send 20 files
    encoded_pipe = "|".encode(type)#precalculation of some values. from here to --
    encoded_ack_header = "ACK_HEADER".encode(type)
    encoded_end_header = "END_HEADER".encode(type)
    encoded_end_header_hash = compute_sha256(encoded_end_header)
    encoded_ack_header_hash = compute_sha256(encoded_ack_header)
    encoded_end = "END".encode(type)
    encoded_ok = "OK".encode(type)
    encoded_end_hash = compute_sha256(encoded_end)
    encoded_ok_hash = compute_sha256(encoded_ok)#here
    dest = (host, port) #the destination address for packets
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(dest)
        rtt_sum, rtt_count = 0, 0 #two value one for summation of example rtts the other is for while loop
        while rtt_count < 2: #get two rtt value
            rtt = calculate_rtt(s,dest,encoded_ok,encoded_pipe)
            if rtt != 0: #if the function above returns 0, that means an error occured like timeout. just ignore it. If not 0 make the calculations
                rtt_sum += rtt
                rtt_count +=1
        rtt = rtt_sum / 2 #average of the gathered rtt information
        if rtt < 0.01: #if the rtt is below 0.01 set it to 0.01. This value is gathered during experiments. Making timeout below that value does not make significant change
            rtt = 0.01
        s.settimeout(rtt) #1 saniye geçerse excepte girmesini sa�~_lıyo
        data_list = read_data(pathlist) # the list for all data of 20 files
        index_list = get_index_list(data_list) #the list to store indexes. please look at note 6 on information about code part at report
        header_to_sent = create_one_header_with_hash(pathlist, encoded_pipe) #gathering all the header together. please look at note 3 for more information
        while True: #a while loop to send header
            s.sendto(header_to_sent, dest)
            try:
                message = s.recv(1024)
                if message == encoded_ack_header_hash + encoded_ack_header: #if encoded ack header signal received break the loop. this means client get the header
                    break
            except:
                pass
        for _ in range(5) #this loop is for safety. in a packet loss situation without this loop there might be some stuck at code
            s.sendto(encoded_end_header_hash + encoded_end_header, dest) #sending encoded end header is for telling the client that header part is finished
            try:
                message = s.recv(128) #hashli gelsin
                if message[:64] == encoded_ok_hash and message[64:] == encoded_ok: #if ok is received that means client get the message
                    break
            except: #all of the except pass blocks are for timeout errors.
                pass
        while index_list: #this loop sends all packets of 20 files
            try:
                length = 0
                for x,y in index_list: #get the indexes from index list. use that index at the beginning of the packets, please check note 7 on report
                    length += 1 #for the loop below
                    packet_to_send = data_list[x][y] #get the data from the data_list
                    index_of_packet = str(y).encode(type) #make the index a byte-like object to send
                    file_name_2 = pathlist[x][14:] #get the filename whose data we are transferring
                    file_name_as_bytes = file_name_2.encode(type) #make the file name byte-like object
                    hash = compute_sha256((file_name_2 + "|" + str(y)).encode(type) + encoded_pipe + data_list[x][y]) #bring them all together and calculate the hash. please look at note 2 at report
                    hashed_packet = hash+file_name_as_bytes+encoded_pipe+index_of_packet+encoded_pipe+packet_to_send #bring the hash and other values and create a byte-like object to send
                    s.sendto(hashed_packet, dest) #sending the packet part
                for i in range(length): #for all the packets that are sent, try to get an ack
                    message = s.recv(1024)
                    hash = message[:64]#retrieve the hash and
                    ok, rec_filename, rec_index = message[64:].decode(type).split("_") #retrieve the other data from arriving packet
                    rec_index = int(rec_index) #make the index integer in order to use
                    if ok == "OK" and hash == compute_sha256(("OK_"+ rec_filename+"_"+str(rec_index)).encode(type)): #if hash and message is ok, which means no corruption at packet
                        try:
                            index_list.remove((get_index_of_file(pathlist,rec_filename),rec_index))#get the index and delete this index from index_list. this means the data on that index is sent and no need to retransmission
                        except:#(for comment above) if there are some indexes at the list still, which means not ACKed, continue the loop (line 50)
                            pass
            except:
                pass
        for _ in range(5) #send a signal for receiver to let it know everything is sent. this loop is here because of the same reason with the loop at line 42
            s.sendto(encoded_end_hash + encoded_end, dest) #send encoded end hash. receiver will extract it and understand files are received
            try:
                message = s.recv(1024) #waiting for an ok message from receiver
                if message[:64] == encoded_ok_hash:
                    s.sendto(encoded_end_hash + encoded_end,dest)
                    break
            except
                pass:
    end = time.time()
    return end - start

def create_header(path):
    filename = path[14:] #remove the /root/objects/ part from the path
    bytecount = os.path.getsize(path) #get the bytecount
    return (filename + "_" + str(bytecount)).encode(type) #concatenate them with - in between then encode to send

def get_index_of_file(pathlist, file_name): #a function that gets pathlist and file name than returns the index
    for path in pathlist:
        if path[14:] == file_name:
            return pathlist.index(path)
    raise Exception

def create_one_header_with_hash(pathlist, encoded_pipe): #a function that creates just one header with using create_header function, brings 20 result together
    paths = bytearray()
    for index, path in enumerate(pathlist):
        paths.extend(create_header(path))
        if index != len(pathlist) -1:
            paths.extend(encoded_pipe)
    result = bytes(paths)
    hash = compute_sha256(result)
    return hash+result


def read_data(pathlist): #just a function to read data of the files. it return a list of list of byte-like objects
    data = []
    for path in pathlist:
        with open(path,"rb") as f:
            temp = []
            while True:
                chunk = f.read(1024)
                if not chunk:
                    break
                temp.append(chunk)
            data.append(temp)
    return data

def compute_sha256(data): #computing hash. 
    return hashlib.sha256(data).hexdigest().encode(type)


def get_index_list(data_list): #making the index list. the result will be in form [(0,0),(0,1).....]
    res = [(i,j) for i in range(len(data_list)) for j in range(len(data_list[i]))]
    return res
def calculate_rtt(s, dest, encoded_ok, encoded_pipe): #function to calculate rtt. sends a message and gets the result. then returns the time between those actions
    s.settimeout(0.3)
    s.sendto(encoded_pipe,dest)
    try:
        a = time.time()
        s.recv(10)
        b = time.time()
        return b-a
    except:
        return 0 #if a timeout happens return 0. which will be checked at line 24

paths= ["/root/objects/large-0.obj","/root/objects/large-1.obj","/root/objects/large-2.obj",
"/root/objects/large-3.obj","/root/objects/large-4.obj","/root/objects/large-5.obj",
"/root/objects/large-6.obj","/root/objects/large-7.obj","/root/objects/large-8.obj",
"/root/objects/large-9.obj","/root/objects/small-0.obj","/root/objects/small-1.obj",
"/root/objects/small-2.obj","/root/objects/small-3.obj","/root/objects/small-4.obj",
"/root/objects/small-5.obj","/root/objects/small-6.obj","/root/objects/small-7.obj",
"/root/objects/small-8.obj","/root/objects/small-9.obj"]
print(send_object(paths, host, port))

        