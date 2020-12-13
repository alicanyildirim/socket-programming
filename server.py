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


# TCP connection
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# the server only gets the ports, how to know the host?
tcp_socket.bind((HOST, PORT))

# listen 
tcp_socket.listen()

# accept the connection
client_socket, client_addr = tcp_socket.accept()

reassamble = []
while True:
    # message is 1033 bytes + 8 bytes = 1041 bytes
    message = client_socket.recv(1041)
    if message == b'':
        client_socket.close()
        break 


    t = struct.unpack("d", message[:8])[0]
    passing_time = time.time() - t
    # get the time information
    #print(passing_time)
    # get the payload.
    payload = message[8:]
    reassamble.append(payload)

length = len(reassamble)
with open("tcp_out.txt", "wb") as output_file:
	for i in range(length):
		output_file.write(reassamble[i])
# now the reassamble is a str


tcp_file_raw  = open("tcp_out.txt",'rb')
tcp_str = tcp_file_raw.read()
tcp_file_raw.close()
# need to encode, md5 throws error otherwise
#tcp_check = tcp_str.encode('latin-1')
print(hashlib.md5(tcp_str).hexdigest())

# split the payload into chunks.

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
