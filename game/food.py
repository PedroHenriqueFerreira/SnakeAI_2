from typing import TYPE_CHECKING
from random import choice

from settings import *

if TYPE_CHECKING:
    from game.game import Game

class Food:
    ''' Classe que representa a comida '''
    
    def __init__(self, game: 'Game'):
        self.game = game

        self.coord: tuple[float, float] | None = None

    def reset(self):
        ''' Reseta a comida '''
        
        self.coord = self.get_random_coord()
        
        self.game.canvas.undraw_food()
        self.game.canvas.draw_food(self.coord, self.game.grid)

    def get_random_coord(self):
        ''' Posição aleatória para a comida que não esteja no corpo da cobrinha '''
        
        coords: list[tuple[float, float]] = []
        
        for x in range(self.game.grid):
            for y in range(self.game.grid):
                coord = (x, y)
                if coord in self.game.snake.coords:
                    continue
                
                coords.append(coord)

        if len(coords) == 0:
            return None

        return choice(coords)