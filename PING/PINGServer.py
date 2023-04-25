# PING Server.py
# David Williams
# 4/18/2023

from random import randint
from socket import *
import socket
import sys
import time

# Error Handling
args = sys.argv
if len(args) != 3:
    print ("ERR - Incorrect Number Of Arguments")
    exit()
if (10000 > int(args[1]) > 11000):
    print("ERR - arg 1")
if int(args[1]) > 65536 or int(args[1]) < 0:  
    print("ERR - arg 1")
else:
    port = int(args[1])
loss = int(args[2])

try:
    try:
        # Create a server socket
        serverSocket = socket.socket(AF_INET, SOCK_DGRAM)
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        serverSocket.bind(('', port))
        packet = []
        returned = []
        serverIP = ""

    # Handle if port is already taken by active socket
    except OSError:
        print("ERR - cannot create PINGServer socket using port number {}".format(port))
        exit()


    addressInfo = socket.getaddrinfo(hostname, None)
    # Get the IP address from the tuple of IP information
    for info in addressInfo:
        ip_address = info[4][0]
        

    

    # Find a way to print the IP
    serverIP = serverSocket.getsockname()[0]
    print('PINGServer started with server IP: {} Port: {} ...'.format(ip_address, port))

 

    while 1:
        # Waits for some client to send a packet
        lossed = randint(1,100) <= loss
        if lossed:
            status = "DROPPED"
        else:
            status = "RECEIVED"
        ping_msg, clientAddress = serverSocket.recvfrom(2048) 
        ping_msg = ping_msg.decode()
    
        # Store the chunks of data until the full packet is received
        packet.append(ping_msg)
        
        
        # Once the packet is completely received, assemble format and print the packet.
        if len(packet) == 8:
            start = time.time()
            
            
                
        
            print("\nIP:", packet[5] , " :: Port:", port, " :: ClientID:", packet[1], " :: Seq#:", ":: ", packet[2], status)

            print('----------Received Ping Request Packet Header----------', '\n'  'Version:', packet[0], '\nClient ID:', packet[1], '\nSequence No.:', packet[2], '\nTime:', "{:.3f}".format(float(packet[3])), '\nPayload Size:', packet[4]) 
            print('----------Received Ping Request Packet Payload---------\nHost:', packet[5],'\nClass-name: VCU-CMSC440-SPRING-2023','\nUser-name: Williams, David', '\nRest:', packet[6])
            print("---------------------------------------")
           
            # Repeat the same process to send the packet back to the client
            returned = [packet[0], packet[1], packet[2], packet[3], packet[4], packet[5], packet[6]]
            if lossed:
                time.sleep(int(packet[7]))
                
            else:
                for x in returned:
                    serverSentence = x
                    serverSentence = serverSentence.upper()
                    serverSocket.sendto(serverSentence.encode(), clientAddress)  
           
                print('-------Ping Response Packet Header------', '\n'  'Version:', packet[0], '\nClient ID:', packet[1], '\nSequence No.:', packet[2], '\nTime:', "{:.3f}".format(start), '\nPayload Size:', packet[4]) 
                print('------ Ping Response Packet Payload------\nHost:', packet[5],'\nClass-name: PINGServer','\nUser-name: Williams, David', '\nRest:', packet[6].upper())
                print("---------------------------------------")
            
            # Empty the 'buffer' for the next incoming packet
            returned.clear();
            packet.clear()
except KeyboardInterrupt:
    print('\nClosing client socket...')
    serverSocket.close()
    

