from tkinter import Misc, Canvas as BaseCanvas

from settings import *

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