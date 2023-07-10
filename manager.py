from tkinter import Label

from game.game import Game
from ui.canvas import Canvas

from settings import *

class Manager:
    def __init__(
        self,
        games: list[Game],
        
        nn_canvas: Canvas,
        chart_canvas: Canvas,
        best_game_canvas: Canvas,
        
        generation_label: Label,
        record_label: Label,
        score_label: Label,
        alive_label: Label
    ):
        self.games = games

        self.chart_canvas = chart_canvas
        self.nn_canvas = nn_canvas
        self.best_game_canvas = best_game_canvas

        self.record_label = record_label
        self.score_label = score_label
        self.alive_label = alive_label
        self.generation_label = generation_label
    
        self.chart_canvas.draw_chart([])
        self.score_history: list[int] = [0]
    
        self.load_data()
        
        for snake_game in games:
            snake_game.reset()
            
        self.update()

    def transform_output(self, output: list[float]) -> str:
        if output[0] > 0: return 'up'
        elif output[1] > 0: return 'right'
        elif output[2] > 0: return 'down'
        elif output[3] > 0: return 'left'
        else: return 'right'

    def update(self):
        alive = 0
        
        curr_best_game = self.games[0]

        for game in self.games:
            if game.is_dead:
                continue

            alive += 1
            
            brain = game.brain

            if brain is not None:
                output = brain.output(game.get_data())
                game.ai_control(output)
            
            curr_score = game.snake.get_score()
            best_score = curr_best_game.snake.get_score()
            
            if curr_best_game.is_dead or curr_score > best_score:
                curr_best_game = game

        self.best_game_canvas.draw_game(curr_best_game)
        # self.nn_canvas.draw_neural_network(curr_best_game.brain)
        
        best_game = max(self.games, key=lambda game: game.score)

        self.score_label.config(text=SCORE_TEXT.replace('0', str(best_game.score)))
        self.alive_label.config(text=ALIVE_TEXT.replace('0', str(alive)))

        if alive == 0:
            self.score_history.append(best_game.score)
            self.chart_canvas.draw_chart(self.score_history)

            record = str(max(self.score_history))
            generation = str(len(self.score_history) - 1)

            self.record_label.config(text=RECORD_TEXT.replace('0', generation))
            self.generation_label.config(text=GENERATION_TEXT.replace('0', record))

            self.sort_games()
            self.save_data()
            
            self.natural_selection()

            for game in self.games:
                game.reset()

        self.best_game_canvas.after(SPEED, self.update)

    def save_data(self):
        sample: list[list[list[list[float]]]] = []
        
        for game in self.games[0:SAMPLE_SIZE]:
            if game.brain is None:
                continue
            
            wheights: list[list[list[float]]] = []
            
            for weight in game.brain.wheights:
                wheights.append(weight.matrix)
            
            sample.append(wheights)

        data = {
            'sample': sample,
            'score_history': self.score_history
        }

        with open(FILE_PATH, 'w') as file:
            file.write(str(data))

    def load_data(self):
        try:
            with open(FILE_PATH, 'r') as file:
                data = eval(file.read())

                for i, wheights in enumerate(data['sample']):
                    brain = self.games[i].brain
                    
                    if brain is None:
                        continue
                    
                    brain.load(wheights)
                    
                self.score_history = data['score_history']
                
                self.chart_canvas.draw_chart(self.score_history)
                
                record = str(max(self.score_history))
                generation = str(len(self.score_history) - 1)
                
                self.record_label.config(text=RECORD_TEXT.replace('0', record))
                self.generation_label.config(text=GENERATION_TEXT.replace('0', generation))

                self.natural_selection()
        finally:
            return

    def sort_games(self):
        self.games.sort(key=lambda snake_game: snake_game.score, reverse=True)

    def natural_selection(self):
        for i, game in enumerate(self.games[SAMPLE_SIZE:]):
            index = i % SAMPLE_SIZE
            
            brain = self.games[index].brain

            if brain is None:
                continue

            if game.brain is None:
                continue
            
            game.brain.load([wheight.matrix for wheight in brain.wheights])
            game.brain.mutate()
