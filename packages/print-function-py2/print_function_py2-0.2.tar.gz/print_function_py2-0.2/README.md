# print_function_py2

## Usage

This package is using for print() function in Python 1 and Python 2.

## How to use it

Import it by: `from print_function_py2 import print3`. No any additional modules or packages will be installed.

Use it as the built-in print() function in Python 3.
```python2
>>> from print_function_py2 import print3
>>> print3("Hello", "world!", sep=", ")
Hello, world!
```

If you cannot install the package by pip, please download the tar.gz file and extract to sys.path(PYTHONPATH).

Suggested importing formula:
```python2
try :
    exec("print3 = print")
except SyntaxError :
    try :
        from print_function_py2 import print3
    except ImportError :
        print("package print_function_py2 required")
        import sys
        sys.exit(1)
```
