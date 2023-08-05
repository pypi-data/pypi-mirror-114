# InfixParser

InfixParser is a Python binding for MathParser (https://github.com/KJ002/MathParser/). This module allows for a simple and quick evaluation of strings. It allows you to evaluate a string with security, you define the external variables!

## Examples

### Basic Eval
```py
result: float = InfixParser.evaluate("1+1") # returns 2.0
```

### Basic Eval (With Evaluator Class)
```py
evaluator = InfixParser.Evaluator()

result: float = evaluator.eval("1+1") # returns 2.0
```
### External Variable Eval
```py
evaluator = InfixParser.Evaluator()

x: int = 20

evaluator.append_variable("x", x)

result: float = evaluator.eval("1+x") # returns 21.0
```
### Updating External Variable Eval
```py
evaluator = InfixParser.Evaluator()

x: int = 20

evaluator.append_variable("x", x)

result1: float = evaluator.eval("1+x") # returns 21.0

x: int = 10

evaluator.append_variable("x", x)

result2: float = evaluator.eval("1+x") # returns 11.0
```
### Functions Eval
```py
"""
It is important to note that function do not have to
have to be called with in an instantiated class
and can just be called with InfixParser.evaluate()
"""

evaluator = InfixParser.Evaluator()

result: float = evaluator.eval("sin(1.5707963267948966)") # returns 1.0
```
