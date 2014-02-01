import bisect

class IndexElement:
    def __init__(self, k, p):
        self.key = k
        self.pointer = p

    def __lt__(self, other):
        return self.key < other.key

    def __gt__(self, other):
        return self.key > other.key

class IndexNode:
    def __init__(self):
        self.selfPointer = None
        self.level = None
        self.beginPointer = None
        self.pointers = [] # Note: This list must be sorted by key

    # Note: This will not return the location of the key's IndexElement if the key is
    # not in the index - it'll return the position where it should be inserted. This is
    # used internally to figure out which branch of the tree to go down.
    def find(self, key):
        i = bisect.bisect_left(self.pointers, IndexElement(key, None))
        if i != len(self.pointers) and self.pointers[i].key == key:
            return i + 1
        else:
            return i

    def size(self):
        if self.beginPointer is not None:
            return len(self.pointers) + 1
        else:
            return 0

    def pointer(self, i):
        if i == 0:
            return self.beginPointer
        else:
            return self.pointers[i - 1].pointer

    # Note: Since self.pointers must be sorted, this should be used with care
    def addPointer(self, key, pointer):
        self.pointers.append(IndexElement(key, pointer))

    def getDebugInfo(self):
        return 'Self Pointer: {0}\nLevel: {1}\nBegin Pointer: {2}\nPointers: {3}'.format(
                self.selfPointer,
                self.level,
                self.beginPointer,
                len(self.pointers)
            )
