from stardb.btree import BTreeDatabase
from stardb.util import readVLQU

class SimpleDatabase(BTreeDatabase):
    def __init__(self, blockFile, contentID, keySize):
        super().__init__(blockFile)
        self.contentIdentifier = contentID
        self.keySize = keySize

    def getKeySize(self):
        return self.keySize

    def getContentIdentifier(self):
        return self.contentIdentifier

    def readKey(self, buff):
        return buff.read(self.keySize)

    def readData(self, buff):
        size = readVLQU(buff)
        return buff.read(size)
