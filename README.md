I have started to do this homework in 12.12.2020. I decided to start with the TCP, since UDP requires RDT on top of it, i thought it would be easier to do after implementing TCP. 

I spent most of my time debugging the transferred file check. My program sends it as a binary but when I write it to the file, decoding and encoding method did not seem to work. I think my wrting was the issue, by adding "b" tag, I was able to solve the issue.