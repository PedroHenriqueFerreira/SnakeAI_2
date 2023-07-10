from typing import TYPE_CHECKING
from tkinter import Misc, Canvas as BaseCanvas
from settings import *

if TYPE_CHECKING:
    from game.game import Game

class Canvas(BaseCanvas):
    def __init__(self, parent: Misc, size: int):
        super().__init__(parent, width=size, height=size, highlightthickness=0)
    
    def draw_text(self, coord: tuple[int, int], text: str, color: str, font: tuple[str, int], tags: str) -> int:
        return self.create_text(
            *coord,
            text=text,
            fill=color,
            font=font,
            tags=tags
        )
        
    def draw_pixel(self, coord: tuple[int, int], grid: int, color: str, tags: str) -> int:
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
        if coord is None:
            return
        
        return self.draw_pixel(coord, grid, COLORS['red'], 'food')
    
    def undraw_food(self) -> None:
        self.delete('food')
    
    def draw_snake(self, coord: tuple[int, int], grid: int) -> None:
        self.draw_pixel(coord, grid, COLORS['blue'], 'snake')
        
    def undraw_snake(self, idx: int | None = None) -> None:
        if idx is None:
            self.delete('snake')
        else:
            self.delete(self.find_withtag('snake')[idx])
        
    def draw_bg(self, grid: int) -> None:
        self.draw_pixel((0, 0), 1, COLORS['light_green'], 'bg')
        
        for x in range(grid):
            for y in range(grid):
                if (x + y) % 2 == 0:
                    self.draw_pixel((x, y), grid, COLORS['dark_green'], 'bg')
                    
    def draw_message(self, message: str) -> None: 
        self.draw_pixel((0, 0), 1, COLORS['gray'], 'message')
        
        center = int(self.winfo_reqwidth() / 2)
        
        self.draw_text((center, center), message, COLORS['white'], MESSAGE_FONT, 'message')
        
    def undraw_message(self) -> None:
        self.delete('message')
    
    def draw_line( self, origin: tuple[int, int], destiny: tuple[int, int], size: int, color: str, tags: str) -> int:
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
        return self.create_polygon(
            *[pos for coord in coords for pos in coord],
            fill='',
            width=width,
            outline=color,
            tags=tags
        )
    
    def draw_chart(self, values: list[int]) -> None:
        size = self.winfo_reqwidth()
        
        if len(self.find_withtag('line')) == 0:
            block_size = int(size / CHART_GRID)

            for i in range(CHART_GRID + 1):
                pos = i * block_size

                self.draw_line((0, pos), (size, pos), LINE_WIDTH, COLORS['gray'], 'line')
                self.draw_line((pos, 0), (pos, size), LINE_WIDTH, COLORS['gray'], 'line')

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
        self.draw_polygon(coords, LINE_WIDTH, COLORS['red'], 'chart')
    
    def draw_game(self, game: 'Game'):
        if len(self.find_withtag('bg')) == 0:
            self.draw_bg(GAME_GRID)
        
        self.delete('food')
        if game.food.coord is not None:
            self.draw_food(game.food.coord, GAME_GRID)
        
        self.delete('snake')
        for snake_coord in game.snake.coords:
            self.draw_snake(snake_coord, GAME_GRID)