from typing import TYPE_CHECKING
from tkinter import Misc, Canvas as BaseCanvas
from settings import *

if TYPE_CHECKING:
    from game.game import Game

class Canvas(BaseCanvas):
    ''' Classe que representa o canvas do jogo '''
    
    def __init__(self, parent: Misc, size: int):
        super().__init__(parent, width=size, height=size, highlightthickness=0)
    
    def draw_text(self, coord: tuple[int, int], text: str, color: str, font: tuple[str, int], tags: str) -> int:
        ''' Desenha um texto no canvas '''
        
        return self.create_text(
            *coord,
            text=text,
            fill=color,
            font=font,
            tags=tags
        )
        
    def draw_pixel(self, coord: tuple[int, int], grid: int, color: str, tags: str) -> int:
        ''' Desenha um pixel no canvas '''
        
        size = self.winfo_reqwidth() / grid
        
        x, y = coord
        
        return self.create_rectangle(
            x * size, y * size,
            x * size + size, y * size + size,
            width=0,
            fill=color,
            tags=tags
        )
        
    def draw_food(self, coord: tuple[int, int], grid: int) -> int:
        ''' Desenha a comida no canvas '''
        
        if coord is None:
            return
        
        return self.draw_pixel(coord, grid, FOOD_COLOR, 'food')
    
    def undraw_food(self) -> None:
        ''' Apaga a comida no canvas '''
        self.delete('food')
    
    def draw_snake(self, coord: tuple[int, int], grid: int) -> None:
        ''' Desenha a cobrinha no canvas '''
        
        self.draw_pixel(coord, grid, SNAKE_COLOR, 'snake')
        
    def undraw_snake(self, idx: int | None = None) -> None:
        ''' Apaga a cobrinha no canvas '''
        
        if idx is None:
            self.delete('snake')
        else:
            self.delete(self.find_withtag('snake')[idx])
        
    def draw_bg(self, grid: int) -> None:
        ''' Desenha o background do jogo no canvas '''
        
        self.draw_pixel((0, 0), 1, GRASS_COLORS[0], 'bg')
        
        for x in range(grid):
            for y in range(grid):
                if (x + y) % 2 == 0:
                    self.draw_pixel((x, y), grid, GRASS_COLORS[1], 'bg')
                    
    def draw_message(self, message: str) -> None: 
        ''' Desenha uma mensagem no canvas '''
        
        self.draw_pixel((0, 0), 1, BG_COLORS[1], 'message')
        
        center = int(self.winfo_reqwidth() / 2)
        
        self.draw_text((center, center), message, MESSAGE_COLOR, MESSAGE_FONT, 'message')
        
    def undraw_message(self) -> None:
        ''' Apaga a mensagem no canvas '''
        
        self.delete('message')
    
    def draw_line( self, origin: tuple[int, int], destiny: tuple[int, int], size: int, color: str, tags: str) -> int:
        ''' Desenha uma linha no canvas '''
        
        xi, yi = origin
        xf, yf = destiny
        
        return self.create_line(
            xi, yi,
            xf, yf,
            width=size,
            fill=color,
            tags=tags
        )
    
    def draw_polygon(self, coords: list[tuple[int, int]], width: int, color: str, tags: str) -> int:
        ''' Desenha um polígono no canvas '''
        
        return self.create_polygon(
            *[pos for coord in coords for pos in coord],
            fill='',
            width=width,
            outline=color,
            tags=tags
        )
    
    def draw_chart(self, values: list[int]) -> None:
        ''' Desenha um gráfico no canvas '''
        
        size = self.winfo_reqwidth()
        
        if len(self.find_withtag('line')) == 0:
            block_size = int(size / CHART_GRID)

            for i in range(CHART_GRID + 1):
                pos = i * block_size

                self.draw_line((0, pos), (size, pos), LINE_WIDTH, CHART_GRID_COLOR, 'line')
                self.draw_line((pos, 0), (pos, size), LINE_WIDTH, CHART_GRID_COLOR, 'line')

        if len(values) == 0 or max(values) == 0:
            return
        
        coords: list[tuple[int, int]] = []
        
        coords.append((-LINE_WIDTH, size + LINE_WIDTH))
    
        if len(values) > 1:
            for i, value in enumerate(values):
                x = int(i * (size / (len(values) - 1)))
                y = int(size - (value / max(values)) * size)

                if x == 0:
                    coords.append((x - LINE_WIDTH, y))
                    
                coords.append((x, y))

                if x == size:
                    coords.append((x + LINE_WIDTH, y))
        else:
            coords.append((size, 0))

        coords.append((size + LINE_WIDTH, size + LINE_WIDTH))

        self.delete('chart')
        self.draw_polygon(coords, LINE_WIDTH, FOOD_COLOR, 'chart')
    
    def draw_game(self, game: 'Game'):
        ''' Desenha o jogo no canvas '''
        
        if len(self.find_withtag('bg')) == 0:
            self.draw_bg(GAME_GRID)
        
        self.delete('food')
        if game.food.coord is not None:
            self.draw_food(game.food.coord, GAME_GRID)
        
        self.delete('snake')
        for snake_coord in game.snake.coords:
            self.draw_snake(snake_coord, GAME_GRID)