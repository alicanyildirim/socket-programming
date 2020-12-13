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

import socket
import hashlib
import struct
import time

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

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
run_tcp_server("out4.bin",HOST,PORT)




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
