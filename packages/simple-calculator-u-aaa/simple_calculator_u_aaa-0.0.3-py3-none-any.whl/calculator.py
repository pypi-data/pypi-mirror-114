class Calculator:
    """"
    This calculator performs the following basic mathematical operations:
    * Addition
    * Subtraction
    * Division
    * Multiplication
    * nth root of number
    * exponent

    Attributes
    ----------
    __value : (int or float)
        the calculator memory value

    Methods
    --------
    input_validation(new_value):
        validates that the value entered is a number or float

    add(new_value: int or float):
        adds the new value to the value in the calculator memory

    subtract(new_value: int or float):
        subtracts the new value from the value in the calculator memory

    multiply(new_value: int or float):
        multiplies the new value with the value in the calculator memory

    divide(new_value: int or float):
        divides the value in the calculator memory with the new value

    n_root(root: int or float):
        takes the (n) root of the value in the calculator memory

    exponent(exponent: int or float):
        raises the values in the calculator memory to the power of the inputted value

    reset_memory():
        resets the calculator memory value to 0

    memory_value():
        returns the calculator memory value
    """

    def __init__(self,  value = 0) -> None:
        """
        initializes the memory value
        """
        self.__input_validation(value)
        self.__value = value

    def __input_validation(self, new_value: (int, float)) -> None:
        """
        validates that the inputted value is an integer or float
        """
        if not isinstance(new_value, (int,float)):
            raise NotANumber(new_value)


    def add(self, new_value: (int,float)) -> (int, float):
        """
        adds the new value to the value in the calculator memory
        """
        self.__input_validation(new_value)
        self.__value += new_value
        return self.__value

    def subtract(self, new_value: (int, float)) -> (int, float):
        """
        subtracts the new value from the value in the calculator memory
        """
        self.__input_validation(new_value)
        self.__value -= new_value
        return self.__value

    def multiply(self, new_value: (int, float)) -> (int, float):
        """
        multiplies the new value with the value in the calculator memory
        """
        self.__input_validation(new_value)
        self.__value *= new_value
        return self.__value

    def divide(self, new_value: (int, float)) -> (int, float):
        """
        divides the value in the calculator memory with the new value
        """
        self.__input_validation(new_value)
        self.__value /= new_value
        return self.__value
        #except (ZeroDivisionError) as err:
                #print(f'Cannot divide by zero -> {err}')

    def n_root(self, root: (int, float)) -> (int, float):
        """
        takes the (n) root of the value in the calculator memory
        """
        self.__input_validation(root)
        if root <= 0:
            raise NotAPositiveNumber(root, type= 'Inputted value')
        elif self.__value <= 0:
            raise NotAPositiveNumber(self.__value, type= 'Memory value')
        else:

            self.__value = self.__value ** (1/root)
            return self.__value

    def exponent(self, exponent: (int, float)) -> (int, float):
        """
        raises the values in the calculator memory to the power of the inputted value
        """
        self.__input_validation(exponent)
        self.__value = self.__value ** exponent
        return self.__value

    def reset_memory(self) -> (int, float):
        """
        resets the calculator memory value to 0
        """
        self.__value = 0
        return self.__value

    def memory_value(self) -> (int, float):
        return self.__value

class NotANumber(Exception):
    """
    Raises an error stating the input is not a number

    Methods
    --------
    __init__(value, message):
        initializes the error class
    __str__():
        returns the inputted value and error message
    """
    def __init__(self, value, message = 'is not a number'):
        """
        initializes the error class
        """
        self.__message = message
        self.__value = value
        super().__init__(self.__message)

    def __str__(self):
        """
        returns the inputted value and error message
        """
        return f'"{self.__value}" {self.__message}'

class NotAPositiveNumber(Exception):
    """
    Raises an error stating the input is not a positive number

    Methods
    --------
    __init__(value, message):
        initializes the error class
    __str__():
        returns the inputted value and error message
    """
    def __init__(self, value, message = 'is not a positive number.The function only accepts positive numbers', type = ''):
        """
        initializes the error class
        """
        self.__message = message
        self.__value = value
        self.__type = type
        super().__init__(self.__message)

    def __str__(self):
        """ returns the value and error message"""
        return f'{self.__type} ({self.__value}) {self.__message}'


