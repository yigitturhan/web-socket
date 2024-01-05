import socket
import hashlib
import time
dest = ("", 12345)
type = 'utf-8'
def get_objects(dest):
    start = time.time() #the starting time to measure total time to send 20 files
    encoded_ok = "OK".encode(type) #precalculation of some values in order to decrease complexity - from here to
    encoded_end_header = "END_HEADER".encode(type)
    encoded_end_header_hash = compute_sha256(encoded_end_header)
    encoded_nack_header = "NACKHEADER".encode(type)
    encoded_ack_header = "ACK_HEADER".encode(type)
    encoded_ack_header_hash = compute_sha256(encoded_ack_header)
    encoded_nack_header_hash = compute_sha256(encoded_nack_header)
    encoded_end = "END".encode(type)
    encoded_end_hash = compute_sha256(encoded_end)
    encoded_ok_hash = compute_sha256(encoded_ok)
    encoded_pipe = "|".encode(type)#here
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(dest)#binding the port
        file_names, files = [], [] #two lists. one stores file names the other stores related data
        rtt_send, counter = False, 0 #values to calculate rtt at the sender side
        s.settimeout(0.3) #default timeout for rtt calculation
        for _ in range(8): #this tries 15 times to get just a pipe symbol. used for rtt calculation Please check note 1 in the information about code part at report
            try:
                message, addr = s.recvfrom(1024)
                s.sendto(encoded_ok,addr)
            except:
                pass
        s.settimeout(None) #reseting the timeout since in normal data transfer we have not set any timeout at the receiver side
        while True:
            message, addr = s.recvfrom(1024) #We expect to get end header signal or the header datas which will be used at the lists at line 21
            hash = message[:64] #we have extracted the hash
            message = message[64:] #and the remaining of the received message
            if hash == encoded_end_header_hash: #if the received hash equals too encoded_end_header_hash this means getting the header data part is finished
                s.sendto(encoded_ack_header_hash+encoded_ack_header, addr) #send ack header to sender side
                break
            if len(message) +len(hash) < 64: #just a check not to get an error. It is required because some of the packets which we expect above (rtt calculation) may come to here
                s.sendto(encoded_ok, addr) #in this case just send ok and continue to expect data
                continue
            try:
                if compute_sha256(message) != hash: #if there is a problem with hash that means the file is corrupted. Please check note 2 at the information about code in the report
                    s.sendto(encoded_nack_header_hash+encoded_nack_header, addr)#in this case just send a nack
                    continue
                if len(file_names) != 0:#if the data is ready but we are getting the same message because of dupplication or packet loss we ignore that
                    s.sendto(encoded_ack_header_hash+encoded_ack_header, addr)#then we send ack header to server in order to tell it we can continue to other process
                    continue
                data = message.decode(type) #header endse tüm filelar gelmi�~_ d
                headers = data.split("|") #spliting the headers. please check note 3 at information about code part
                for header in headers:
                    fileName, fileSize = header.split('_') #in each header extract filename and filesize
                    fileSize = int(fileSize)
                    if fileName not in file_names:
                        file_names.append(fileName)
                        files.append([False]*ceil(fileSize,1024)) #the ceil is for creating right number of elements in a list.
                s.sendto(encoded_ack_header_hash+encoded_ack_header, addr) #if all process is done send server the ack header message. which means we can continue to other process
            except:
                s.sendto(encoded_ok_hash+encoded_ok, addr)#if a problem occurs above we send ok. Then server tries to send the message again

        while True: #the part where we get the data for each file
            message = s.recv(1250) #getting the message
            hash = message[:64]#and extracting the hash
            if hash == encoded_end_header_hash: #if hash is end header hash that means this should be a packet which should arrive at above.
                s.sendto(encoded_ack_header_hash+encoded_ack_header, addr) #discard it and send ack header to inform server that we can continue
                continue
            if hash == encoded_end_hash: #if hash is end hash that means that process is done and we have received all the data
                s.sendto(encoded_ok_hash+encoded_ok, addr)#send an ok for server to stop the program
                break
            try:
                a,b,c = message[64:].decode(type).split("|") #if we cannot split the arriving data to 3 pieces this means there is an error
            except: #the try except block is for handling that error. just ignore this packet and continue with next loop
                continue
            file_name, index, data = message[64:].decode(type).split("|") #extracting the filename, index and data of packet. please check note 4 for more information
            data, index = data.encode(type), int(index) #encoding the data to write on the file and making the index integer
            if compute_sha256(file_name.encode(type)+encoded_pipe+str(index).encode(type)+encoded_pipe+data) == hash: #if the arrived packets hash is same with the calculation this means no error occured
                files[file_names.index(file_name)][index] = data #at the files list get the first index (this data belongs to which file) then the second index (at which order this should be)
                ack_data = ("OK_"+file_name+"_"+str(index)).encode(type)
                hash_of_ack = compute_sha256(ack_data)
                s.sendto(hash_of_ack+ack_data, addr)#send an ok message with filename and index. this will tell the server that we have received this part
        write_files(file_names, files)#when everything is finished write the files with incoming data
    end = time.time() #end time to calculate total time to receive 20 files
    return end - start #return the total time

def compute_sha256(data):
    return hashlib.sha256(data).hexdigest().encode(type) #please check note 5 for more information

def ceil(num, divider): #the ceil function. it returns how much element do we need to store a file in 1024 byte length elements
    if num//divider == num/divider:
        return num//divider
    return num//divider + 1

def write_files(file_names, file_data): #a function which gets file names and data then writes the files
    for i in range(len(file_names)):
        with open(file_names[i],"wb") as f:
            for data in file_data[i]:
                f.write(data)



print(get_objects(dest))