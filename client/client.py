# Client takes -> server ip, server's udp listen port, server's tcp listen port,

# client's sender port for udp, client's sender port for tcp through cl args.

# only client can read the files.
# client should divide the both files into chunks of up to 1000bytes before sending. -> fragmentation.
# transfer files.
# timeout?

'''
    Client -> Sender, Server -> Reciever
    What if the ACK is corrupted? -> Client does not know what happens in the Server side, ..
    so he can't just retransmit, since that may cause duplicate packets being transmitted.
    Can use sequnce numbers to uniquely identify packets. If reciever gets duplicate, just discards.
    Only two sequence numbers will suffice. How? Client can only send current packet or next packet.    
    Server says 0 -> Client sends the pck again. 
    Server says 1 -> Client sends the next pck. 
    ! Server does not know if the current transmit is a retransmit or not.
    ! In case of bit error -> checksum, ACKs, Seq Num.
    ! In case of pck loss (entire pck) ->  need a timeout. Wait for a reasonable amount of time..
    If Client does not recieve a ACK by then, sends it again.
    What is a reasonable time? 
    Client will send a pck and start the timer. Before the timer goes off if Client recieves a ACK, it stops the timer. Otherwise repeat.

    Client                 - Server
    send pck0              - rcv pck0, send ACK0
    rcv  ACK0, send pck1   - rcv pck1, send ACK1
    rcv  ACK1, send pck0   - rcv pck0, send ACK0

    premature timeout -> duplicate pcks and acks

'''

from sys import argv
import socket
import hashlib
import struct
import time
import sys


#Get the arguments from command line.
server_ip = argv[1] 
udp_listen_for_server = argv[2]
tcp_listen_for_server = argv[2]
udp_sender_for_client = argv[3]
tcp_sender_for_client = argv[4]


def run_tcp_client(tcp_file,server_ip,PORT):
    # the file we will send via tcp
    #print(sys.getsizeof(tcp_str))    
    #print(len(tcp_str))    
    tcp_file_raw  = open(tcp_file,'rb')
    tcp_str = tcp_file_raw.read()


    # create streaming socket
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # establish tcp connection with the server
    tcp_socket.settimeout(1)
    # needs to be tuple apparently
    tcp_socket.connect(('',int(PORT)))
    #print(sys.getsizeof(sliced))    
    # split data into chunks.
    #print(len(chunks))    
    # split data into chunks.
    chunks = [tcp_str[i:i+1000] for i in range(0, len(tcp_str), 1000)]
    for chunk in chunks:
        #print(f"Sending {i}")
        #print("a")

        # gives 1033 bytes 
        #print(sys.getsizeof(chunk.encode('utf-8')))    

        # need to make it byte 
        byte_chunk = bytearray(chunk)

        # using 'd' -> double will store 8 bytes.
        # send the time with the data to the server.
        message = struct.pack("d", time.time()) + byte_chunk
        tcp_socket.send(message)
        time.sleep(0.001)


    # need to encode, md5 throws error otherwise

    # need to encode, md5 throws error otherwise
    #tcp_check = tcp_str.encode('utf-8')

    # Closing the connection
    tcp_socket.close()
    
    tcp_file_raw.close()
    tcp_file_raw  = open(tcp_file,'rb')
    tcp_str = tcp_file_raw.read()
    file_checksum = hashlib.md5(tcp_str).hexdigest()

    print(f"TCP file checksum: {file_checksum}")




    # this also prints a newline
    #print(tcp_file_raw.read())

    # tcp_file_raw.close()


#run_tcp_client(tcp_file_original,HOST,PORT)
#run_tcp_client("test1.bin",HOST,PORT)
#run_tcp_client("lorem.txt",HOST,PORT)
#run_tcp_client("test1.bin",HOST,PORT)
#run_tcp_client("test2.bin",HOST,PORT)
#run_tcp_client("test3.bin",HOST,PORT)
#run_tcp_client("test4.bin",HOST,PORT)

'''
tcp_file = "transfer_file_TCP.txt"
tcp_file_raw  = open(tcp_file,'rb')
tcp_str = tcp_file_raw.read()
checksum = hashlib.md5(tcp_str)
'''
#print(checksum)
#print(sys.getsizeof(checksum))



    # Send a pck and start the timer. include checksum + seq. number + pck
    # If Client recieves ACK0, retransmit the current packet.
    # If Client recieves ACK1, client sends the next packet.
    # Wait for reasonable amount of time for the ACK.
        # If recieved clear the timer, sent the next pck.
        # If not recieved. send the current pck again.
    

# used: server_ip,udp_listen_for_server,udp_sender_for_client
# udp_sender_for_client  => dest. port
# udp_listen for_ server =>     


def run_udp_client(udp_file,server_ip,udp_listen_for_server,udp_sender_for_client):
    # read the file.
    udp_file_raw  = open(udp_file,'rb')
    udp_str = udp_file_raw.read()
    
    # split data into chunks.
    chunks = [udp_str[i:i+900] for i in range(0, len(udp_str), 900)]


    
    # py takes it as a string so type casting is needed.
    # host -> str, port -> int 
    
    # this sends the chunks to the server
    # create streaming socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    
    #retransmisson count of the packets
    retransmisson = 0
    # sent every bit of chunk to the server.
    sequence = 0
    for chunk in chunks:
        # flag to check if there is ACK to process
        flag = False
        # need to make it byte, hashes work on bytes not chars they say.
        byte_chunk = bytearray(chunk) # 957 bytes
        start_time = time.time() * 1000.0 # seconds to ms. 24 bytes.

        checksum = hashlib.md5(byte_chunk).digest() # in byte format.
        header =  struct.pack("d", start_time) + struct.pack("32s",checksum) + struct.pack("i", sequence)
        #print(checksum)
        message = header + byte_chunk #this gives 977, math doesn't add up.
        #print(sys.getsizeof(message))
        while not flag:
            
            # message is ready to go to the server.
            #sent the encapsulated message to the server.
            udp_socket.sendto(message,(server_ip,int(udp_listen_for_server))) #This is true.
            #try to listen for the ACK
            # stop and wait for response here.
            try:
                time.sleep(0.0001)
                ack_all, _ = udp_socket.recvfrom(1000)
            except socket.timeout:
                #the ACK never came :(
                # send it again if it is a duplicate on the server site it will not process it, 
                # however server will not processes it
                retransmisson += 1
                udp_socket.sendto(message,(server_ip,int(udp_listen_for_server))) #This is true.
                
            else:
                #print(ack_all)
                ack_checksum = struct.unpack("32s", ack_all[0:32])[0]
                ack = ack_all[32:]
                #print(ack)
                #control_ack = b'1'
                control_ack_checksum = hashlib.md5(ack).digest()
                #print(ack_checksum.hex())
                #print(control_ack_checksum.hex())
                #print(control_ack_checksum.hex() == ack_checksum.hex()[:32])
                if(ack_checksum.hex()[:32] == control_ack_checksum.hex()):
                    if(b'1' == ack):
                        #print("YES")
                        #recieved ACK1 
                        # Go to the next chunk to deliver.
                        flag = True
                        sequence += 1
                    else:
                        #Negative ACK recieved. send it again.
                        retransmisson += 1
                        udp_socket.sendto(message,(server_ip,int(udp_listen_for_server))) #This is true.
                    #print(ack)
                else:
                    # ACK is corrupted.
                    # can't just send this chunk again. possible duplicate.
                    retransmisson += 1
                    udp_socket.sendto(message,(server_ip,int(udp_listen_for_server))) #This is true.
            # I need to sleep here or the connection closes.        
            # time.sleep(0.005)
        
    # Close the connection
    udp_socket.close()
    
    udp_file_raw.close()
    udp_file_raw  = open(udp_file,'rb')
    udp_str = udp_file_raw.read()
    file_checksum = hashlib.md5(udp_str).hexdigest()

    print(f"UDP file checksum: {file_checksum}")
    # UDP Transmission Re-transferred Packets:  ...
    print(f"UDP Transmission Re-transferred Packets: {retransmisson}" )
    #close the file.
    udp_file_raw.close()
    



tcp_file_original = "transfer_file_TCP.txt"
run_tcp_client(tcp_file_original,server_ip,tcp_listen_for_server)



udp_file_original = "transfer_file_UDP.txt"
#run_udp_client(udp_file_original,server_ip,udp_listen_for_server,udp_sender_for_client) 

# How I compared the file transmitted.
'''
udp_file_raw  = open(udp_file_original,'rb')
udp_str = udp_file_raw.read()
checksum = hashlib.md5(udp_str).hexdigest()
print(checksum)
'''
