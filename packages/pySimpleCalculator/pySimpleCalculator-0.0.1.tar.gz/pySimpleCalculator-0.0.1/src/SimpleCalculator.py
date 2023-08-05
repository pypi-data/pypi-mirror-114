from typing import Union

class Calculator:
    def __init__(self)-> None:
        self.answer = 0
        
        
    def validate_input(self, value):   
        if not isinstance (value,  (int,float)):
            raise TypeError("Value entered is not numeric \n Enter a numeric input!!!!")
            
    def reset(self):
        self.answer = 0
        
    def current_value(self):
        return self.answer

    def add(self, number: Union[int, float])-> float:
        self.validate_input(number)
        self.answer += number
        return self.answer

    def subtract(self, number: Union[int, float])-> float:
        self.validate_input(number)
        self.answer -= number
        return self.answer
    

    def multiply(self, number: Union[int, float])-> float:
        self.validate_input(number)                   
        self.answer *= number
        return self.answer
    

    def divide(self, number: Union[int, float])-> float:
        self.validate_input(number)
        try:
            self.answer /= number
            return self.answer
        except ZeroDivisionError as err:
            raise ZeroDivisionError(f"number cannot be zero => {err}") from None
        

    def nth_root(self, root: Union[int, float], number=None)  ->float: 
        try:
            if number != None:
                self.validate_input(number)
                self.validate_input(root)
                self.answer = number ** (root ** -1) 


            else:    
                self.validate_input(root)
                self.answer = self.answer** 1 / root
            return self.answer
        except ZeroDivisionError as err:
            print(f"root cannot  be zero=> {err}")
            

    def exp(self, power, number=None)  ->float:
        if number != None:
            self.validate_input(number)
            self.validate_input(power)
            self.answer = number** power 
        else:
         
            self.validate_input(power) 
            self.answer = self.answer**power 
        return self.answer
