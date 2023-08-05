## Table of contents
* General Info
* Usage
* Technologies used
* Acknowledgement
* License

## General Info
This is a simple python package that can be used to perform the simple mathematical functions:
* Addition
* Subtraction
* Division
* Multiplication
* N-th root of number
* Exponent

## Usage
This calculator can be used for basic mathematical operations. It also has a calculator memory.

Sample Code
```python
from calc import Calculator

cal = Calculator(4)
#sets calculator memory to 4
```
OR
```python
from calc import Calculator

cal = Calculator()
```

#### Addition
```python
cal.add(4)

#returns 4
```
#### Subtraction
```python
cal.subtract(1)

#returns 3
```
#### Multiplication
```python
cal.multiply(2)

#returns 6
```
#### Division
```python
cal.divide(2)

#returns 3
```
#### Memory
```python
cal.memory_value()

#returns 3
```
```python
cal.reset_memory()

#returns 0
```
## Technologies used
* Python version: 3.8

## Acknowledgement
This project was inspired by Turing College

## License
MIT 2021
