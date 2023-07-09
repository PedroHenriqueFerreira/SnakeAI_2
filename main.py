from tkinter import Tk
from ui.canvas import Canvas

from game.game import Game

from settings import *

root = Tk()

canvas = Canvas(root, GAME_SIZE)
canvas.pack()

Game(canvas)

root.mainloop()