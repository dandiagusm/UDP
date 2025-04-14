from check_sum import *
from utility import *
import socket

#################
# CONSTANT
#################
N_FILES = 1
N_PACKETS = 10
MAX_FILES = 5
LAST_DATA = 12
READ_DATA = ''

#################
# TYPE
#################
DATA = 0x0
ACK = 0x1
FIN = 0x2
FIN_ACK = 0x3
CHUNK_SIZE = 32768

# Create UDP socket
sendersocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Ask receiver IP Address
receiver_ip = input('Receiver IP: ')

# Ask receiver Port Address
receiver_port = int(input('Receiver Port: '))

# Combine IP and Port to make Receiver Address
receiver_address = (receiver_ip, receiver_port)

# Connect to receiver
sendersocket.connect(receiver_address)

# Set Timeout
sendersocket.settimeout(10)

# Get Filenames that want to be sended
valid_files = False
while not valid_files:
    filenames = input('Send File : ')
    if filenames == '':
        print('Please input at least one file')
    else:
        filenames = filenames.split(' ')
        if (len(filenames) > MAX_FILES):
            print('Cannot send more than 5 files')
        else:
            valid_files = True

#### LOOP PER FILES ####
seq_num = [0 for i in range(0,len(filenames))]
done_id = []
chunks = []
for filename in filenames:
    file = open(filename, 'rb')

    text = file.read(CHUNK_SIZE)
    if(len(text)==0):
        print(f"File {filename} kosong")
    else :
        array_byte = []
        while text:
            array_byte.append(text)
            text = file.read(CHUNK_SIZE)
        chunks.append(array_byte)
        file.close()

ID = 0x0
FINISH = False
if chunks == []:
    FINISH = True
    
give_name = False
while not FINISH:
    #### GIVE NAME ####
    if not give_name:
        sendersocket.sendto((chr(0x50) + filenames[ID]).encode(), receiver_address)
        print(f"Give name file : {filenames[ID]}")
        give_name = True

    if (seq_num[ID] == len(chunks[ID]) - 1):
        TYPE = FIN
    else:
        TYPE = DATA

    #### BUILD PACKET ####
    PACKET = build_packet(TYPE, ID, seq_num[ID], chunks[ID][seq_num[ID]])

    #### SEND PACKET ####
    sendersocket.sendto(PACKET, receiver_address)
    print(f"Paket ID {ID} SEQ {seq_num[ID]} telah berhasil dikirim")

    #### RECEIVE ACKNOWLDGE PACKET ####
    try:
        data, address = sendersocket.recvfrom(33000)
        if data:
            TYPE_RECEIVED, ID_RECEIVED, SEQ_RECEIVED, LENGTH, CHECK_SUM, READ_DATA = extract_packet(data)
            if (TYPE_RECEIVED == ACK):
                seq_num[ID] += 1
            elif (TYPE_RECEIVED == FIN_ACK):
                done_id.append(ID)
                give_name = False
                ID += 1
    except:
        print(f"Paket ID {ID} SEQ {seq_num[ID]} timeout")
        sendersocket.sendto(PACKET, receiver_address)

    FINISH = len(done_id) == len(chunks)
