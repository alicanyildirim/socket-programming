## HOW TO RUN

there are two folders, client and server, server.py will write the files two server folder. The execution is as follows:
python3 server/server.py  65144 65145
python3 client/client.py 127.0.0.1 65144 65145 65456 65352

The filenames can be changed in the client.py 242th line for tcp, 247th line for udp; 
                             in the server.py 255th line for tcp, 259th line for udp.


I have started to do this homework in 12.12.2020. I decided to start with the TCP, since UDP requires RDT on top of it, i thought it would be easier to do after implementing TCP. 

I never encountered this, but since I start the udp process after the tcp, according to the delays or timeouts, the pipes may be broken if the client for udp starts firstly and waits for a second.
## TCP
I spent most of my time debugging the transferred file check. My program sends it as a binary but when I write it to the file, decoding and encoding method did not seem to work. I think my wrting was the issue, by adding "b" tag, I was able to solve the issue. I had the issue of getting corrupted chars when sending with tcp. 
I got '�����' these types of corrupt readings from TCP. These defects wasted good chunk of my time. But then I uncommented my time.sleep()
then those defects were gone. Running diff on two files gave finally no differences and the checksums matched. I have looked to socket.settimeout, but decided to implemented it later if I had time, because it did not work when adding intuitively.
I have created 4 files with the head -c XM < /dev/urandom to test, however I got an error from client which stated the following error 'UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 1: invalid start byte' this is probably caused by my program not being able to decode the chars created by /dev/urandom. Creating lorem ipsum file, I confirm that is the case since that lorem ipsum file did not budge against my program. Fortunately I was able to find out the cause of it easily and simple change to byte_chunk to bytearray type solved the issue. Testing it again gave me the correct checksums of the file sent to the server. 


## UDP
    For UDP I have watched [this](https://www.youtube.com/watch?v=6lP0ow8Voe0) video and it was amazing. The layout of what I need to implement was pretty much clear for me. 
    Below I wrote down what I believe must happen in order to implement RDT on top of UDP.
    *client*                                        *server*
    1. divide the data into chunks.                 5. Unpack the pck.
    2. calculate checksum                           6. Check the checksum.
    3. pack = checksum + seq + pck                      * if they are the same, append the data, send ACK1
    4. sent the pack to the Server.                     * if not send ACK0
    5. start timer, wait for ACK                    
    7. if ACK0, retransmit, else move to the next.

    After working on it for a while I couldn't wrap my head around it, because it became complex for me.
    What I did was to implement udp incrementally like in the slides and the video I reffered to.


    Poor understanding of the recvfrom funct and the port I need to use cost me a lot of time. I haven't been using the address I should get from the recvfrom. 

    I also had a bug while getting the commandline arguments, but PORT gave connection refused so I waste a bunch of time there.
    I have finished and started to test it in 19.12.2020 at 20:15 o'clock.    

I have learnt how to implement RDT over UDP and I got hands on experience with socket programming.