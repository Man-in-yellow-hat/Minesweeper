from time import sleep


class Solver:
    def __init__(self, board):
        self.board = board
        self.lastGuess = True
        self.guesses = 0

    def solveBasic(self):
        updated = False
        for row in self.board.getBoard():
            for piece in row:
                seen = piece.getAsSeen()
                if 1 <= seen < 9:
                    if piece.doClickedNeighbors() == len(piece.getNeighbors()) - seen:
                        for neighbor in piece.getNeighbors():
                            if not neighbor.getIsClicked() and neighbor.getAsSeen() != 10:
                                self.board.handleClick(neighbor, True)
                                updated = True

                    if piece.doFlaggedNeighbors() == seen:
                        for neighbor in piece.getNeighbors():
                            if not neighbor.getIsClicked() and not neighbor.getFlagged():
                                self.board.handleClick(neighbor, False)
                                updated = True
        return updated

    def solveGroup(self):
        updated = False
        for row in self.board.getBoard():
            for piece in row:
                if piece.getIsClicked():
                    for neighbor in piece.getNeighbors():
                        combinedGroup = piece.getGroup().intersection(neighbor.getGroup())
                        if len(combinedGroup) == 2 and neighbor.getIsClicked() and piece.doNumToFlag() == 1 and (2 <= len(piece.getGroup()) <= 3):
                            if len(neighbor.getGroup()) >= 3:
                                for newNeighbor in neighbor.getGroup():
                                    if newNeighbor not in combinedGroup and not newNeighbor.getIsClicked() and not newNeighbor.getFlagged():
                                        if neighbor.doNumToFlag() == 1  and len(piece.getGroup()) == 2:
                                            self.board.handleClick(newNeighbor, False)
                                            updated = True
                                        elif neighbor.doNumToFlag() == 2 and len(neighbor.getGroup()) == 3:
                                            self.board.handleClick(newNeighbor, True)
                                            updated = True
        return updated

    def guess(self):
        for row in self.board.getBoard():
            for piece in row:
                if piece.getIsClicked():
                    pass
                else:
                    if not self.board.getWon() and not piece.getFlagged():
                        if self.board.getNumToFlag() == 0:
                            self.board.handleClick(piece, False)
                        elif self.board.getNumToFlag() == 1:
                            if self.lastGuess:
                                self.guesses += 1
                                print("guess solving! guesses: ", self.guesses)
                                self.board.handleClick(piece, False)
                                self.lastGuess = False


