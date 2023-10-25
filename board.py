from piece import Piece
from random import random, randint


class Board:
    def __init__(self, size, correctNumBomb, screen, testBoard):
        self.board = []
        self.size = size
        self.prob = correctNumBomb / (size[0] * size[1])
        self.correctNumBomb = correctNumBomb
        self.numToFlag = correctNumBomb
        self.lost = False
        self.numClicked = 0
        self.numNonBomb = size[0] * size[1] - correctNumBomb
        self.numBomb = 0
        self.numFlags = 0
        self.screen = screen
        if testBoard:
            self.SETTESTBOARD()
        else:
            self.setBoard()

    def setBoard(self):
        # board is a list of row lists
        y = 0
        for row in range(self.size[0]):
            x = 0
            row = []
            for col in range(self.size[1]):
                hasBomb = random() < self.prob
                if hasBomb:
                    self.numBomb += 1
                piece = Piece(hasBomb, [x, y])
                row.append(piece)
                x += 1
            self.board.append(row)
            y += 1
        if self.getNumBomb() != self.getCorrectNumBomb():
            if self.getNumBomb() < self.getCorrectNumBomb():
                bombToAdd = self.getCorrectNumBomb() - self.getNumBomb()
                while bombToAdd != 0:
                    piece = self.getPiece((randint(0, self.size[0] - 1), randint(0, self.size[1] - 1)))
                    while piece.getHasBomb():
                        piece = self.getPiece((randint(0, self.size[0] - 1), randint(0, self.size[1] - 1)))
                    piece.addBomb()
                    self.numBomb += 1
                    bombToAdd -= 1
            elif self.getNumBomb() > self.getCorrectNumBomb():
                bombToRemove = self.getNumBomb() - self.getCorrectNumBomb()
                while bombToRemove != 0:
                    piece = self.getPiece((randint(0, self.size[0] - 1), randint(0, self.size[1] - 1)))
                    while not piece.getHasBomb():
                        piece = self.getPiece((randint(0, self.size[0] - 1), randint(0, self.size[1] - 1)))
                    piece.removeBomb()
                    self.numBomb -= 1
                    bombToRemove -= 1
        self.setNeighbors()

    def firstBlock(self):
        xRange = ((self.getSize()[0] // 2) - (self.getSize()[0] // 10),
                  (self.getSize()[0] // 2) + (self.getSize()[1] // 10))
        yRange = ((self.getSize()[1] // 2) - (self.getSize()[1] // 10),
                  (self.getSize()[1] // 2) + (self.getSize()[1] // 10))
        piece = self.getPiece([randint(xRange[0], xRange[1]), randint(yRange[0], yRange[1])])
        count = 0
        while piece.getNeighborsWithBomb() != 0 or piece.getHasBomb():
            if count > 50:
                xRange = (0, self.getSize()[0] - 1)
                yRange = (0, self.getSize()[1] - 1)
            x = randint(xRange[0], xRange[1])
            y = randint(yRange[0], yRange[1])
            piece = self.getPiece([x, y])
            count += 1
        self.handleClick(piece, False)

    def setNeighbors(self):
        # set neighbors for each piece using getListNeighbors
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                piece = self.getPiece((row, col))
                neighbors = self.getListNeighbors((row, col))
                piece.setNeighbors(neighbors)

    def getListNeighbors(self, index):
        # finds neighbors for a piece and returns list of neighbors
        neighbors = []
        for row in range(index[0] - 1, index[0] + 2):
            for col in range(index[1] - 1, index[1] + 2):
                outOfBounds = row < 0 or row >= self.size[0] or col < 0 or col >= self.size[1]
                same = row == index[0] and col == index[1]
                if same or outOfBounds:
                    continue
                neighbors.append(self.getPiece((row, col)))
        return neighbors

    def getNumToFlag(self):
        return self.numToFlag

    def getSize(self):
        return self.size

    def getPiece(self, index):
        return self.board[index[0]][index[1]]

    def getNumBomb(self):
        return self.numBomb

    def getCorrectNumBomb(self):
        return self.correctNumBomb

    def handleClick(self, piece, flagToggle):
        if not piece.getIsClicked():
            if flagToggle:
                tempFlag = piece.toggleFlag()
                self.numFlags -= tempFlag
                self.numToFlag += tempFlag
                self.screen.updateNumFlags(tempFlag)
                return
            if piece.getFlagged():
                return
            piece.clickPiece()
            if piece.getHasBomb():
                self.lost = True
                return
            self.numClicked += 1
            if piece.getNeighborsWithBomb() == 0:
                for neighbor in piece.getNeighbors():
                    self.handleClick(neighbor, False)

    def handleSpace(self, piece):
        if not piece.getIsClicked():
            tempFlag = piece.toggleFlag()
            self.numFlags -= tempFlag
            self.numToFlag += tempFlag
            self.screen.updateNumFlags(tempFlag)
            return
        else:
            flaggedNeighbors = 0
            neighborsToCheck = []
            for neighbor in piece.getNeighbors():
                if neighbor.getFlagged():
                    flaggedNeighbors += 1
                    if not neighbor.getHasBomb():
                        neighborsToCheck.append(neighbor)
                else:
                    if not neighbor.getIsClicked():
                        neighborsToCheck.append(neighbor)
            if flaggedNeighbors == piece.getNeighborsWithBomb():
                for neighbor in neighborsToCheck:
                    self.handleClick(neighbor, False)
                    if not neighbor.getFlagged():
                        neighbor.clickPiece()
                        self.numClicked += 1

    def getBoard(self):
        return self.board

    def getNumClicked(self):
        return self.numClicked

    def getNumNonBomb(self):
        return self.numNonBomb

    def getLost(self):
        return self.lost

    def getWon(self):
        return self.getNumNonBomb() == self.getNumClicked()

    def SETTESTBOARD(self):
        row1 = [Piece(False, [0, 0]), Piece(False, [0, 1]), Piece(True, [0, 2]), Piece(False, [0, 3])]
        row2 = [Piece(False, [1, 0]), Piece(False, [1, 1]), Piece(True, [1, 2]), Piece(True, [1, 3])]
        row3 = [Piece(False, [2, 0]), Piece(False, [2, 1]), Piece(True, [2, 2]), Piece(True, [2, 3])]
        row4 = [Piece(False, [3, 0]), Piece(False, [3, 1]), Piece(False, [3, 2]), Piece(False, [3, 3])]
        self.board.append(row1)
        self.board.append(row2)
        self.board.append(row3)
        self.board.append(row4)
        self.numBomb = self.getCorrectNumBomb()
        self.setNeighbors()