# PING Client.py
# David Williams
# 4/18/2023

import random
import select
from socket import *
import string
import sys
import socket
import time

args = sys.argv

# Handle if arguments are missing or incorrect
if len(args) != 6:
    print ("Error: Invalid Arguments")
    exit()
    
# define and assign variables
hostname = args[1]
portNum = int(args[2])
port = args[2]
clientID = int(args[3])
num_of_ping_request_packets =int(args[4])
waitTime = args[5]
version = 1
max_payload_size = 300
min_payload_size = 150
returnedPacket = []
payload_size = random.randint(min_payload_size, max_payload_size)
num_of_ping_response_packets = 0
maxRTT = 0.0
minRTT = 99999.0
combinedRTT = 0.0
combinedPayload = 0
lossed = 0

# Create client socket
clientSocket = socket.socket(AF_INET, SOCK_DGRAM)

# Assign hostname to an IP address
try:
    myIP = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    
    #addressInfo returns a tuple containing IP information  
    addressInfo = socket.getaddrinfo(myIP, None)

    # Get the IP addresses from the addressInfo
    ip_addresses = []
    for info in addressInfo:
        
        ip_address = info[4][0]
        ip_addresses.append(ip_address)

    # error raised if the hostname is incorrect or doesn't exist
except socket.gaierror as e:
    print(f"Error resolving hostname {hostname}: {e}")
    exit()
    
# Print opening statement
print('\nPINGClient started with server IP:', ip_address , 'Port:', port, 'Client ID:', clientID, 'Packets:',num_of_ping_request_packets, 'Wait:', waitTime)

# Function to generate string for 'data' in payload
def generate_random_string(length):
    letters_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_digits) for i in range(length))


# Construct and send <number_of_ping_request_packets> packets to the server
for i in range(num_of_ping_request_packets):
    payload_size = random.randint(min_payload_size, max_payload_size)
    classname = "PINGClient"
    username = "Williams, David"
    rest = payload_size - (len(hostname) + len(classname) + len(username))
    payloadData = generate_random_string(rest)
   
    start = time.time()

    print('----------Ping Request Packet Header----------', '\n'  'Version:', 1, '\nClient ID:', clientID, '\nSequence No.:', i, '\nTime:', "{:.3f}".format(start), '\nPayload Size:', payload_size) 
    print('----------Ping Request Packet Payload---------\n Host:', ip_address,'\nClass-name: PINGClient','\nUser-name: Williams, David', '\nRest:', payloadData)
    print("---------------------------------------")
    combinedPayload += payload_size
    

    pingHeader = [str(version), str(clientID), str(i), str(start), str(payload_size), ip_address, payloadData, str(waitTime) ]
   
    for x in pingHeader:

            clientSentence = x
            clientSocket.sendto(clientSentence.encode(), (hostname, portNum))
            
            
    # Receive from server
    while 1:
            # A way to see if there will be a timeout
            ready = select.select([clientSocket], [], [], float(waitTime))
            
        
           
            
            
            if ready[0]:
                
               
                server_msg, serverAddress = clientSocket.recvfrom(2048)
                server_msg = server_msg.decode()

                # Create an array containing the packet information
                returnedPacket.append(server_msg)
               
            else:
                 print('------Ping Response Timed-Out-----\n')
                 break
            
            # Once the packet is complete, format and print the packet
            if len(returnedPacket) == 7:
                    totaltime = (time.time() - start)
                    start = time.time()
                    
                    if totaltime < float(minRTT):
                        minRTT = totaltime
                        
                    if totaltime > maxRTT:
                        maxRTT = totaltime
                        
                    combinedRTT += totaltime
                    
                    print('----------Received Ping Request Packet Header----------\nVersion:', returnedPacket[0], '\nClient ID:', returnedPacket[1], '\nSequence No.:', returnedPacket[2], '\nTime:', "{:.3f}".format(float(returnedPacket[3])), '\nPayload Size:', returnedPacket[4]) 
                    print('----------Received Ping Request Packet Payload---------\n Host:', returnedPacket[5],'\nClass-name: VCU-CMSC440-SPRING-2023', '\nRest:', returnedPacket[6])
                    print("---------------------------------------\nRTT:{:.3f}\n".format((totaltime) * 1000) ) 
                    
                    # Empty the 'buffer' for the next packet
                    returnedPacket.clear() 
                    num_of_ping_response_packets = num_of_ping_response_packets + 1
                    break
            
    if num_of_ping_response_packets == 0: avgRTT = 0
    else:avgRTT = combinedRTT/num_of_ping_response_packets
    
    if num_of_ping_response_packets == 0: lossRate = 0
    else:lossRate =  (1 - (num_of_ping_response_packets/num_of_ping_request_packets))
    
    #minRTT =  "{:.3f}".format(minRTT* 1000)
    
   
    
# Print the summary stats for the entire PING interaction
print('\nSummary', num_of_ping_request_packets, '::', num_of_ping_response_packets, '::', round(lossRate * 100), '::', "{:.3f}".format(minRTT* 1000), '::',"{:.3f}".format((maxRTT * 1000)), '::', "{:.3f}".format((avgRTT * 1000)) , '::', (round(combinedPayload/num_of_ping_request_packets)))
# close the socket
clientSocket.close()

