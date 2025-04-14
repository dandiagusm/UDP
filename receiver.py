import socket
from check_sum import check_sum, check_sum_from_hex
from utility import *

DATA = 0x0
ACK = 0x1
FIN = 0x2
FIN_ACK = 0x3

# Create UDP socket
receiversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind to address and IP
port_accepted = False
while not port_accepted:
    port = int(input("Port number: "))
    try:
        receiversocket.bind(('localhost', port))
        port_accepted = True
    except:
        print(f'Cannot use port {port}. Please another port!')
        

# Listen for incoming datagrams
print("Receiver is listneing on", receiversocket.getsockname())

file_handler = None
while True:
    #accept connections from outside
    data, address = receiversocket.recvfrom(33000)

    # Show connection received information
    print(f"Connection from {address} has been established!")

    if data:
        #### Set File name ####
        search_name = data.decode()
        if (ord(search_name[0]) == 80):
            file_handler = open(search_name[1:], 'wb')
            continue

        #### Extract packet from sender ####
        TYPE_RECEIVED, ID_RECEIVED, SEQ_RECEIVED, LENGTH, CHECK_SUM, READ_DATA = extract_packet(data)
        ##### Check checksum ######
        data = data.decode()
        checksum_calculate = check_sum(data[:5] + data[7:])
        checksum_received = check_sum_from_hex(data[5:7])
        if checksum_calculate == checksum_received:
            file_handler.write(READ_DATA)
            if (TYPE_RECEIVED == DATA):
                TYPE_RECEIVED = ACK
            elif (TYPE_RECEIVED == FIN):
                TYPE_RECEIVED = FIN_ACK

            PACKET_BACK = build_packet(TYPE_RECEIVED, ID_RECEIVED, SEQ_RECEIVED, '')
            receiversocket.sendto(PACKET_BACK, address)
            print(f"Sending ACK Packet ID {ID_RECEIVED} SEQ {SEQ_RECEIVED}")
