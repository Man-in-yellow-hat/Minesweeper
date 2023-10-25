from game import Game
from board import Board
from screen import Screen
from solver import Solver
import pygame

pygame.init()

# set test = 1 to test
test = 0

# if true, will not attempt to solve automatically
manualSolve = False
if manualSolve:
    guess = False
else:
    # if true (and not manually solving), will guess until win or loss
    guess = True


difficulties = {"beginner": [9, 9, 10, 800, 800], "intermediate": [16, 16, 40, 800, 800],
                "expert": [16, 30, 99, 1200, 640], "cracked": [100, 100, 1600, 800, 800],
                "dumbass": [5, 5, 20, 400, 400], "test": [4, 4, 5, 400, 400]}
if test == 1:
    difficulty = difficulties["test"]
else:
    difficulty = difficulties["expert"]
size = (difficulty[0], difficulty[1])
correctNumBombs = difficulty[2]
screen = Screen(correctNumBombs)
board = Board(size, correctNumBombs, screen, test)
screenSize = (difficulty[3], difficulty[4])
solver = Solver(board)
game = Game(board, screenSize, screen, solver, (manualSolve, guess))
game.run()
