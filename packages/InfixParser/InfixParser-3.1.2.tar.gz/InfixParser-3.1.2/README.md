# InfixParser

InfixParser is a Python binding for MathParser (https://github.com/KJ002/MathParser/). This module allows for a simple and quick evaluation of strings. It allows you to evaluate a string with security, you define the external variables!

## Examples

### Basic Eval
```py
result: float = InfixParser.evaluate("1+1") # returns 2.0
```

### Basic Eval (With Evaluator Class)
```py
parser = InfixParser.Evaluator()

result: float = parser.eval("1+1") # returns 2.0
```
### External Variable Eval
```py
parser = InfixParser.Evaluator()

x: int = 20

parser.append_variable("x", x)

result: float = parser.eval("1+x") # returns 21.0
```
### Updating External Variable Eval
```py
parser = InfixParser.Evaluator()

x: int = 20

parser.append_variable("x", x)

result1: float = parser.eval("1+x") # returns 21.0

x: int = 10

parser.append_variable("x", x)

result2: float = parser.eval("1+x") # returns 11.0
```
### Functions Eval
```py
parser = InfixParser.Evaluator()

result: float = parser.eval("sin(1.5707963267948966)") # returns 1.0
```
