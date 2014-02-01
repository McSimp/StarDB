class BlockStorage:
    def __init__(self):
        self.isOpen = False

    def checkIfOpen(self, methodName, mustBeOpen):
        if mustBeOpen and not self.isOpen:
            raise Exception('BlockStorage method "{0}" called when not open, must be open'.format(methodName))

        if not mustBeOpen and self.isOpen:
            raise Exception('BlockStorage method "{0}" called when open, cannot call when open'.format(methodName))

    def readBlock(self, blockIndex, blockOffset = 0, size = None):
        raise NotImplementedError()

    def readUserData(self, dataOffset, size):
        raise NotImplementedError()

    def open(self):
        raise NotImplementedError()
