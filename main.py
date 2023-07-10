from tkinter import Tk, Frame, Label

from manager import Manager

from ui.canvas import Canvas
from ai.neural_network import NeuralNetwork
from game.game import Game

from settings import *

win = Tk()
win.title('SnakeAI')
win.config(bg=COLORS['black'])
win.option_add('*background', COLORS['black'])
win.option_add('*foreground', COLORS['white'])

main = Frame(win)
main.pack(expand=1)

header = Frame(main)
header.grid(row=0, column=0, padx=PADDING, pady=PADDING)

labels: list[Label] = []

for i, text in enumerate([GENERATION_TEXT, RECORD_TEXT, SCORE_TEXT, ALIVE_TEXT]):
    label = Label(header, text=text, font=TEXT_FONT)
    label.grid(row=0, column=i, padx=PADDING, pady=PADDING)
    
    labels.append(label)
    
body = Frame(main)
body.grid(row=1, column=0, padx=PADDING, pady=PADDING)

left_frame = Frame(body)
left_frame.grid(row=0, column=0)
games: list[Game] = []

for i in range(GAMES_ROWS):
    for j in range(GAMES_COLS):
        game_canvas = Canvas(left_frame, GAME_SIZE)
        game_canvas.grid(row=i, column=j, padx=PADDING / 2, pady=PADDING / 2)
        
        nn = NeuralNetwork(INPUT_SIZE, HIDDEN_SIZES, OUTPUT_SIZE)
        game = Game(game_canvas, GAME_GRID, LIVES, SPEED, IS_AI, nn)
        
        games.append(game)
        
right_frame = Frame(body)
right_frame.grid(row=0, column=1)

best_game_canvas = Canvas(right_frame, BEST_GAME_SIZE)
best_game_canvas.grid(row=0, column=0, padx=PADDING, pady=PADDING)

chart_canvas = Canvas(right_frame, CHART_SIZE)
chart_canvas.grid(row=1, column=0, padx=PADDING, pady=PADDING)

nn_canvas = Canvas(right_frame, NEURAL_NETWORK_SIZE)
nn_canvas.grid(row=2, column=0, padx=PADDING, pady=PADDING)

Manager(games, nn_canvas, chart_canvas, best_game_canvas, *labels)

win_width = win.winfo_screenwidth()
win_height = win.winfo_screenheight()

win_x = int((win.winfo_screenwidth() - win_width) / 2)
win_y = int((win.winfo_screenheight() - win_height) / 2)

win.geometry(f'{win_width}x{win_height}+{win_x}+{win_y}')

win.mainloop()