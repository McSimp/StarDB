from stardb.databases import SimpleDatabase
from hashlib import sha256

class SimpleSha256Database(SimpleDatabase):
    def __init__(self, blockFile, contentID):
        super().__init__(blockFile, contentID, 32)

    def find(self, key):
        digest =  sha256(key.encode('utf-8')).digest()
        return super().find(digest)
