from random import random, randint

class Matrix:
    ''' Classe que representa uma matriz '''
    
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        
        self.matrix: list[list[float]] = [[0 for _ in range(cols)] for _ in range(rows)]
    
    def add_bias(self) -> None:
        ''' Adiciona uma linha nova para o BIAS '''
        
        self.rows += 1
        self.matrix.append([1] * self.cols)
    
    def activate(self) -> None:
        ''' Atualiza a matriz com a função de ativação ReLU '''

        for row in self.matrix:
            for i in range(len(row)):
                row[i] = max(0, row[i])
    
    def randomize(self) -> None:
        ''' Modifica a matriz para valores aleatórios '''
        
        for row in self.matrix:
            for i in range(len(row)):
                row[i] = (random() * 2) - 1
    
    def mutate(self) -> None:
        ''' Cria mutações nos valores da matriz '''
        
        mutation_rate = random() / 2
        
        for row in self.matrix:
            for i in range(len(row)):
                if random() > mutation_rate:
                    continue
                
                row[i] += max(-1, min(1, (random() * 2) - 1))
    
    def clone(self):
        ''' Cria uma cópia da matriz '''
        
        result = Matrix(self.rows, self.cols)
        
        for i in range(self.rows):
            for j in range(self.cols):
                result.matrix[i][j] = self.matrix[i][j]
        
        return result
        
    def to_array(self) -> list[float]:
        ''' Transforma a matriz em um array '''
        
        return [item for row in self.matrix for item in row]
    
    @staticmethod
    def load(matrix: list[list[float]]) -> 'Matrix':
        ''' Carrega uma matriz '''
        
        result = Matrix(len(matrix), len(matrix[0]))
        
        for i in range(result.rows):
            for j in range(result.cols):
                result.matrix[i][j] = matrix[i][j]
        
        return result
    
    @staticmethod
    def from_array(array: list[float]) -> 'Matrix':
        ''' Transforma um array em uma matriz '''
        
        result = Matrix(len(array), 1)

        for i, value in enumerate(array):
            result.matrix[i][0] = value          
        
        return result
    
    @staticmethod
    def crossover(a: 'Matrix', b: 'Matrix') -> 'Matrix':
        ''' Cria um cruzamento entre duas matrizes '''
        
        if (a.rows, a.cols) != (b.rows, b.cols):
            raise ValueError('Matrices must have the same size')
        
        rand_row = randint(0, a.rows - 1)
        rand_col = randint(0, a.cols - 1)
        
        result: Matrix = Matrix(a.rows, a.cols)
        
        for i in range(a.rows):
            for j in range(a.cols):
                if i < rand_row or (i == rand_row and j <= rand_col):
                    result.matrix[i][j] = a.matrix[i][j]
                else:
                    result.matrix[i][j] = b.matrix[i][j]
                
        return result
    
    @staticmethod
    def multiply(a: 'Matrix', b: 'Matrix') -> 'Matrix':
        ''' Multiplica duas matrizes '''
        
        result: Matrix = Matrix(a.rows, b.cols)
        
        if a.cols != b.rows: 
            return result
        
        for i in range(a.rows):
            for j in range(b.cols):   
                for k in range(a.cols):
                    result.matrix[i][j] += a.matrix[i][k] * b.matrix[k][j]
        
        return result