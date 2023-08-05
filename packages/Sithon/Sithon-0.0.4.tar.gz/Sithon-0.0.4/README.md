# Sithon
A small library used for test cases in Python, heavily inspired on V's test!

*This project was made for learning purposes, and is not meant to be used in real projects, but you can still use it, it
s just not 100% working well.*

# Features
Only supports ``assert x == y`` so far.

Asynchronous test cases supported.

Line count can be a bit off.

# Usage
```py
# All test files needs to be start with `test_`
import math

# All test functions needs to start with `test_`
def test_sum_function():
    assert math.factorial(4) == 5
    assert math.factorial(3) == 6
```

Go to the project directory
```
$ python3.10 -m sithon
./test_math.py:sum_function:6 | FAIL assert math.factorial(4) == 5
        Left value: 24
        Right value: 5

./test_math.py:sum_function:7 | PASSED assert math.factorial(3) == 6    
        Left value: 6
        Right value: 6
```

# Rules
You can't have any other functions that test functions inside of a `test_` file.

You can't use import aliases 

# Install
``pip install sithon``
