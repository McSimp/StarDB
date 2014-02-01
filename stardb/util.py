import struct

def unpack(fmt, buff):
    return struct.unpack(fmt, buff)[0]

def bytesToString(bytes):
    return bytes.decode('utf-8').rstrip('\0')

def readVLQU(stream):
    value = 0
    while True:
        tmp = ord(stream.read(1))
        value = (value << 7) | (tmp & 0x7f)
        if tmp & 0x80 == 0:
            break
    return value