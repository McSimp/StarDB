import struct
from io import BytesIO

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

def unpackStringList(data):
    stream = BytesIO(data) # TODO: I think this makes a copy
    count = readVLQU(stream)
    strings = []
    for i in range(count):
        strLen = readVLQU(stream)
        strings.append(stream.read(strLen).decode('utf-8'))
    return strings
