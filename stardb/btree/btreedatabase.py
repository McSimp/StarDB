from stardb.btree import BTree
from stardb.btree import IndexNode
from stardb.btree import LeafNode
from stardb.util import unpack, bytesToString
from io import BytesIO

class LeafInputStream:
    def __init__(self, blockStorage, buff):
        self.blockStorage = blockStorage
        self.blockBuffer = buff

    def read(self, size):
        # TODO: Try profiling this with a pre-allocated buffer
        data = BytesIO()
        blockDataSize = self.blockStorage.blockSize - 4 # Size of block excluding next pointer

        bytesToRead = size
        while bytesToRead > 0:
            endOfBlock = False

            # If there's enough room in the current block to read 'bytesToRead', just read
            # it straight into the output.
            if (self.blockBuffer.tell() + bytesToRead) < blockDataSize:
                data.write(self.blockBuffer.read(bytesToRead))
                bytesToRead = 0
            # Otherwise, read all the data we can
            else:
                bytesAvailable = blockDataSize - self.blockBuffer.tell()
                data.write(self.blockBuffer.read(bytesAvailable))
                bytesToRead -= bytesAvailable
                endOfBlock = True

            # If we've reached the end of the block and we've still got more data to read,
            # load the next block and begin the process again.
            if endOfBlock and bytesToRead > 0:
                nextBlockPointer = unpack('>i', self.blockBuffer.read(4))
                if nextBlockPointer != -1:
                    self.blockBuffer = self.blockStorage.readBlock(nextBlockPointer)

                    magic = bytesToString(self.blockBuffer.read(2))
                    if magic != BTreeDatabase.LeafMagic:
                        raise Exception('Incorrect leaf block signature')
                else:
                    raise Exception('Insufficient leaf data')

        # TODO: This is probably an expensive copy
        return data.getvalue()

class BTreeDatabase(BTree):
    FileIdentifier = 'BTreeDB4'
    IndexMagic = 'II'
    LeafMagic = 'LL'

    def __init__(self, blockStorage):
        super().__init__()
        self.blockStorage = blockStorage
        self.indexCache = {}

    def readRoot(self):
        rootData = self.blockStorage.readUserData(28, 14)

        # TODO: Figure out what's going on here
        unknownBool = unpack('?', rootData.read(1))
        rootData.seek(1, 1)
        if unknownBool:
            rootData.seek(8, 1)

        self.rootPointer = unpack('>i', rootData.read(4))
        self.rootIsLeaf = unpack('?', rootData.read(1))

    def open(self):
        self.blockStorage.open()

        userData = self.blockStorage.readUserData(0, 28)

        fileID = bytesToString(userData.read(12))
        if fileID != self.FileIdentifier:
            raise Exception(
                'DB file identifier does not match expected value of "{0}" (Got {1})'.format(
                    self.FileIdentifier,
                    fileID
                )
            )

        contentID = bytesToString(userData.read(12))
        if contentID != self.getContentIdentifier():
            raise Exception(
                'DB content identifier does not match expected value of "{0}" (Got {1})'.format(
                    self.getContentIdentifier(),
                    contentID
                )
            )

        keySize = unpack('>I', userData.read(4))
        if keySize != self.getKeySize():
            raise Exception(
                'DB content key size does not match expected value of "{0}" (Got {1})'.format(
                    self.getKeySize(),
                    keySize
                )
            )

        self.readRoot()

    def readIndex(self, pointer):
        index = IndexNode()
        buff = self.blockStorage.readBlock(pointer)

        self.currentBuffer = buff

        magic = bytesToString(buff.read(2))
        if magic != self.IndexMagic:
            raise Exception('Incorrect index block signature.')

        index.selfPointer = pointer
        index.level = unpack('B', buff.read(1))

        numChildren = unpack('>i', buff.read(4))
        index.beginPointer = unpack('>i', buff.read(4))

        for i in range(numChildren):
            key = self.readKey(buff)
            pointer = unpack('>i', buff.read(4))
            index.addPointer(key, pointer)

        return index

    def loadIndex(self, pointer):
        if pointer not in self.indexCache:
            index = self.readIndex(pointer)
            self.indexCache[pointer] = index
            return index
        else:
            return self.indexCache[pointer]

    def loadLeaf(self, pointer):
        leaf = LeafNode()
        self.currentLeafBlock = pointer

        buff = self.blockStorage.readBlock(pointer)

        magic = bytesToString(buff.read(2))
        if magic != self.LeafMagic:
            raise Exception('Iincorrect leaf block signature')

        leaf.selfPointer = pointer

        leafInput = LeafInputStream(self.blockStorage, buff)

        count = unpack('>i', leafInput.read(4))
        for i in range(count):
            key = self.readKey(leafInput)
            data = self.readData(leafInput)
            leaf.addElement(key, data)

        return leaf

    def getDebugInfo(self):
        return 'Root Is Leaf: {0}\nRoot Pointer: {1}\nIndex Cache Size: {2}'.format(
                self.rootIsLeaf,
                self.rootPointer,
                len(self.indexCache)
            )

    def getKeySize(self):
        raise NotImplementedError

    def getContentIdentifier(self):
        raise NotImplementedError

    def readKey(self, buff):
        raise NotImplementedError

    def readData(self, buff):
        raise NotImplementedError
