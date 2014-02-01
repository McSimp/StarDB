from stardb.databases import SimpleSha256Database
from hashlib import sha256
from stardb.util import unpackStringList

# TODO: AssetDatabaseException class if _digest or _index not found

class AssetDatabase(SimpleSha256Database):
    def __init__(self, blockFile):
        super().__init__(blockFile, 'Assets1')
        self.fileList = None

    # I believe this is basically the SHA256 of fileName + fileContents 
    # for every single file in the database.
    def getDigest(self):
        return self['_digest']

    def getFileList(self):
        if self.fileList is not None:
            return self.fileList

        # Read file listing from _index
        indexData = self['_index']

        # It's a Starbound string list, so parse it into our Python list
        self.fileList = unpackStringList(indexData)
        return self.fileList
