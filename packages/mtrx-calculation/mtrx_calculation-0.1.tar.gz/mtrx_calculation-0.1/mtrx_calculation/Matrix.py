import numpy as np
from .Calculations import Calculation

class Matrix_calculator(Calculation):
    def __init__(self, number1, number2):
        Calculation.__init__(self, number1, number2)
        
    def multiply(self):
        
        return np.dot(self.number1, self.number2)
    
 
    