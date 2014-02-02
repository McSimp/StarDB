from io import BytesIO
from stardb.storage import BlockStorage
from stardb.util import unpack, bytesToString

class BlockFile(BlockStorage):
    HeaderMagic = 'SBBF02'
    PrefixHeaderSize = 32

    def __init__(self, dataFile):
        # We can pass in either a file object or a file path (string)
        if type(dataFile) == str:
            dataFile = open(dataFile, 'rb')
        self.file = dataFile
        self.isOpen = False
        self.headerSize = 256
        self.headFreeIndexBlock = None
        self.blockSize = 1024
        self.blockStart = 0
        self.blockEnd = 0
        self.blockCount = 0

    def setExtents(self, start, end):
        self.blockStart = start
        self.blockEnd = end

        if self.blockEnd < self.blockStart:
            self.blockEnd = self.blockStart

        self.blockCount = (self.blockEnd - self.blockStart) // self.blockSize

    def getUserHeaderSize(self):
        return self.headerSize - self.PrefixHeaderSize

    def readBlock(self, blockIndex, blockOffset = 0, size = None):
        self.checkIfOpen('readBlock', True)

        if blockIndex > self.blockCount:
            raise Exception('blockIndex: {0} out of block range'.format(blockIndex))

        if size is None:
            size = self.blockSize - blockOffset

        blockOffset = min(self.blockSize, blockOffset)
        size = min(self.blockSize - blockOffset, size)

        if size <= 0:
            raise Exception('BlockFile.readBlock would read no data (Offset = {0}, Size = {1})'.format(blockOffset, size))

        self.file.seek(self.blockStart + (blockIndex * self.blockSize) + blockOffset)
        return BytesIO(self.file.read(size))

    def readUserData(self, dataOffset, size):
        self.checkIfOpen('readFromUserData', True)

        if (dataOffset + size) > self.getUserHeaderSize():
            raise Exception('BlockFile.readUserData called outside of bounds of user header')

        self.file.seek(self.PrefixHeaderSize + dataOffset)
        return BytesIO(self.file.read(size))

    def open(self):
        self.checkIfOpen('open', False)

        if self.file is None:
            raise Exception('BlockFile.open called with no file set')

        f = self.file

        f.seek(0)
        magic = bytesToString(f.read(6))
        if magic != self.HeaderMagic:
            raise Exception('File is not a valid BlockFile')

        self.headerSize = unpack('>i', f.read(4))
        self.blockSize = unpack('>i', f.read(4))

        noFreeIndexBlock = unpack('?', f.read(1))
        if not noFreeIndexBlock:
            self.headFreeIndexBlock = unpack('>i', f.read(4))

        # TODO: I think if noFreeIndexBlock == True then we need recovery

        # Calculate file size
        f.seek(0, 2)
        fileSize = f.tell()

        self.setExtents(self.headerSize, fileSize)

        self.isOpen = True

    def getDebugInfo(self):
        return 'Header Size: {0}\nBlock Size: {1}\nHead Free Index Block: {2}\nBlock Start: {3}\nBlock End: {4}\nBlock Count: {5}'.format(
                self.headerSize,
                self.blockSize,
                self.headFreeIndexBlock,
                self.blockStart,
                self.blockEnd,
                self.blockCount
            )
