import pygame
import os
import sys
from time import sleep
from random import randint
pygame.font.init()
myFont = pygame.font.SysFont('arial', 50)


class Game:
    def __init__(self, board, screenSize, screen, solver, solveGuess):
        self.board = board
        self.solver = solver
        self.boardSize = (screenSize[0], screenSize[1] + 40)
        self.screenSize = screenSize
        self.screen = pygame.display.set_mode(self.boardSize)
        self.pieceSize = self.screenSize[0] // self.board.getSize()[1], \
                         self.screenSize[1] // self.board.getSize()[0]
        self.sounds = self.getSounds()
        self.started = False
        self.displayScreen = screen
        self.timeStamp = 0
        self.loadImages()
        self.manualSolve = solveGuess[0]
        self.guess = solveGuess[1]

    def run(self):
        pygame.init()
        running = True
        start_time = pygame.time.get_ticks()
        while running:
            if 0 < (pygame.time.get_ticks() - start_time) % 1000 < 50:
                # delay so that if is caught, cannot run again for another 50 sec so no skips
                self.timeStamp += 1
                pygame.time.delay(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    if self.inBounds(position):
                        rightClick = pygame.mouse.get_pressed()[2]
                        self.handleClick(position, rightClick, False)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    position = pygame.mouse.get_pos()
                    if self.inBounds(position):
                        self.handleClick(position, False, True)
                if not self.started and self.board.numClicked == 0 and event.type == pygame.KEYDOWN\
                        and event.key == pygame.K_s:
                    self.started = True
                    self.board.firstBlock()
            self.draw()
            pygame.display.flip()
            if self.board.getWon():
                # sound = self.sounds[1][randint(0, len(self.sounds[1]) - 1)]
                # sound.play()
                sleep(2)
                running = False
            if self.board.getLost():
                # sound = self.sounds[0][randint(0, len(self.sounds[0]) - 1)]
                # sound.play()
                # sleep(6)
                sleep(2)
                running = False
            # sleep(.15)
            if self.manualSolve:
                continue
            else:
                if not self.solver.solveBasic() and not self.solver.solveGroup() and \
                        (pygame.time.get_ticks() - start_time) > 500 and self.guess:
                    self.solver.guess()


        pygame.quit()
        sys.exit()

    def inBounds(self, position):
        return position[0] < self.screenSize[0] - 8 and position[1] < self.screenSize[1] - 10

    def draw(self):
        text = myFont.render(str(self.displayScreen.getNumFlags()) + "   ", False, (255, 255, 255), (0, 0, 0))
        timeText = myFont.render(str(self.getTime()) + "   ", False, (255, 255, 255), (0, 0, 0))
        self.screen.blit(text, (20, self.screenSize[1]))
        self.screen.blit(timeText, (self.screenSize[0] - 120, self.screenSize[1]))

        topLeft = (0, 0)
        for row in range(self.board.getSize()[0]):
            for col in range(self.board.getSize()[1]):
                piece = self.board.getPiece((row, col))
                image = self.getImage(piece)
                self.screen.blit(image, topLeft)
                topLeft = topLeft[0] + self.pieceSize[0], topLeft[1]
            topLeft = 0, topLeft[1] + self.pieceSize[1]

    def getTime(self):
        return self.timeStamp

    def getSounds(self):
        sounds = [[], []]
        for fileName in os.listdir("loseSounds"):
            string = "loseSounds/" + fileName
            sound = pygame.mixer.Sound(string)
            sounds[0].append(sound)
        for fileName in os.listdir("winSounds"):
            string = "winSounds/" + fileName
            sound = pygame.mixer.Sound(string)
            sounds[1].append(sound)
        return sounds

    def loadImages(self):
        # now we have dictionary containing images (without .png)
        self.images = {}
        for fileName in os.listdir("images"):
            if not fileName.endswith(".png"):
                continue
            image = pygame.image.load(r"images/" + fileName)
            image = pygame.transform.scale(image, self.pieceSize)
            self.images[fileName.split(".")[0]] = image

    def getImage(self, piece):
        # string = "unclicked-bomb" if piece.getHasBomb() else str(piece.getNeighborsWithBomb())
        if self.board.getLost() and piece.getHasBomb():
            if piece.getIsClicked():
                string = "bomb-at-clicked-block"
            else:
                if piece.getFlagged():
                    string = "flag"
                else:
                    string = "unclicked-bomb"
        elif piece.getIsClicked():
            if piece.getFlagged():
                if not piece.getHasBomb():
                    string = "wrong-flag"
            else:
                if piece.getHasBomb():
                    string = "bomb-at-clicked-block"
                else:
                    string = str(piece.getNeighborsWithBomb())
                    piece.setAsSeen(piece.getNeighborsWithBomb())
        else:
            if piece.getFlagged():
                if self.board.getLost():
                    string = "wrong-flag"
                else:
                    string = "flag"
            else:
                string = "empty-block"
        return self.images[string]

    def handleClick(self, position, rightClick, space):
        # handles a click, right click, or space click
        index = position[1] // self.pieceSize[1], position[0] // self.pieceSize[0]
        piece = self.board.getPiece(index)
        if space:
            self.board.handleSpace(piece)
        else:
            self.board.handleClick(piece, rightClick)


