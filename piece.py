class Piece:
    def __init__(self, hasBomb, location=None):
        self.neighborsWithBomb = 0
        self.hasBomb = hasBomb
        self.clicked = False
        self.flagged = False
        self.clickedNeighbors = 0
        self.flaggedNeighbors = 0
        self.asSeen = 9
        self.possibleClicks = set()
        self.numToFlag = 0
        self.location = location
        self.neighbors = []

    def setAsSeen(self, setTo):
        self.asSeen = setTo

    def getAsSeen(self):
        return self.asSeen

    def addBomb(self):
        self.hasBomb = True

    def removeBomb(self):
        self.hasBomb = False

    def getHasBomb(self):
        return self.hasBomb

    def getIsClicked(self):
        return self.clicked

    def getFlagged(self):
        return self.flagged

    def toggleFlag(self):
        self.flagged = not self.getFlagged()
        if self.getFlagged():
            self.setAsSeen(10)
            return -1
        else:
            return 1

    def setPossibleClicks(self):
        self.possibleClicks = set()
        for neighbor in self.getNeighbors():
            if (not neighbor.getIsClicked()) and (not neighbor.getFlagged()):
                self.possibleClicks.add(neighbor)

    def getGroup(self):
        self.setPossibleClicks()
        return self.possibleClicks

    def clickPiece(self):
        self.clicked = True

    def setNeighbors(self, neighbors):
        self.neighbors = neighbors
        for neighbor in neighbors:
            if neighbor.getHasBomb():
                self.neighborsWithBomb += 1

    def doClickedNeighbors(self):
        self.clickedNeighbors = 0
        for neighbor in self.getNeighbors():
            if neighbor.getIsClicked():
                self.clickedNeighbors += 1
        return self.clickedNeighbors

    def doNumToFlag(self):
        self.numToFlag = self.getNeighborsWithBomb() - self.doFlaggedNeighbors()
        return self.numToFlag

    def doFlaggedNeighbors(self):
        self.flaggedNeighbors = 0
        for neighbor in self.getNeighbors():
            if neighbor.getFlagged():
                self.flaggedNeighbors += 1
        return self.flaggedNeighbors

    def getNeighborsWithBomb(self):
        return self.neighborsWithBomb

    def getNeighbors(self):
        return self.neighbors

