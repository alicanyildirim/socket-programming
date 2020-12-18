I have started to do this homework in 12.12.2020. I decided to start with the TCP, since UDP requires RDT on top of it, i thought it would be easier to do after implementing TCP. 

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


    I should also note that the transmission times include the timeout value since it is also a part of the communication.