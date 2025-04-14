from check_sum import check_sum

def build_packet(TYPE, ID, SEQ, DATA):
    ##### Concat TYPE with ID #####
    PACKET = chr((TYPE << 4) + ID)

    ##### Concat with SEQUENCE #####
    PACKET += chr(0) + chr(SEQ)

    ##### Concat with Length #####
    PACKET += chr(0) + chr(len(DATA))

    ##### Concat with Checksum #####
    READ_DATA = ''
    for char in DATA:
        READ_DATA += chr(char)
    PACKET += chr(0) + chr(check_sum(PACKET + READ_DATA))
    
    ##### Concat with Data #####
    PACKET += READ_DATA

    return PACKET.encode()

def extract_packet(PACKET):
    data = PACKET.decode()

    TYPE = ord(data[0]) >> 4
    ID =  ord(data[0]) & 0x0f
    SEQ = ord(data[2])
    LENGTH = data[3:5].encode()
    CHECK_SUM = data[5:7].encode()
    READ_DATA = data[7:].encode()

    return TYPE, ID, SEQ, LENGTH, CHECK_SUM, READ_DATA
