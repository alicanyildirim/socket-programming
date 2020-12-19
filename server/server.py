# cl args listen port for udp, listen port for tcp

# realize when the whole file is transferred then stop listening, reassamble, save the files.

# calculate the average packet transmisson times for udp and tcp
# start the time before sending a packet in client. 
# stop the time after packet is recieved in server.
# If you resend a packet only consider the last packet.

#Print average as..
#TCP Packets Average Transmission Time: ... ms
#UDP Packets Average Transmission Time: ... ms
#TCP Communication Total Transmission Time: ... ms
#UDP Communication Total Transmission Time: ... ms


# in the client -> UDP Transmission Re-transferred Packets: ...

from sys import argv
import socket
import hashlib
import struct
import time

udp_listen_port = argv[1] 
tcp_listen_port = argv[2]


def run_tcp_server(output,HOST,PORT):
    # TCP connection
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # the server only gets the ports, how to know the host?
    tcp_socket.bind((HOST, PORT))
    # listen 
    tcp_socket.listen()
    # accept the connection
    client_socket, _ = tcp_socket.accept()
    reassamble = []
    elapsed_times = []
    start_times = []
    while True:
        # message is 1033 bytes + 8 bytes = 1041 bytes
        message = client_socket.recv(1041)
        if message == b'':
            #TCP Packets Average Transmission Time: ... ms
            average_tcp_time = sum(elapsed_times) / len(elapsed_times) 
            print(f"TCP Packets Average Transmission Time: {average_tcp_time:.4} ms" )
            
            #TCP Communication Total Transmission Time: ... ms
            total_time = (time.time()-start_times[0])*100
            print(f"TCP Communication Total Transmission Time: {total_time:.4} ms" )
            client_socket.close()
            break 


        # get the time information
        t = struct.unpack("d", message[:8])[0]
        passing_time = time.time() - t
        start_times.append(t)
        #from sec to msec
        elapsed_times.append(passing_time*100)
        
        # get the payload.
        payload = message[8:]
        reassamble.append(payload)
    length = len(reassamble)
    with open(output, "wb") as output_file:
        for i in range(length):
            output_file.write(reassamble[i])
    
    
    # need to encode, md5 throws error otherwise
    tcp_file_raw  = open(output,'rb')
    tcp_str = tcp_file_raw.read()
    print(hashlib.md5(tcp_str).hexdigest())
    tcp_file_raw.close()
    #tcp_check = tcp_str.encode('latin-1')

    # split the payload into chunks.
output = "tcp_out1.txt"
#run_tcp_server(output,HOST,PORT)

#run_tcp_server("out_lorem.txt",HOST,PORT)
#run_tcp_server("out1.bin",HOST,PORT)
#run_tcp_server("out2.bin",HOST,PORT)
#run_tcp_server("out3.bin",HOST,PORT)
#run_tcp_server("out4.bin",HOST,PORT)




# checksum using pseudo header + tcp header + tcp body

# Source Port
# Destination Port
# Sequence Number
# Acknoledgement Number
# Data Offset
# Flags
# Window
# Checksum (initial value)
# Urgent pointer
'''
def run_udp_server(output,HOST,PORT):
    # TCP connection
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # the server only gets the ports, how to know the host?
    tcp_socket.bind((HOST, PORT))
    # listen 
    tcp_socket.listen()
    # accept the connection
    client_socket, _ = tcp_socket.accept()
    reassamble = []
    elapsed_times = []
    start_times = []
    while True:
        # message is 1033 bytes + 8 bytes = 1041 bytes
        message = client_socket.recv(1041)
        if message == b'':
            #TCP Packets Average Transmission Time: ... ms
            average_tcp_time = sum(elapsed_times) / len(elapsed_times) 
            print(f"TCP Packets Average Transmission Time: {average_tcp_time:.4} ms" )
            
            #TCP Communication Total Transmission Time: ... ms
            total_time = (time.time()-start_times[0])*100
            print(f"TCP Communication Total Transmission Time: {total_time:.4} ms" )
            client_socket.close()
            break 


        # get the time information
        t = struct.unpack("d", message[:8])[0]
        passing_time = time.time() - t
        start_times.append(t)
        #from sec to msec
        elapsed_times.append(passing_time*100)
        
        # get the payload.
        payload = message[8:]
        reassamble.append(payload)
    length = len(reassamble)
    with open(output, "wb") as output_file:
        for i in range(length):
            output_file.write(reassamble[i])
    
    
    # need to encode, md5 throws error otherwise
    tcp_file_raw  = open(output,'rb')
    tcp_str = tcp_file_raw.read()
    print(hashlib.md5(tcp_str).hexdigest())
    tcp_file_raw.close()
    #tcp_check = tcp_str.encode('latin-1')

    # split the payload into chunks.
output = "tcp_out1.txt"
'''
#run_tcp_server(output,HOST,PORT)

#run_tcp_server("out_lorem.txt",HOST,PORT)
#run_tcp_server("out1.bin",HOST,PORT)
#run_tcp_server("out2.bin",HOST,PORT)
#run_tcp_server("out3.bin",HOST,PORT)
#run_tcp_server("out4.bin",HOST,PORT)


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

output = "udp_out1.txt"
# run server with -> server.py 65432 65432
def run_udp_server(udp_listen_port,output):
    # UDP connection
    # the server only gets the ports, how to know the host?
    # host address: '' represents INADDR_ANY, which is used to bind to all interfaces
    # py takes it as a string so type casting is needed.


    #create two sockets one listens, other one sends, hope this works..

    # this one listens for the actual message.   
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('', int(udp_listen_port)))
    #udp_socket.connect(('',int(udp_sender_for_client)))

    # this one sends the ACK.
    # I need to broadcast.
    #response_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #response_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #response_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    #response_socket.bind(('', int(udp_listen_port)))

    reassamble = []
    elapsed_times = []
    communication_start = []
    initial = 0 # if this is 0 than get the filename and the ip address.
    sequences = [] # sequences so far accepted from client.
    # need a try except block for timeout..
    try:
        while True:
            # need to set the timeout to now it is finished. Set it to 3. no particular reason
            udp_socket.settimeout(3)
            # take 1000 bytes at most.
            message, addr = udp_socket.recvfrom(1000) 
            #print(message)

            # get the time information
            start_time = struct.unpack("d", message[:8])[0]
            
            #coming_checksum = struct.unpack("32s", message[8:40])[0] #this somehow gives unpack requires a buffer of 32 bytes
            # so this is a workaround for it
            remaining_pck = message[8:]
            coming_checksum = remaining_pck[:32]
            sequence = remaining_pck[32:36]
            #print(int.from_bytes(sequence, "little"))
            int_sequence = int.from_bytes(sequence, "little")
            #print(checksum.hex())
            

            # get the payload.
            payload = remaining_pck[36:]
            #print(f"Payload: {payload}")
            # calculate the checksum of what you get from client 
            new_checksum = hashlib.md5(payload).digest()
            #need to get the first 32 bit of coming_checksum, it is acting weird.
            if(new_checksum.hex()== coming_checksum.hex()[:32]):
                #ip_address = payload[40:55] # get the ip address which is 64 bytes at most.
                #file_name = payload[55:] # get the file name which is the rest of the payload.                
                #print(ip_address)
                #print(file_name)
                #break
                if(len(communication_start) == 0 and initial == 0):
                    # First need to get the file name, and the ip address.
                    
                    
                   # initial += 1                    
                    
                    # get the start time of the transaction.
                    communication_start.append(start_time)
                
                

                # calculate the passing time, add it to the array.
                passing_time = time.time()*1000.0 - start_time
                elapsed_times.append(passing_time)



                # server will not accept duplicates so we add the sequence number and check if we recieved that before.
                if(int_sequence not in sequences):
                    sequences.append(int_sequence)
                    # add the data 
                    reassamble.append(payload)



                # send ACK
                ack = b'1'
                #print(f"ACK: {ack}")
                ack_checksum = hashlib.md5(ack).digest()
                response = struct.pack("32s",ack_checksum) + ack
                #print(response)
                #response = ack_checksum + ack
                # since server don't know the ip, broadcasting is necessary
                # (I was about to first get the ip from the client, luckly found this way.)
                udp_socket.sendto(response,addr) 
            else:
                # send NACK
                ack = b'0'
                #print(f"ACK: {ack}")
                ack_checksum = hashlib.md5(ack).digest()
                response = struct.pack("32s",ack_checksum) + ack
                #print(response)
                #response = ack_checksum + ack
                # since server don't know the ip, broadcasting is necessary
                # (I was about to first get the ip from the client, luckly found this way.)
                udp_socket.sendto(response,addr) 
                print("a")

            #print(payload)
    except socket.timeout:
        udp_socket.close()
    

    length = len(reassamble)
    with open('server/'+output, "wb") as output_file:
        for i in range(length):
            output_file.write(reassamble[i])
    

    udp_file_raw  = open(output,'rb')
    udp_str = udp_file_raw.read()
    print(hashlib.md5(udp_str).hexdigest())
    udp_file_raw.close()






    #PRINT 

    #UDP Packets Average Transmission Time: ... ms
    average_udp_time = sum(elapsed_times) / len(elapsed_times) 
    print(f"UDP Packets Average Transmission Time: {average_udp_time:.4} ms" )
    
    #UDP Communication Total Transmission Time: ... ms
    total_time = time.time()*1000.0-communication_start[0]
    print(f"UDP Communication Total Transmission Time: {total_time:.4} ms" )

    # TODO UDP Transmission Re-transferred Packets:  ...


run_udp_server(udp_listen_port,output)
