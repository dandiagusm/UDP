def check_sum(msg):
    chk = 0
    #### Check for 2 bytes ####
    for i in range(0, len(msg), 2):
        word = ord(msg[i]) + (ord(msg[i+1]) << 8 )
        chk = chk + word

        chk = (chk>>16) + (chk & 0xffff)
        chk = chk + (chk >> 16)

        #complement and machkk to 4 byte chkhort
        chk = ~chk & 0xffff

        return chk

def check_sum_from_hex(msg):
    chk = 0
    for byte in msg:
        chk += ord(byte)

    return chk;
