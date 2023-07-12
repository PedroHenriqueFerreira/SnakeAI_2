from tkinter import Event

from ai.neural_network import NeuralNetwork

from ui.canvas import Canvas

from game.food import Food
from game.snake import Snake

class Game:
    ''' Classe que representa o jogo '''
    
    def __init__(
        self, 
        canvas: Canvas, 
        grid: int, 
        lives: int, 
        speed: int, 
        is_ai: bool, 
        nn: NeuralNetwork | None = None
    ):
        self.canvas = canvas
        
        self.speed = speed
        self.is_ai = is_ai
        self.grid = grid
        self.lives = lives
        self.curr_lives = lives
        self.energy = grid ** 2
        self.curr_energy = grid ** 2
        self.score = 0
        self.is_dead = True
        
        self.brain = nn

        self.canvas.draw_bg(grid)
        self.canvas.draw_message('Jogar Snake')
        
        self.snake = Snake(self)
        self.food = Food(self)
        
        if not is_ai:
            self.canvas.bind('<Key>', self.control)
            self.canvas.focus_set()
    
    def ai_control(self, output: list[float]) -> None:
        ''' Controla a cobrinha pelo algoritmo '''
        
        if len(output) != 4:
            raise ValueError('Output must have 4 values')
        
        if output[0] > 0:
            self.snake.set_direction('up')
        elif output[1] > 0:
            self.snake.set_direction('right')
        elif output[2] > 0:
            self.snake.set_direction('down')
        elif output[3] > 0:
            self.snake.set_direction('left')
    
    def control(self, event: 'Event[Canvas]') -> None:
        ''' Controla a cobrinha pelo teclado '''
        
        self.snake.set_direction(event.keysym.lower())
    
        if self.is_dead:
            self.reset()
            
    def reset(self):
        ''' Reseta o jogo '''
        
        self.canvas.undraw_message()
        
        if self.curr_lives == 0 or self.curr_lives == self.lives:
            self.curr_lives = self.lives
            self.score = 0
            
        self.curr_energy = self.energy
        
        self.is_dead = False
        
        self.snake.reset()
        self.food.reset()
        
        self.update()
    
    def die(self):
        ''' Mata a cobrinha '''
        
        self.curr_lives -= 1
        
        if self.curr_lives > 0:
            return self.reset()
        
        self.is_dead = True
        
        self.canvas.draw_message(f'Pontuacao: {self.score}')
        
    def update(self):
        ''' Atualiza o jogo '''
        
        if self.is_dead: 
            return
        
        next_coord = self.snake.get_next_coord()
    
        bodyCollision = next_coord in self.snake.coords
        wallCollision = -1 in next_coord or self.grid in next_coord
        
        if bodyCollision or wallCollision or self.curr_energy == 0:
            return self.die()
        
        self.snake.add_coord(next_coord)
        
        if next_coord == self.food.coord:
            self.food.reset()
            self.curr_energy = self.energy
        else:
            self.snake.remove_coord(self.snake.coords[0])
            self.curr_energy -= 1
            
        curr_score = self.snake.get_score()
        
        if curr_score > self.score:
            self.score = curr_score
            
        self.canvas.after(self.speed, self.update)
        
    def get_data(self):
        *snake_body, snake_head = self.snake.coords
        
        food_data: list[int] = []
        vision_data: list[int] = []
        
        for i in range(2):
            if self.food.coord[i] < snake_head[i]:
                food_data.append(1)
            elif self.food.coord[i] > snake_head[i]:
                food_data.append(-1)
            else:
                food_data.append(0)
    
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    continue
                
                coord = (snake_head[0] + i, snake_head[1] + j)
                
                x, y = coord
                
                if coord in snake_body or x < 0 or y < 0 or x >= self.grid or y >= self.grid:
                    vision_data.append(1)
                else:
                    vision_data.append(0)
        
        up = (snake_head[0] - 2, snake_head[1])
        right = (snake_head[0], snake_head[1] + 2)
        down = (snake_head[0] + 2, snake_head[1])
        left = (snake_head[0], snake_head[1] - 2)
        
        for coord in (up, right, down, left):
            if coord in snake_body or x < 0 or y < 0 or x >= self.grid or y >= self.grid:
                vision_data.append(1)
            else:
                vision_data.append(0)
        
        return food_data + vision_data