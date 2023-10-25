class Screen:
    def __init__(self, numFlags):
        self.displayedNumBombs = numFlags

    def getNumFlags(self):
        if self.displayedNumBombs < 0:
            return 0
        else:
            return self.displayedNumBombs

    def updateNumFlags(self, addOrSubtractFlag):
        self.displayedNumBombs += addOrSubtractFlag



