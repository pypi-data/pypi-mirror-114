import math
import numpy as np

class Calculation:
    def __init__ (self, number1, number2):
        self.number1=number1
        self.number2=number2
        
    def addition (self):
        
        return np.add(self.number1,self.number2)
    
    def subtraction (self):
        
        return np.subtract(self.number1,self.number2)