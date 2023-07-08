from random import uniform, random

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
    
    def relu(self) -> None:
        ''' Atualiza a matriz com a função de ativação ReLU '''

        for row in self.matrix:
            for i in range(len(row)):
                row[i] = max(0, row[i])
    
    def randomize(self) -> None:
        ''' Modifica a matriz para valores aleatórios '''
        
        for row in self.matrix:
            for i in range(len(row)):
                row[i] = uniform(-1, 1)
    
    def mutate(self) -> None:
        ''' Cria mutações nos valores da matriz '''
        
        mutation_rate = random()
        
        for row in self.matrix:
            for i in range(len(row)):
                if random() > mutation_rate:
                    continue
                
                row[i] = max(-1, (min(1, row[i] + uniform(-1, 1))))
    
    def to_array(self) -> list[float]:
        ''' Transforma a matriz em um array '''
        
        return [item for row in self.matrix for item in row]
    
    @staticmethod
    def from_array(array: list[float]) -> 'Matrix':
        ''' Transforma um array em uma matriz '''
        
        result = Matrix(len(array), 1)

        for i, value in enumerate(array):
            result.matrix[i][0] = value          
        
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
    
    def __str__(self) -> str:
        ''' Cria uma string para representar a matriz '''
        
        max_size = max([len(str(i)) for i in self.to_array()])
        
        string = ''
        
        for i, row in enumerate(self.matrix):
            string += '['
            
            for j, item in enumerate(row):
                space = 0 if j == 0 else 1
                
                string += str(item).rjust(max_size + space)

            string += ']'
        
            if i + 1 != len(self.matrix):    
                string += '\n'
        
        return string