import bisect

class LeafElement:
    def __init__(self, k, d):
        self.key = k
        self.data = d

    def __lt__(self, other):
        return self.key < other.key

    def __gt__(self, other):
        return self.key > other.key

class LeafNode:
    def __init__(self):
        self.selfPointer = None
        self.nextLeaf = None
        self.elements = [] # Note: This list must be sorted by key

    def findData(self, key):
        i = bisect.bisect_left(self.elements, LeafElement(key, None))
        if i != len(self.elements) and self.elements[i].key == key:
            return self.elements[i].data
        raise KeyError

    def __getitem__(self, key):
        return self.findData(key)

    # Note: Since self.elements must be sorted, this should be used with care
    def addElement(self, key, data):
        self.elements.append(LeafElement(key, data))

    def getDebugInfo(self):
        return 'Self Pointer: {0}\nNext Leaf: {1}\nElements: {2}'.format(
                self.selfPointer,
                self.nextLeaf,
                len(self.elements)
            )
