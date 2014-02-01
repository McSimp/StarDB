class BTree:
    def __init__(self):
        self.rootIsLeaf = False
        self.rootPointer = None

    def find(self, key):
        if self.rootIsLeaf:
            return self.findInLeaf(self.loadLeaf(self.rootPointer), key)
        else:
            return self.findInIndex(self.loadIndex(self.rootPointer), key)

    def __getitem__(self, key):
        return self.find(key)

    # Warning: It's usually not a good idea to use the "in" operator (which calls this method) -
    # it's better to just use the subscript operator and catch the KeyError exception.
    def __contains__(self, key):
        try:
            self.find(key)
            return True
        except KeyError:
            return False

    def findInLeaf(self, leaf, key):
        return leaf.findData(key)

    def findInIndex(self, index, key):
        i = index.find(key)
        if index.level == 0:
            return self.findInLeaf(self.loadLeaf(index.pointer(i)), key)
        else:
            return self.findInIndex(self.loadIndex(index.pointer(i)), key)

    def loadLeaf(self, pointer):
        raise NotImplementedError

    def loadIndex(self, pointer):
        raise NotImplementedError
