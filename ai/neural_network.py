from ai.matrix import Matrix

class NeuralNetwork:
    ''' Classe que representa uma rede neural '''
    
    def __init__(
        self, 
        input_size: int, 
        hidden_sizes: list[int], 
        output_size: int
    ):  
        if len(hidden_sizes) == 0:
            raise ValueError('Hidden sizes must have at least one value')
        
        self.input_size = input_size
        self.hidden_sizes = hidden_sizes
        self.output_size = output_size
        
        self.wheights: list[Matrix] = []
        
        for i, curr_size in enumerate(hidden_sizes + [output_size]):
            prev_size = input_size if i == 0 else hidden_sizes[i - 1]
            
            weight = Matrix(curr_size, prev_size + 1)
            weight.randomize()
            
            self.wheights.append(weight)
            
    def output(self, inputs_array: list[float]) -> list[float]:
        ''' Calcula a saída da rede neural '''
        
        if len(inputs_array) != self.input_size:
            raise ValueError(f'Input size must be {self.input_size}')    
        
        curr_matrix: Matrix = Matrix.from_array(inputs_array)
        curr_matrix.add_bias()
        
        for i, wheight in enumerate(self.wheights):
            curr_matrix = Matrix.multiply(wheight, curr_matrix)
            curr_matrix.relu()
            
            if i + 1 == len(self.wheights):
                continue
                
            curr_matrix.add_bias()
            
        return curr_matrix.to_array()
    
    def mutate(self):
        ''' Cria mutações nos pesos da rede neural '''
                
        for wheight in self.wheights:
            wheight.mutate()
            
    def clone(self):
        ''' Cria uma cópia da rede neural '''
        
        result = NeuralNetwork(self.input_size, self.hidden_sizes, self.output_size)
        
        for i, wheight in enumerate(self.wheights):
            result.wheights[i] = wheight.clone()
        
        return result
    
    def load(self, wheights: list[list[list[float]]]) -> None:
        ''' Carrega os pesos da rede neural '''
        
        if len(wheights) != len(self.wheights):
            raise ValueError('Wheights must have the same size')
        
        for i in range(len(wheights)):
            wheight = Matrix.load(wheights[i])
            
            if wheight.rows != self.wheights[i].rows or wheight.cols != self.wheights[i].cols:
                raise ValueError('Wheights must have the same size')
            
            self.wheights[i] = wheight.clone()
    
    def save(self) -> list[Matrix]:
        ''' Salva os pesos da rede neural '''
        
        return [wheight.clone() for wheight in self.wheights]
    
    @staticmethod
    def crossover(a: 'NeuralNetwork', b: 'NeuralNetwork') -> 'NeuralNetwork':
        ''' Cria um cruzamento entre duas redes neurais '''
        
        a_sizes = [a.input_size] + a.hidden_sizes + [a.output_size]
        b_sizes = [b.input_size] + b.hidden_sizes + [b.output_size]
        
        if a_sizes != b_sizes:
            raise ValueError('Neural networks must have the same sizes')
        
        result = NeuralNetwork(a.input_size, a.hidden_sizes, a.output_size)
        
        for i in range(len(result.wheights)):
            result.wheights[i] = Matrix.crossover(a.wheights[i], b.wheights[i])
            
        return result