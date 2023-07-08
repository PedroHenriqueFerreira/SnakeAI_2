from matrix import Matrix

class NeuralNet:
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
        
nn = NeuralNet(6, [5, 5], 4)

print(nn.output([1] * 6))
