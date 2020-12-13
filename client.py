# Client takes -> server ip, server's udp listen port, server's tcp listen port,

# client's sender port for udp, client's sender port for tcp through cl args.

# only client can read the files.
# client should divide the both files into chunks of up to 1000bytes before sending. -> fragmentation.
# transfer files.
# timeout?


from sys import argv
import socket
import hashlib
import struct
import time
import sys
#Get the arguments from command line.
server_ip = argv[1]
server_udp_listen = argv[2]
server_tcp_listen = argv[2]
client_udp_sender = argv[3]
client_tcp_sender = argv[4]

tcp_file_original = "transfer_file_TCP.txt"

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server


def run_tcp_client(tcp_file,HOST,PORT):
    # the file we will send via tcp
    #print(sys.getsizeof(tcp_str))    
    #print(len(tcp_str))    
    tcp_file_raw  = open(tcp_file,'rb')
    tcp_str = tcp_file_raw.read()


    # create streaming socket
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # establish tcp connection with the server

    # needs to be tuple apparently
    tcp_socket.connect((HOST,PORT))

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
        time.sleep(0.1)


    # need to encode, md5 throws error otherwise

    # need to encode, md5 throws error otherwise
    #tcp_check = tcp_str.encode('utf-8')

    tcp_file_raw.close()
    tcp_file_raw  = open(tcp_file,'rb')
    tcp_str = tcp_file_raw.read()
    print(hashlib.md5(tcp_str).hexdigest())




    # this also prints a newline
    #print(tcp_file_raw.read())

    # tcp_file_raw.close()

    '''
    # the file we will send via tcp
    tcp_file_raw = open(tcp_file,'r')
    tcp_str = tcp_file_raw.read()

    # need to encode, md5 throws error otherwise
    a = tcp_str[:1000].encode('utf-8')


    print(hashlib.md5(a).hexdigest())
    '''

#run_tcp_client(tcp_file_original,HOST,PORT)
#run_tcp_client("test1.bin",HOST,PORT)
#run_tcp_client("lorem.txt",HOST,PORT)
#run_tcp_client("test1.bin",HOST,PORT)
#run_tcp_client("test2.bin",HOST,PORT)
#run_tcp_client("test3.bin",HOST,PORT)
run_tcp_client("test4.bin",HOST,PORT)