from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from game.game import Game

class Snake:
    ''' Classe que representa a cobrinha '''
    
    def __init__(self, game: 'Game'):
        self.game = game

        self.initial_coords = self.get_initial_coords()

        self.coords: list[tuple[float, float]] = []
        self.direction: Literal['up', 'right', 'down', 'left'] = 'right'
    
    def reset(self):
        ''' Reseta a cobrinha '''
        
        self.coords.clear()
        self.direction = 'right'
        
        
        self.game.canvas.undraw_snake()
        
        for coord in self.initial_coords:
            self.add_coord(coord)
    
    def add_coord(self, coord: tuple[float, float]):
        ''' Adiciona uma coordenada à cobrinha '''
        
        self.coords.append(coord)
        
        self.game.canvas.draw_snake(coord, self.game.grid)
    
    def remove_coord(self, coord: tuple[float, float]):
        ''' Remove uma coordenada da cobrinha '''
        
        idx = self.coords.index(coord)
        self.coords.pop(idx)
        
        self.game.canvas.undraw_snake(idx)
    
    def set_direction(self, direction: str):
        ''' Define a direção da cobrinha'''
        
        if direction in ('up', 'w') and self.direction != 'down':
            self.direction = 'up'
        elif direction in ('right', 'd') and self.direction != 'left':
            self.direction = 'right'
        elif direction in ('down', 's') and self.direction != 'up':
            self.direction = 'down'
        elif direction in ('left', 'a') and self.direction != 'right':
            self.direction = 'left'
    
    def get_next_coord(self):
        ''' Retorna a próxima coordenada da cobrinha '''
        
        x, y = self.coords[-1]
        
        match(self.direction):
            case 'up': 
                return (x, y - 1)
            case 'right': 
                return (x + 1, y)
            case 'down': 
                return (x, y + 1)
            case 'left' | _: 
                return (x - 1, y)
    
    def get_initial_coords(self):
        ''' Retorna as coordenadas iniciais da cobrinha '''
        x = int(self.game.grid / 4)
        y = int(self.game.grid / 2)

        return [(x + i, y) for i in range(3)]
    
    def get_score(self):
        ''' Retorna a pontuação do jogador '''
        
        return len(self.coords) - len(self.initial_coords)