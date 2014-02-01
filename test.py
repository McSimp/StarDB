from stardb.storage.blockfile import BlockFile
from stardb.btree.btreedatabase import BTreeDatabase
from stardb.util import readVLQU

import hashlib

class SimpleDatabase(BTreeDatabase):
    def __init__(self, blockFile, keySize, contentID):
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

glblIndex = hashlib.sha256('_index'.encode('utf-8')).digest()

if __name__ == '__main__':
    f = open('C:\\SSDSteam\\SteamApps\\common\\Starbound\\assets\\packed.pak', 'rb')

    bf = BlockFile(f)
    db = SimpleDatabase(bf, 32, 'Assets1')
    db.open()
    print(bf.getDebugInfo())
    print(db.getDebugInfo())
    
    try:
        db[glblIndex]
        print("Found")
    except KeyError:
        print("Not Found")
